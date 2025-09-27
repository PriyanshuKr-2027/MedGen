#!/usr/bin/env python3
"""
Test script for follow-up functionality
"""

import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services.ai_service import AIService

def test_followup_suggestions():
    """Test follow-up suggestion generation"""
    print("Testing follow-up suggestion generation...")
    
    ai_service = AIService()
    
    # Test with different urgency levels
    test_cases = [
        {
            'urgency': 'High',
            'possible_causes': ['Severe infection', 'Emergency condition']
        },
        {
            'urgency': 'Moderate', 
            'possible_causes': ['Bacterial infection', 'Moderate condition']
        },
        {
            'urgency': 'Low',
            'possible_causes': ['Common cold', 'Minor condition']
        }
    ]
    
    for i, case in enumerate(test_cases):
        print(f"\nTest case {i+1}: {case['urgency']} urgency")
        suggestions = ai_service.generate_followup_suggestions(case)
        print("Generated suggestions:")
        for j, suggestion in enumerate(suggestions):
            print(f"  {j+1}. {suggestion}")

def test_followup_context():
    """Test follow-up context building"""
    print("\n\nTesting follow-up context building...")
    
    ai_service = AIService()
    
    consultation_history = {
        'symptoms': 'Headache and fever for 2 days',
        'ai_analysis': 'Possible viral infection. Rest and hydration recommended.',
        'severity': 'mild'
    }
    
    patient_info = {
        'age': 30,
        'gender': 'Male'
    }
    
    question = "How long will these symptoms last?"
    
    context = ai_service._build_followup_context(consultation_history, question, patient_info)
    print("Generated context:")
    print(context)
    
    # Test response formatting
    response = ai_service._format_followup_response("The symptoms should resolve in 3-5 days with proper rest.", question)
    print("\nFormatted response:")
    print(response)

if __name__ == "__main__":
    print("Follow-up Functionality Test")
    print("=" * 40)
    
    # Create Flask app and context
    app = create_app()
    
    with app.app_context():
        try:
            test_followup_suggestions()
            test_followup_context()
            print("\n✅ All tests completed successfully!")
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()