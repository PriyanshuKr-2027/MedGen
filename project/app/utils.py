from functools import wraps
from flask import session, redirect, url_for, flash
import re

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session or session['user_role'] != role:
                flash('Access denied. Insufficient permissions.', 'error')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def parse_ai_response(response_text):
    """Parse AI response into structured format"""
    try:
        # Simple parsing logic for demo - in production, use more sophisticated NLP
        sections = {
            'causes': [],
            'remedies': [],
            'otc_suggestions': [],
            'severity': 'mild'
        }
        
        # Extract severity from keywords
        if any(keyword in response_text.lower() for keyword in ['emergency', 'urgent', 'severe', 'critical']):
            sections['severity'] = 'critical'
        elif any(keyword in response_text.lower() for keyword in ['moderate', 'concerning']):
            sections['severity'] = 'moderate'
        
        # Simple extraction logic (in production, use proper NLP)
        lines = response_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if 'cause' in line.lower():
                current_section = 'causes'
            elif 'remed' in line.lower() or 'treatment' in line.lower():
                current_section = 'remedies'
            elif 'medication' in line.lower() or 'otc' in line.lower():
                current_section = 'otc_suggestions'
            elif line.startswith('•') or line.startswith('-') or line.startswith('*'):
                if current_section and current_section in sections:
                    sections[current_section].append(line[1:].strip())
        
        return sections
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        return {
            'causes': ['Unable to analyze symptoms'],
            'remedies': ['Please consult a healthcare professional'],
            'otc_suggestions': [],
            'severity': 'moderate'
        }