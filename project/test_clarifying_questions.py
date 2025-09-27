#!/usr/bin/env python3
"""
Test script for clarifying questions functionality
"""

import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services.ai_service import AIService

def test_clarifying_questions():
    """Test clarifying question generation"""
    print("Testing clarifying question generation...")
    
    ai_service = AIService()
    
    test_cases = [
        "I have a headache and fever",
        "I have chest pain and shortness of breath",
        "I have stomach pain and nausea",
        "I have been coughing for days"
    ]
    
    for i, symptoms in enumerate(test_cases):
        print(f"\nTest case {i+1}: '{symptoms}'")
        questions = ai_service.generate_clarifying_questions(symptoms)
        print(f"Generated {len(questions)} questions:")
        
        for j, question in enumerate(questions):
            print(f"  {j+1}. {question['question']} (Type: {question['type']})")
            if question['type'] == 'radio' and question.get('options'):
                print(f"      Options: {', '.join(question['options'][:3])}...")
        
        # Test preliminary severity assessment
        severity = ai_service._assess_preliminary_severity(symptoms)
        print(f"  Preliminary Severity: {severity}")

def test_analysis_flow():
    """Test the full analysis flow with clarifications"""
    print("\n\nTesting analysis flow...")
    
    ai_service = AIService()
    
    # Test without clarifications (should ask questions)
    symptoms = "I have a bad headache and feel dizzy"
    result = ai_service.analyze_symptoms(symptoms)
    
    if result.get('needs_clarification'):
        print("✅ Correctly identified need for clarification")
        print(f"Questions generated: {len(result['questions'])}")
    else:
        print("❌ Did not identify need for clarification")
    
    # Test with clarifications (should provide analysis)
    clarifications = {
        'duration': '2-3 days',
        'severity_rating': '7',
        'pain_type': 'Throbbing'
    }
    
    result_with_clarifications = ai_service.analyze_symptoms(symptoms, clarifications=clarifications)
    
    if not result_with_clarifications.get('needs_clarification'):
        print("✅ Correctly provided analysis with clarifications")
        print(f"Analysis keys: {list(result_with_clarifications.keys())}")
    else:
        print("❌ Still asking for clarification even with answers provided")

if __name__ == "__main__":
    print("Clarifying Questions Functionality Test")
    print("=" * 50)
    
    # Create Flask app and context
    app = create_app()
    
    with app.app_context():
        try:
            test_clarifying_questions()
            test_analysis_flow()
            print("\n✅ All clarifying questions tests completed successfully!")
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()