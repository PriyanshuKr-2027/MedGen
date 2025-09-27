import requests
import json
from flask import current_app

class AIService:
    def __init__(self):
        self.api_key = current_app.config['OPENROUTER_API_KEY']
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "deepseek/deepseek-chat"
    
    def analyze_symptoms(self, symptoms, patient_info=None, clarifications=None):
        """Analyze patient symptoms using DeepSeek AI"""
        try:
            # Check if we need to ask clarifying questions first
            if not clarifications:
                clarifying_questions = self.generate_clarifying_questions(symptoms, patient_info)
                if clarifying_questions:
                    return {
                        'needs_clarification': True,
                        'questions': clarifying_questions,
                        'preliminary_severity': self._assess_preliminary_severity(symptoms)
                    }
            
            # Construct the prompt with clarifications
            prompt = self._build_medical_prompt(symptoms, patient_info, clarifications)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are MedGen, a helpful medical AI assistant for the MedGen telemedicine platform. Provide symptom analysis, possible causes, remedies, and OTC medication suggestions. Always remind users to consult healthcare professionals for serious concerns."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response = requests.post(self.base_url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                return self._format_response(ai_response)
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return self._fallback_response()
                
        except Exception as e:
            print(f"AI Service Error: {e}")
            return self._fallback_response()
    
    def generate_clarifying_questions(self, symptoms, patient_info=None):
        """Generate clarifying questions based on initial symptoms"""
        try:
            # Generate context-aware questions based on symptoms
            questions = []
            symptoms_lower = symptoms.lower()
            
            # Duration question - always ask
            questions.append({
                'id': 'duration',
                'question': 'How long have you been experiencing these symptoms?',
                'type': 'radio',
                'options': [
                    'Less than 24 hours',
                    '1-3 days',
                    '4-7 days',
                    'More than a week',
                    'Several weeks or months'
                ]
            })
            
            # Severity rating - always ask
            questions.append({
                'id': 'severity_rating',
                'question': 'On a scale of 1-10, how would you rate the severity of your symptoms? (1 = mild discomfort, 10 = unbearable)',
                'type': 'slider',
                'min': 1,
                'max': 10,
                'default': 5
            })
            
            # Pain-specific questions
            if any(word in symptoms_lower for word in ['pain', 'ache', 'hurt', 'sore']):
                questions.append({
                    'id': 'pain_type',
                    'question': 'How would you describe the pain?',
                    'type': 'radio',
                    'options': [
                        'Sharp and stabbing',
                        'Dull and aching',
                        'Throbbing',
                        'Burning',
                        'Cramping'
                    ]
                })
                
                questions.append({
                    'id': 'pain_triggers',
                    'question': 'What makes the pain worse?',
                    'type': 'checkbox',
                    'options': [
                        'Movement',
                        'Rest',
                        'Eating',
                        'Breathing',
                        'Touch/pressure',
                        'Nothing specific'
                    ]
                })
            
            # Fever-related questions
            if any(word in symptoms_lower for word in ['fever', 'hot', 'temperature', 'chills']):
                questions.append({
                    'id': 'temperature',
                    'question': 'Have you measured your temperature?',
                    'type': 'radio',
                    'options': [
                        'No fever (below 100°F/37.8°C)',
                        'Low-grade fever (100-102°F/37.8-38.9°C)',
                        'High fever (above 102°F/38.9°C)',
                        'Haven\'t measured'
                    ]
                })
            
            # Respiratory symptoms
            if any(word in symptoms_lower for word in ['cough', 'breathing', 'chest', 'throat']):
                questions.append({
                    'id': 'breathing_difficulty',
                    'question': 'Are you experiencing any breathing difficulties?',
                    'type': 'radio',
                    'options': [
                        'No breathing problems',
                        'Mild shortness of breath',
                        'Difficulty breathing with activity',
                        'Difficulty breathing at rest',
                        'Severe breathing problems'
                    ]
                })
            
            # Digestive symptoms
            if any(word in symptoms_lower for word in ['stomach', 'nausea', 'vomit', 'diarrhea', 'constipation']):
                questions.append({
                    'id': 'eating_drinking',
                    'question': 'How is your appetite and ability to keep food/fluids down?',
                    'type': 'radio',
                    'options': [
                        'Normal appetite, no problems',
                        'Reduced appetite but can eat',
                        'Very little appetite',
                        'Unable to keep food down',
                        'Unable to keep fluids down'
                    ]
                })
            
            # Recent changes
            questions.append({
                'id': 'recent_changes',
                'question': 'Have you had any recent changes or exposures?',
                'type': 'checkbox',
                'options': [
                    'Recent travel',
                    'Contact with sick people',
                    'New medications',
                    'Diet changes',
                    'Stress or life changes',
                    'None of the above'
                ]
            })
            
            # Limit to 4-5 most relevant questions
            return questions[:5]
            
        except Exception as e:
            print(f"Error generating clarifying questions: {e}")
            return []
    
    def _assess_preliminary_severity(self, symptoms):
        """Assess preliminary severity based on symptoms"""
        symptoms_lower = symptoms.lower()
        
        # High severity indicators
        high_severity_keywords = [
            'severe', 'unbearable', 'chest pain', 'difficulty breathing', 
            'can\'t breathe', 'blood', 'unconscious', 'seizure', 'emergency'
        ]
        
        # Moderate severity indicators
        moderate_severity_keywords = [
            'moderate', 'worsening', 'fever', 'vomiting', 'persistent'
        ]
        
        if any(keyword in symptoms_lower for keyword in high_severity_keywords):
            return 'High'
        elif any(keyword in symptoms_lower for keyword in moderate_severity_keywords):
            return 'Moderate'
        else:
            return 'Low'

    def _build_medical_prompt(self, symptoms, patient_info, clarifications=None):
        """Build a comprehensive medical analysis prompt"""
        prompt = f"""
        Please analyze the following symptoms and provide a structured medical assessment:

        PATIENT SYMPTOMS: {symptoms}
        """
        
        if patient_info:
            prompt += f"""
        PATIENT INFO:
        - Age: {patient_info.get('age', 'Not specified')}
        - Gender: {patient_info.get('gender', 'Not specified')}
        """
        
        if clarifications:
            prompt += f"""
        ADDITIONAL INFORMATION FROM PATIENT:
        """
            for key, value in clarifications.items():
                prompt += f"- {key.replace('_', ' ').title()}: {value}\n"
        
        prompt += """
        
        Please provide:
        
        1. POSSIBLE CAUSES (3-5 most likely conditions)
        2. RECOMMENDED REMEDIES (home care and lifestyle changes)
        3. OTC MEDICATIONS (safe over-the-counter options with dosages)
        4. URGENCY LEVEL (Low/Moderate/High)
        5. WHEN TO SEEK IMMEDIATE CARE
        
        Format your response clearly with bullet points. Always include appropriate medical disclaimers.
        """
        
        return prompt
    
    def _format_response(self, ai_response):
        """Format AI response into structured data"""
        try:
            # Parse the response into structured format
            sections = {
                'possible_causes': [],
                'remedies': [],
                'otc_suggestions': [],
                'urgency': 'Low',
                'seek_care': '',
                'full_response': ai_response
            }
            
            lines = ai_response.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Identify sections
                if 'possible causes' in line.lower():
                    current_section = 'possible_causes'
                elif 'recommended remedies' in line.lower() or 'home care' in line.lower():
                    current_section = 'remedies'
                elif 'otc medication' in line.lower() or 'over-the-counter' in line.lower():
                    current_section = 'otc_suggestions'
                elif 'urgency' in line.lower():
                    if 'high' in line.lower() or 'urgent' in line.lower():
                        sections['urgency'] = 'High'
                    elif 'moderate' in line.lower():
                        sections['urgency'] = 'Moderate'
                elif 'seek immediate care' in line.lower() or 'emergency' in line.lower():
                    current_section = 'seek_care'
                elif line.startswith(('•', '-', '*')) or line[0].isdigit():
                    # Extract bullet point content
                    content = line.lstrip('•-*0123456789. ').strip()
                    if current_section and current_section in ['possible_causes', 'remedies', 'otc_suggestions']:
                        sections[current_section].append(content)
                    elif current_section == 'seek_care':
                        sections['seek_care'] += content + ' '
            
            # Ensure we have some content
            if not any(sections[key] for key in ['possible_causes', 'remedies']):
                return self._fallback_response()
            
            return sections
            
        except Exception as e:
            print(f"Error formatting AI response: {e}")
            return self._fallback_response()
    
    def get_disease_information(self, disease_name):
        """Get comprehensive information about a specific disease"""
        try:
            prompt = f"""
            Please provide comprehensive information about {disease_name}. Structure your response with:

            1. OVERVIEW (brief description of the disease)
            2. SYMPTOMS (common signs and symptoms)
            3. CAUSES (what causes this condition)
            4. TREATMENT OPTIONS (medical treatments available)
            5. HOME REMEDIES (safe home care options)
            6. OTC MEDICATIONS (over-the-counter medicines that can help)
            7. PREVENTION (how to prevent this condition)
            8. WHEN TO SEE A DOCTOR (warning signs requiring medical attention)

            Format your response clearly with bullet points. Include appropriate medical disclaimers.
            """

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are MedGen, a knowledgeable medical AI assistant. Provide accurate, comprehensive disease information suitable for patient education. Always include appropriate medical disclaimers and emphasize the importance of professional medical consultation."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.6,
                "max_tokens": 1500
            }

            response = requests.post(self.base_url, headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                return self._format_disease_response(ai_response, disease_name)
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return self._fallback_disease_response(disease_name)

        except Exception as e:
            print(f"Disease Information Error: {e}")
            return self._fallback_disease_response(disease_name)

    def _format_disease_response(self, ai_response, disease_name):
        """Format disease information response"""
        try:
            sections = {
                'disease_name': disease_name,
                'overview': '',
                'symptoms': [],
                'causes': [],
                'treatment': [],
                'home_remedies': [],
                'otc_medications': [],
                'prevention': [],
                'when_to_see_doctor': '',
                'full_response': ai_response
            }

            lines = ai_response.split('\n')
            current_section = None

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Identify sections
                line_lower = line.lower()
                if 'overview' in line_lower:
                    current_section = 'overview'
                elif 'symptom' in line_lower:
                    current_section = 'symptoms'
                elif 'cause' in line_lower:
                    current_section = 'causes'
                elif 'treatment' in line_lower and 'home' not in line_lower and 'otc' not in line_lower:
                    current_section = 'treatment'
                elif 'home' in line_lower and 'remed' in line_lower:
                    current_section = 'home_remedies'
                elif 'otc' in line_lower or 'over-the-counter' in line_lower:
                    current_section = 'otc_medications'
                elif 'prevention' in line_lower or 'prevent' in line_lower:
                    current_section = 'prevention'
                elif 'when to see' in line_lower or 'see a doctor' in line_lower or 'warning' in line_lower:
                    current_section = 'when_to_see_doctor'
                elif line.startswith(('•', '-', '*')) or (line[0].isdigit() and '.' in line[:3]):
                    # Extract bullet point content
                    content = line.lstrip('•-*0123456789. ').strip()
                    if current_section and current_section in ['symptoms', 'causes', 'treatment', 'home_remedies', 'otc_medications', 'prevention']:
                        sections[current_section].append(content)
                    elif current_section == 'when_to_see_doctor':
                        sections['when_to_see_doctor'] += content + ' '
                elif current_section == 'overview' and not any(word in line_lower for word in ['symptoms', 'causes', 'treatment', 'prevention']):
                    sections['overview'] += line + ' '

            # Clean up overview
            sections['overview'] = sections['overview'].strip()
            sections['when_to_see_doctor'] = sections['when_to_see_doctor'].strip()

            return sections

        except Exception as e:
            print(f"Error formatting disease response: {e}")
            return self._fallback_disease_response(disease_name)

    def _fallback_disease_response(self, disease_name):
        """Provide fallback response for disease information"""
        return {
            'disease_name': disease_name,
            'overview': f'{disease_name} is a medical condition that requires proper diagnosis and treatment.',
            'symptoms': ['Consult a healthcare professional for accurate symptom information'],
            'causes': ['Multiple factors may contribute to this condition'],
            'treatment': ['Professional medical evaluation and treatment recommended'],
            'home_remedies': ['Rest and maintain good hygiene', 'Stay hydrated', 'Follow doctor\'s recommendations'],
            'otc_medications': ['Consult pharmacist or doctor before taking any medications'],
            'prevention': ['Maintain good hygiene', 'Follow healthy lifestyle practices'],
            'when_to_see_doctor': 'Consult a healthcare professional for proper diagnosis and treatment.',
            'full_response': f'Detailed information about {disease_name} is temporarily unavailable. Please consult a healthcare professional for accurate medical information.'
        }

    def ask_followup_question(self, consultation_history, new_question, patient_info=None):
        """Ask follow-up questions based on previous consultation"""
        try:
            # Build context from consultation history
            context = self._build_followup_context(consultation_history, new_question, patient_info)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are MedGen, a helpful medical AI assistant providing follow-up consultation. Based on the previous consultation context, answer the patient's new question. Provide specific, relevant advice while maintaining medical accuracy and safety."
                    },
                    {
                        "role": "user",
                        "content": context
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 800
            }
            
            response = requests.post(self.base_url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                return self._format_followup_response(ai_response, new_question)
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return self._fallback_followup_response(new_question)
                
        except Exception as e:
            print(f"Follow-up AI Service Error: {e}")
            return self._fallback_followup_response(new_question)
    
    def generate_followup_suggestions(self, symptoms_analysis):
        """Generate suggested follow-up questions based on initial analysis"""
        try:
            urgency = symptoms_analysis.get('urgency', 'Low')
            possible_causes = symptoms_analysis.get('possible_causes', [])
            
            suggestions = []
            
            # Generate context-aware follow-up questions
            if urgency == 'High':
                suggestions = [
                    "What should I do if my symptoms get worse?",
                    "How quickly should I seek medical attention?",
                    "What warning signs should I watch for?"
                ]
            elif urgency == 'Moderate':
                suggestions = [
                    "How long should I wait before seeing a doctor?",
                    "What can I do to prevent this from getting worse?",
                    "Are there any dietary changes I should make?"
                ]
            else:
                suggestions = [
                    "How long will these symptoms typically last?",
                    "What activities should I avoid while recovering?",
                    "How can I prevent this from happening again?",
                    "What home remedies work best for my condition?"
                ]
            
            # Add cause-specific questions
            if any('infection' in cause.lower() for cause in possible_causes):
                suggestions.append("How can I prevent spreading this to others?")
            
            if any('allerg' in cause.lower() for cause in possible_causes):
                suggestions.append("How can I identify what I'm allergic to?")
            
            return suggestions[:4]  # Return top 4 suggestions
            
        except Exception as e:
            print(f"Error generating follow-up suggestions: {e}")
            return [
                "How long will these symptoms last?",
                "What should I avoid while recovering?",
                "When should I see a doctor?",
                "How can I prevent this in the future?"
            ]
    
    def _build_followup_context(self, consultation_history, new_question, patient_info):
        """Build context for follow-up questions"""
        context = f"""
        PREVIOUS CONSULTATION CONTEXT:
        Original Symptoms: {consultation_history.get('symptoms', 'Not specified')}
        AI Analysis: {consultation_history.get('ai_analysis', 'Not available')}
        Severity: {consultation_history.get('severity', 'Not specified')}
        
        """
        
        if patient_info:
            context += f"""
        PATIENT INFO:
        - Age: {patient_info.get('age', 'Not specified')}
        - Gender: {patient_info.get('gender', 'Not specified')}
        """
        
        context += f"""
        
        NEW FOLLOW-UP QUESTION: {new_question}
        
        Please provide a helpful, specific answer to the patient's follow-up question based on the previous consultation context. Include:
        
        1. Direct answer to their question
        2. Any additional relevant advice
        3. When to seek medical attention if applicable
        4. Safety reminders and medical disclaimers
        """
        
        return context
    
    def _format_followup_response(self, ai_response, question):
        """Format follow-up response"""
        return {
            'question': question,
            'answer': ai_response,
            'timestamp': 'now',
            'type': 'followup'
        }
    
    def _fallback_followup_response(self, question):
        """Provide fallback response for follow-up questions"""
        return {
            'question': question,
            'answer': "I'm sorry, I'm currently unable to provide a detailed answer to your follow-up question. Please consult with a healthcare professional for personalized medical advice regarding your symptoms and treatment options.",
            'timestamp': 'now',
            'type': 'followup'
        }

    def _fallback_response(self):
        """Provide fallback response when AI service fails"""
        return {
            'possible_causes': [
                'Viral upper respiratory infection (common cold)',
                'Seasonal allergies',
                'Mild bacterial infection'
            ],
            'remedies': [
                'Rest and stay hydrated',
                'Use a humidifier or breathe steam',
                'Gargle with warm salt water',
                'Take plenty of fluids'
            ],
            'otc_suggestions': [
                'Ibuprofen (200-400mg) for pain relief',
                'Throat lozenges for sore throat',
                'Decongestant nasal spray (short-term use)',
                'Vitamin C supplements'
            ],
            'urgency': 'Low',
            'seek_care': 'Seek medical attention if symptoms worsen or persist beyond 7-10 days.',
            'full_response': 'AI analysis temporarily unavailable. Basic recommendations provided. Please consult a healthcare professional for personalized medical advice.'
        }