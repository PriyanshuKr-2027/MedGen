from flask import Blueprint, render_template, request, jsonify, session
from app.utils import login_required, role_required
from app.models import User, Consultation, Treatment
from app import db
from sqlalchemy import or_, case

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/dashboard')
@login_required
@role_required('doctor')
def dashboard():
    # Get doctor statistics
    total_patients = User.query.filter_by(role='patient').count()
    pending_consultations = Consultation.query.filter_by(status='pending').count()
    critical_cases = Consultation.query.filter_by(severity='critical', status='pending').count()
    completed_today = Consultation.query.filter(
        Consultation.status == 'completed',
        Consultation.updated_at >= db.func.date('now')
    ).count()
    
    stats = {
        'total_patients': total_patients,
        'pending_consultations': pending_consultations,
        'critical_cases': critical_cases,
        'completed_today': completed_today
    }
    
    # Get recent consultations
    recent_consultations = Consultation.query.filter_by(status='pending')\
        .order_by(Consultation.created_at.desc())\
        .limit(10).all()
    
    return render_template('doctor_dashboard.html', stats=stats, consultations=recent_consultations)

@doctor_bp.route('/consultation/<int:consultation_id>')
@login_required
@role_required('doctor')
def view_consultation(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    patient = User.query.get(consultation.patient_id)
    return render_template('consultation_detail.html', 
                         consultation=consultation, patient=patient)

@doctor_bp.route('/add-treatment', methods=['POST'])
@login_required
@role_required('doctor')
def add_treatment():
    try:
        data = request.get_json()
        consultation_id = data.get('consultation_id')
        prescription = data.get('prescription', '')
        notes = data.get('notes', '')
        
        consultation = Consultation.query.get_or_404(consultation_id)
        
        # Create treatment record
        treatment = Treatment(
            consultation_id=consultation_id,
            doctor_id=session['user_id'],
            prescription=prescription,
            notes=notes
        )
        db.session.add(treatment)
        
        # Update consultation status
        consultation.status = 'completed'
        consultation.doctor_id = session['user_id']
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Treatment added successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@doctor_bp.route('/api/stats')
@login_required
@role_required('doctor')
def get_stats():
    """API endpoint to get updated dashboard statistics"""
    try:
        total_patients = User.query.filter_by(role='patient').count()
        pending_consultations = Consultation.query.filter_by(status='pending').count()
        critical_cases = Consultation.query.filter_by(severity='critical', status='pending').count()
        completed_today = Consultation.query.filter(
            Consultation.status == 'completed',
            Consultation.updated_at >= db.func.date('now')
        ).count()
        
        stats = {
            'total_patients': total_patients,
            'pending_consultations': pending_consultations,
            'critical_cases': critical_cases,
            'completed_today': completed_today
        }
        
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@doctor_bp.route('/api/search-patients')
@login_required
@role_required('doctor')
def search_patients():
    """API endpoint for advanced patient search"""
    try:
        search_term = request.args.get('q', '').strip()
        status_filter = request.args.get('status', '')
        severity_filter = request.args.get('severity', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Build query
        query = Consultation.query.join(User, Consultation.patient_id == User.id)
        
        # Apply search term
        if search_term:
            query = query.filter(
                or_(
                    User.id.like(f'%{search_term}%'),
                    User.name.ilike(f'%{search_term}%'),
                    Consultation.symptoms.ilike(f'%{search_term}%')
                )
            )
        
        # Apply filters
        if status_filter:
            query = query.filter(Consultation.status == status_filter)
        if severity_filter:
            query = query.filter(Consultation.severity == severity_filter)
        
        # Order by priority (critical first, then by date)
        query = query.order_by(
            case(
                (Consultation.severity == 'critical', 1),
                (Consultation.severity == 'moderate', 2),
                else_=3
            ),
            Consultation.created_at.desc()
        )
        
        # Paginate results
        results = query.paginate(page=page, per_page=per_page, error_out=False)
        
        consultations = []
        for consultation in results.items:
            consultations.append({
                'id': consultation.id,
                'patient_id': consultation.patient_id,
                'patient_name': consultation.patient.name,
                'symptoms': consultation.symptoms,
                'severity': consultation.severity,
                'status': consultation.status,
                'created_at': consultation.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'patient_age': consultation.patient.age,
                'patient_gender': consultation.patient.gender
            })
        
        return jsonify({
            'success': True,
            'consultations': consultations,
            'total': results.total,
            'pages': results.pages,
            'current_page': page
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@doctor_bp.route('/patient/<int:patient_id>/history')
@login_required
@role_required('doctor')
def patient_history(patient_id):
    """View complete patient history"""
    patient = User.query.get_or_404(patient_id)
    if patient.role != 'patient':
        return "Invalid patient ID", 400
    
    # Get all consultations for this patient
    consultations = Consultation.query.filter_by(patient_id=patient_id)\
        .order_by(Consultation.created_at.desc()).all()
    
    # Get all treatments for this patient
    treatments = Treatment.query.join(Consultation)\
        .filter(Consultation.patient_id == patient_id)\
        .order_by(Treatment.created_at.desc()).all()
    
    return render_template('patient_history.html', 
                         patient=patient, 
                         consultations=consultations,
                         treatments=treatments)

@doctor_bp.route('/api/patient/<int:patient_id>/quick-info')
@login_required
@role_required('doctor')
def patient_quick_info(patient_id):
    """Get quick patient information for modals/tooltips"""
    try:
        patient = User.query.get_or_404(patient_id)
        if patient.role != 'patient':
            return jsonify({'success': False, 'error': 'Invalid patient ID'}), 400
        
        # Get recent consultations
        recent_consultations = Consultation.query.filter_by(patient_id=patient_id)\
            .order_by(Consultation.created_at.desc()).limit(5).all()
        
        # Get recent treatments
        recent_treatments = Treatment.query.join(Consultation)\
            .filter(Consultation.patient_id == patient_id)\
            .order_by(Treatment.created_at.desc()).limit(3).all()
        
        patient_info = {
            'id': patient.id,
            'name': patient.name,
            'age': patient.age,
            'gender': patient.gender,
            'email': patient.email,
            'phone': patient.phone,
            'total_consultations': len(recent_consultations),
            'recent_consultations': [
                {
                    'id': c.id,
                    'symptoms': c.symptoms[:100] + '...' if len(c.symptoms) > 100 else c.symptoms,
                    'severity': c.severity,
                    'status': c.status,
                    'date': c.created_at.strftime('%Y-%m-%d')
                } for c in recent_consultations
            ],
            'recent_treatments': [
                {
                    'id': t.id,
                    'prescription': t.prescription[:100] + '...' if len(t.prescription) > 100 else t.prescription,
                    'date': t.created_at.strftime('%Y-%m-%d')
                } for t in recent_treatments
            ]
        }
        
        return jsonify({'success': True, 'patient': patient_info})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500