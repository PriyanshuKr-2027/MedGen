from flask import Blueprint, render_template, request, jsonify, session
from app.utils import login_required
from app.models import User
import uuid

connect_bp = Blueprint('connect', __name__)

# Store active call sessions (in production, use Redis or database)
active_calls = {}

@connect_bp.route('/doctor')
@login_required
def connect_doctor():
    """Initialize connection to doctor"""
    user_role = session.get('user_role')
    
    # Generate unique room ID
    room_id = str(uuid.uuid4())
    
    # Get available doctors (demo data)
    doctors = User.query.filter_by(role='doctor').all()
    
    return render_template('connect_call.html', 
                         room_id=room_id, 
                         user_role=user_role,
                         doctors=doctors)

@connect_bp.route('/join/<room_id>')
@login_required
def join_call(room_id):
    """Join an existing call"""
    user_role = session.get('user_role')
    user_name = session.get('user_name')
    
    return render_template('connect_call.html',
                         room_id=room_id,
                         user_role=user_role,
                         user_name=user_name)

@connect_bp.route('/api/create-room', methods=['POST'])
@login_required
def create_room():
    """Create a new call room"""
    try:
        data = request.get_json()
        room_type = data.get('type', 'consultation')
        
        room_id = str(uuid.uuid4())
        user_id = session.get('user_id')
        user_name = session.get('user_name')
        
        # Store room info
        active_calls[room_id] = {
            'creator': user_id,
            'creator_name': user_name,
            'type': room_type,
            'participants': [user_id],
            'created_at': str(uuid.uuid4())  # Use current timestamp in production
        }
        
        return jsonify({
            'success': True,
            'room_id': room_id,
            'join_url': f'/connect/join/{room_id}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@connect_bp.route('/api/room-info/<room_id>')
@login_required
def room_info(room_id):
    """Get room information"""
    if room_id in active_calls:
        room = active_calls[room_id]
        return jsonify({
            'success': True,
            'room': room
        })
    else:
        return jsonify({'success': False, 'error': 'Room not found'}), 404

@connect_bp.route('/api/join-room', methods=['POST'])
@login_required
def join_room_api():
    """Join a room via API"""
    try:
        data = request.get_json()
        room_id = data.get('room_id')
        
        if room_id not in active_calls:
            return jsonify({'success': False, 'error': 'Room not found'}), 404
        
        user_id = session.get('user_id')
        if user_id not in active_calls[room_id]['participants']:
            active_calls[room_id]['participants'].append(user_id)
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500