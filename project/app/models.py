from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # patient, doctor, admin
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    consultations = db.relationship('Consultation', backref='patient', lazy=True, foreign_keys='Consultation.patient_id')
    treatments = db.relationship('Treatment', backref='doctor', lazy=True, foreign_keys='Treatment.doctor_id')

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    symptoms = db.Column(db.Text, nullable=False)
    ai_analysis = db.Column(db.Text)
    severity = db.Column(db.String(20))  # mild, moderate, critical
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consultation_id = db.Column(db.Integer, db.ForeignKey('consultation.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    follow_up_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    consultation = db.relationship('Consultation', backref='treatments')

class FollowUpQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consultation_id = db.Column(db.Integer, db.ForeignKey('consultation.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    consultation = db.relationship('Consultation', backref='followup_questions')
    patient = db.relationship('User', backref='followup_questions')