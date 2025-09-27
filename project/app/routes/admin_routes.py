from flask import Blueprint, render_template, jsonify, session
from app.utils import login_required, role_required
from app.models import User, Consultation
from app import db
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    # Get system statistics
    total_patients = User.query.filter_by(role='patient').count()
    total_doctors = User.query.filter_by(role='doctor').count()
    total_consultations = Consultation.query.count()
    
    # Severity breakdown
    severity_stats = db.session.query(
        Consultation.severity, 
        func.count(Consultation.id)
    ).group_by(Consultation.severity).all()
    
    severity_breakdown = {
        'mild': 0,
        'moderate': 0, 
        'critical': 0
    }
    
    for severity, count in severity_stats:
        if severity in severity_breakdown:
            severity_breakdown[severity] = count
    
    # Recent activity
    recent_consultations = Consultation.query.order_by(
        Consultation.created_at.desc()
    ).limit(10).all()
    
    stats = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_consultations': total_consultations,
        'severity_breakdown': severity_breakdown
    }
    
    return render_template('admin_dashboard.html', 
                         stats=stats, 
                         recent_consultations=recent_consultations)

@admin_bp.route('/analytics')
@login_required
@role_required('admin')
def analytics():
    # Daily consultation trends
    daily_stats = db.session.query(
        func.date(Consultation.created_at).label('date'),
        func.count(Consultation.id).label('count')
    ).group_by(func.date(Consultation.created_at)).limit(30).all()
    
    return jsonify({
        'daily_consultations': [
            {'date': str(stat.date), 'count': stat.count} 
            for stat in daily_stats
        ]
    })