from flask import Blueprint, request, jsonify, send_file, current_app
from app.utils import login_required
from app.services.voice_service import VoiceService
import tempfile
import os

voice_bp = Blueprint('voice', __name__)

# Global voice service instance
voice_service = None

def get_voice_service():
    global voice_service
    if voice_service is None:
        voice_service = VoiceService()
    return voice_service

@voice_bp.route('/speech-to-text', methods=['POST'])
@login_required
def speech_to_text():
    try:
        service = get_voice_service()
        
        # Check if audio file was uploaded
        if 'audio' in request.files:
            audio_file = request.files['audio']
            if audio_file.filename:
                # Save temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                audio_file.save(temp_file.name)
                
                # Process the audio file
                result = service.speech_to_text(temp_file.name)
                
                # Clean up
                os.unlink(temp_file.name)
                
                return jsonify(result)
        
        # Record from microphone
        result = service.speech_to_text()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Speech recognition failed: {str(e)}'
        }), 500

@voice_bp.route('/text-to-speech', methods=['POST'])
@login_required
def text_to_speech():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        
        service = get_voice_service()
        result = service.text_to_speech(text)
        
        if result['success']:
            return jsonify({
                'success': True,
                'audio_url': f'/voice/audio/{os.path.basename(result["audio_path"])}'
            })
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Text-to-speech failed: {str(e)}'
        }), 500

@voice_bp.route('/audio/<filename>')
@login_required
def serve_audio(filename):
    try:
        # Serve generated audio files
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)
        
        if os.path.exists(file_path):
            return send_file(file_path, mimetype='audio/wav')
        else:
            return jsonify({'error': 'Audio file not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@voice_bp.route('/quick-listen', methods=['POST'])
@login_required
def quick_listen():
    """Quick speech recognition for real-time chat"""
    try:
        service = get_voice_service()
        result = service.quick_speech_recognition()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@voice_bp.route('/microphone-test')
@login_required
def microphone_test():
    """Test if microphone is available"""
    try:
        service = get_voice_service()
        available = service.is_microphone_available()
        return jsonify({'available': available})
    except Exception as e:
        return jsonify({'available': False, 'error': str(e)})