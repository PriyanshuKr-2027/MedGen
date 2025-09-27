from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if 'user_id' in session:
        role = session.get('user_role')
        if role == 'patient':
            return redirect(url_for('patient.dashboard'))
        elif role == 'doctor':
            return redirect(url_for('doctor.dashboard'))
        elif role == 'admin':
            return redirect(url_for('admin.dashboard'))
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        
        # Demo login logic
        demo_credentials = {
            'patient': {'username': 'patient', 'password': 'patient123', 'name': 'John Doe'},
            'doctor': {'username': 'doctor', 'password': 'doctor123', 'name': 'Dr. Sarah Wilson'},
            'admin': {'username': 'admin', 'password': 'admin123', 'name': 'Admin User'}
        }
        
        # Check demo credentials
        if role in demo_credentials:
            demo_user = demo_credentials[role]
            if username == demo_user['username'] and password == demo_user['password']:
                # Find or create user in database
                user = User.query.filter_by(username=username).first()
                if not user:
                    user = User(
                        username=username,
                        password=password,
                        role=role,
                        name=demo_user['name'],
                        age=32 if role == 'patient' else None,
                        gender='Male' if role == 'patient' else None
                    )
                    db.session.add(user)
                    db.session.commit()
                
                # Set session
                session['user_id'] = user.id
                session['user_role'] = user.role
                session['user_name'] = user.name
                
                if request.is_json:
                    return jsonify({
                        'success': True, 
                        'redirect': url_for(f'{role}.dashboard')
                    })
                else:
                    return redirect(url_for(f'{role}.dashboard'))
        
        error_msg = 'Invalid credentials. Use demo accounts: patient/patient123, doctor/doctor123, admin/admin123'
        if request.is_json:
            return jsonify({'success': False, 'error': error_msg}), 401
        else:
            flash(error_msg, 'error')
            return render_template('index.html')
    
    return render_template('index.html')

@auth_bp.route('/demo-login/<role>')
def demo_login(role):
    """Quick demo login"""
    demo_credentials = {
        'patient': {'username': 'patient', 'password': 'patient123', 'name': 'John Doe'},
        'doctor': {'username': 'doctor', 'password': 'doctor123', 'name': 'Dr. Sarah Wilson'},
        'admin': {'username': 'admin', 'password': 'admin123', 'name': 'Admin User'}
    }
    
    if role in demo_credentials:
        demo_user = demo_credentials[role]
        user = User.query.filter_by(username=demo_user['username']).first()
        
        if user:
            session['user_id'] = user.id
            session['user_role'] = user.role
            session['user_name'] = user.name
            return redirect(url_for(f'{role}.dashboard'))
    
    flash('Invalid demo login', 'error')
    return redirect(url_for('auth.index'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.index'))