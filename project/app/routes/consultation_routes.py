from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.utils import login_required
from app.models import User, Consultation
from app import db

consultation_bp = Blueprint('consultation', __name__)

@consultation_bp.route('/<int:consultation_id>')
@login_required
def view_consultation(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    
    # Check if user has permission to view this consultation
    user_role = session.get('user_role')
    user_id = session.get('user_id')
    
    if user_role == 'patient' and consultation.patient_id != user_id:
        return redirect(url_for('patient.dashboard'))
    elif user_role not in ['doctor', 'admin'] and consultation.patient_id != user_id:
        return redirect(url_for('auth.index'))
    
    patient = User.query.get(consultation.patient_id)
    doctor = None
    if consultation.doctor_id:
        doctor = User.query.get(consultation.doctor_id)
    
    return render_template('consultation_detail.html',
                         consultation=consultation,
                         patient=patient,
                         doctor=doctor)

@consultation_bp.route('/update-status', methods=['POST'])
@login_required
def update_status():
    try:
        data = request.get_json()
        consultation_id = data.get('consultation_id')
        status = data.get('status')
        
        consultation = Consultation.query.get_or_404(consultation_id)
        consultation.status = status
        
        if session.get('user_role') == 'doctor':
            consultation.doctor_id = session.get('user_id')
        
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500