from flask import Blueprint, render_template, request, jsonify, session
from app.utils import login_required, role_required
from app.models import User, Consultation
from app.services.ai_service import AIService
from app import db

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/dashboard')
@login_required
@role_required('patient')
def dashboard():
    user = User.query.get(session['user_id'])
    
    # Get patient statistics
    total_consultations = Consultation.query.filter_by(patient_id=user.id).count()
    pending_reports = Consultation.query.filter_by(patient_id=user.id, status='pending').count()
    emergency_contacts = 2  # Demo data
    health_alerts = 0  # Demo data
    
    stats = {
        'total_consultations': total_consultations,
        'pending_reports': pending_reports,
        'emergency_contacts': emergency_contacts,
        'health_alerts': health_alerts
    }
    
    return render_template('patient_dashboard.html', user=user, stats=stats)

@patient_bp.route('/symptom-report')
@login_required
@role_required('patient')
def symptom_report():
    return render_template('symptom_report.html')

@patient_bp.route('/analyze-symptoms', methods=['POST'])
@login_required
@role_required('patient')
def analyze_symptoms():
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', '')
        clarifications = data.get('clarifications')
        
        if not symptoms:
            return jsonify({'success': False, 'error': 'No symptoms provided'}), 400
        
        # Get user info
        user = User.query.get(session['user_id'])
        patient_info = {
            'age': user.age,
            'gender': user.gender
        }
        
        # Analyze symptoms using AI service
        ai_service = AIService()
        analysis = ai_service.analyze_symptoms(symptoms, patient_info, clarifications)
        
        # Check if we need clarifying questions
        if analysis.get('needs_clarification'):
            return jsonify({
                'success': True,
                'needs_clarification': True,
                'questions': analysis['questions'],
                'preliminary_severity': analysis['preliminary_severity']
            })
        
        # Determine severity
        severity = analysis.get('urgency', 'Low').lower()
        if severity == 'high':
            severity = 'critical'
        elif severity == 'moderate':
            severity = 'moderate'
        else:
            severity = 'mild'
        
        # Save consultation to database
        consultation = Consultation(
            patient_id=user.id,
            symptoms=symptoms,
            ai_analysis=analysis.get('full_response', ''),
            severity=severity,
            status='pending'
        )
        db.session.add(consultation)
        db.session.commit()
        
        # Save clarifications if provided
        if clarifications:
            # Store clarifications as JSON in a separate field or table
            # For now, we'll append to symptoms
            clarification_text = "\n\nAdditional Information:"
            for key, value in clarifications.items():
                clarification_text += f"\n- {key.replace('_', ' ').title()}: {value}"
            consultation.symptoms += clarification_text
            db.session.commit()
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'consultation_id': consultation.id,
            'severity': severity
        })
        
    except Exception as e:
        print(f"Error analyzing symptoms: {e}")
        return jsonify({
            'success': False, 
            'error': 'Failed to analyze symptoms. Please try again.'
        }), 500

@patient_bp.route('/consultation-history')
@login_required
@role_required('patient')
def consultation_history():
    user_id = session['user_id']
    consultations = Consultation.query.filter_by(patient_id=user_id).order_by(Consultation.created_at.desc()).all()
    return render_template('consultation_history.html', consultations=consultations)

@patient_bp.route('/chat-interface')
@login_required
@role_required('patient')
def chat_interface():
    return render_template('chat_interface.html')

@patient_bp.route('/disease-info')
@login_required
@role_required('patient')
def disease_info():
    return render_template('disease_info.html')

@patient_bp.route('/get-disease-info', methods=['POST'])
@login_required
@role_required('patient')
def get_disease_info():
    try:
        data = request.get_json()
        disease_name = data.get('disease_name', '').strip()
        
        if not disease_name:
            return jsonify({'success': False, 'error': 'Disease name is required'}), 400
        
        # Get disease information using AI service
        ai_service = AIService()
        disease_info = ai_service.get_disease_information(disease_name)
        
        return jsonify({
            'success': True,
            'disease_info': disease_info
        })
        
    except Exception as e:
        print(f"Error getting disease information: {e}")
        return jsonify({
            'success': False, 
            'error': 'Failed to get disease information. Please try again.'
        }), 500

@patient_bp.route('/ask-followup', methods=['POST'])
@login_required
@role_required('patient')
def ask_followup():
    try:
        data = request.get_json()
        consultation_id = data.get('consultation_id')
        question = data.get('question', '').strip()
        
        if not consultation_id or not question:
            return jsonify({'success': False, 'error': 'Consultation ID and question are required'}), 400
        
        # Get the consultation
        consultation = Consultation.query.get_or_404(consultation_id)
        
        # Verify patient owns this consultation
        if consultation.patient_id != session['user_id']:
            return jsonify({'success': False, 'error': 'Access denied'}), 403
        
        # Get user info
        user = User.query.get(session['user_id'])
        patient_info = {
            'age': user.age,
            'gender': user.gender
        }
        
        # Prepare consultation history
        consultation_history = {
            'symptoms': consultation.symptoms,
            'ai_analysis': consultation.ai_analysis,
            'severity': consultation.severity
        }
        
        # Ask follow-up question using AI service
        ai_service = AIService()
        response = ai_service.ask_followup_question(consultation_history, question, patient_info)
        
        # Save follow-up question and response
        from app.models import FollowUpQuestion
        followup = FollowUpQuestion(
            consultation_id=consultation_id,
            patient_id=user.id,
            question=question,
            ai_response=response.get('answer', '')
        )
        db.session.add(followup)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'response': response,
            'followup_id': followup.id
        })
        
    except Exception as e:
        print(f"Error processing follow-up question: {e}")
        return jsonify({
            'success': False, 
            'error': 'Failed to process follow-up question. Please try again.'
        }), 500

@patient_bp.route('/get-followup-suggestions', methods=['POST'])
@login_required
@role_required('patient')
def get_followup_suggestions():
    try:
        data = request.get_json()
        consultation_id = data.get('consultation_id')
        
        if not consultation_id:
            return jsonify({'success': False, 'error': 'Consultation ID is required'}), 400
        
        # Get the consultation
        consultation = Consultation.query.get_or_404(consultation_id)
        
        # Verify patient owns this consultation
        if consultation.patient_id != session['user_id']:
            return jsonify({'success': False, 'error': 'Access denied'}), 403
        
        # Parse the AI analysis to get structured data
        symptoms_analysis = {}
        if consultation.ai_analysis:
            # Simple parsing - in production, you'd store structured data
            symptoms_analysis = {
                'urgency': consultation.severity.title() if consultation.severity else 'Low',
                'possible_causes': []  # Would be extracted from ai_analysis
            }
        
        # Generate follow-up suggestions
        ai_service = AIService()
        suggestions = ai_service.generate_followup_suggestions(symptoms_analysis)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
        
    except Exception as e:
        print(f"Error generating follow-up suggestions: {e}")
        return jsonify({
            'success': False, 
            'error': 'Failed to generate suggestions. Please try again.'
        }), 500

@patient_bp.route('/get-followup-history/<int:consultation_id>')
@login_required
@role_required('patient')
def get_followup_history(consultation_id):
    try:
        # Get the consultation
        consultation = Consultation.query.get_or_404(consultation_id)
        
        # Verify patient owns this consultation
        if consultation.patient_id != session['user_id']:
            return jsonify({'success': False, 'error': 'Access denied'}), 403
        
        # Get all follow-up questions for this consultation
        from app.models import FollowUpQuestion
        followups = FollowUpQuestion.query.filter_by(
            consultation_id=consultation_id
        ).order_by(FollowUpQuestion.created_at.desc()).all()
        
        followup_data = []
        for followup in followups:
            followup_data.append({
                'id': followup.id,
                'question': followup.question,
                'answer': followup.ai_response,
                'created_at': followup.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({
            'success': True,
            'followups': followup_data
        })
        
    except Exception as e:
        print(f"Error getting follow-up history: {e}")
        return jsonify({
            'success': False, 
            'error': 'Failed to get follow-up history. Please try again.'
        }), 500