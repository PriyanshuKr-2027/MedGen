from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure instance folder exists relative to the app root
    instance_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Import models
    from app.models import User, Consultation, Treatment, FollowUpQuestion
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.patient_routes import patient_bp
    from app.routes.doctor_routes import doctor_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.consultation_routes import consultation_bp
    from app.routes.voice_routes import voice_bp
    from app.routes.connect_routes import connect_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(doctor_bp, url_prefix='/doctor')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(consultation_bp, url_prefix='/consultation')
    app.register_blueprint(voice_bp, url_prefix='/voice')
    app.register_blueprint(connect_bp, url_prefix='/connect')
    
    # Create tables
    with app.app_context():
        db.create_all()
        
        # Create demo users if they don't exist
        if not User.query.filter_by(username='patient').first():
            demo_patient = User(username='patient', password='patient123', role='patient', name='John Doe')
            db.session.add(demo_patient)
            
        if not User.query.filter_by(username='doctor').first():
            demo_doctor = User(username='doctor', password='doctor123', role='doctor', name='Dr. Sarah Wilson')
            db.session.add(demo_doctor)
            
        if not User.query.filter_by(username='admin').first():
            demo_admin = User(username='admin', password='admin123', role='admin', name='Admin User')
            db.session.add(demo_admin)
            
        db.session.commit()
    
    return app