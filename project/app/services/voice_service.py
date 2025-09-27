import speech_recognition as sr
import pyttsx3
import tempfile
import os
from threading import Lock
import time

class VoiceService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.tts_lock = Lock()
        
        # Configure TTS settings
        self._configure_tts()
        
        # Adjust for ambient noise
        with self.microphone as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            except:
                pass  # Fallback if microphone not available
    
    def _configure_tts(self):
        """Configure text-to-speech settings"""
        try:
            # Set properties
            self.tts_engine.setProperty('rate', 150)  # Speaking rate
            self.tts_engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)
            
            # Get available voices and set a pleasant one
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
        except Exception as e:
            print(f"TTS configuration error: {e}")
    
    def speech_to_text(self, audio_file_path=None, timeout=10):
        """Convert speech to text from microphone or audio file"""
        try:
            if audio_file_path:
                # Process uploaded audio file
                with sr.AudioFile(audio_file_path) as source:
                    audio = self.recognizer.record(source)
            else:
                # Record from microphone
                with self.microphone as source:
                    print("Listening...")
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=30)
            
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            return {"success": True, "text": text}
            
        except sr.WaitTimeoutError:
            return {"success": False, "error": "Listening timeout - no speech detected"}
        except sr.UnknownValueError:
            return {"success": False, "error": "Could not understand audio"}
        except sr.RequestError as e:
            return {"success": False, "error": f"Could not request results from speech recognition service; {e}"}
        except Exception as e:
            return {"success": False, "error": f"Speech recognition error: {str(e)}"}
    
    def text_to_speech(self, text, output_path=None):
        """Convert text to speech audio file"""
        try:
            with self.tts_lock:
                if not output_path:
                    # Create temporary file
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                    output_path = temp_file.name
                    temp_file.close()
                
                # Generate speech
                self.tts_engine.save_to_file(text, output_path)
                self.tts_engine.runAndWait()
                
                # Verify file was created
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    return {"success": True, "audio_path": output_path}
                else:
                    return {"success": False, "error": "Failed to generate audio file"}
                    
        except Exception as e:
            return {"success": False, "error": f"Text-to-speech error: {str(e)}"}
    
    def quick_speech_recognition(self):
        """Quick speech recognition for real-time use"""
        try:
            with self.microphone as source:
                # Quick listen with shorter timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
            
            # Use Google's free service
            text = self.recognizer.recognize_google(audio)
            return {"success": True, "text": text, "confidence": 0.8}
            
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return {"success": False, "error": "No speech detected"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def is_microphone_available(self):
        """Check if microphone is available"""
        try:
            with self.microphone as source:
                pass
            return True
        except:
            return False