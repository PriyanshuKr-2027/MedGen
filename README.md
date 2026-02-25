# MedGen - AI-Powered Telemedicine Platform

<div align="center">
  <img src="AI Telemedicine Platform.png" alt="MedGen Logo" width="400">
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
  [![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
  [![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
  [![TypeScript](https://img.shields.io/badge/TypeScript-5.5.3-blue.svg)](https://typescriptlang.org/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

## 🏥 Overview

MedGen is a comprehensive AI-powered telemedicine platform designed to bridge healthcare accessibility gaps in rural and underserved areas. Built for the Smart India Hackathon, it combines cutting-edge AI technology with practical telemedicine features to provide multilingual, voice-enabled healthcare consultations.

### 🌟 Key Features

- **🤖 AI-Powered Medical Analysis** - DeepSeek AI integration for intelligent symptom analysis
- **🗣️ Voice-Enabled Interface** - Speech recognition and text-to-speech capabilities
- **🌐 Multilingual Support** - Full English and Hindi translation (500+ keys)
- **👨‍⚕️ Real-time Doctor Consultations** - WebRTC-powered video conferencing
- **📱 Responsive Design** - Mobile-first approach with TailwindCSS
- **🏥 Comprehensive Disease Database** - 24+ conditions across 8 medical categories
- **🚨 Emergency Response System** - Critical case detection and routing
- **📊 Patient History Management** - Complete medical record tracking

## 🏗️ Architecture

### Technology Stack

**Backend:**
- Flask 3.0.0 (Python)
- SQLAlchemy with SQLite/PostgreSQL
- OpenRouter API with DeepSeek Chat model
- Flask-CORS, Flask-Migrate

**Frontend:**
- React 18.3.1 with TypeScript
- Vite build system
- TailwindCSS 3.4.1
- Lucide React icons

**Voice & Communication:**
- Web Speech API
- WebRTC for video calls
- SpeechRecognition library
- pyttsx3 for text-to-speech

### Project Structure

```
project/
├── run.py                 # Application entry point
├── requirements.txt       # Python dependencies
├── package.json          # Node.js dependencies
├── app/
│   ├── __init__.py       # Flask app factory
│   ├── config.py         # Configuration management
│   ├── models.py         # Database models
│   ├── utils.py          # Authentication utilities
│   ├── routes/           # API endpoints
│   │   ├── auth_routes.py
│   │   ├── patient_routes.py
│   │   ├── doctor_routes.py
│   │   ├── admin_routes.py
│   │   ├── consultation_routes.py
│   │   ├── voice_routes.py
│   │   └── connect_routes.py
│   ├── services/         # Business logic
│   │   ├── ai_service.py
│   │   └── voice_service.py
│   ├── static/           # Frontend assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/        # HTML templates
├── src/                  # React components
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
└── instance/            # Database files
    └── telemedicine.db
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PriyanshuKr-2027/MedGen.git
   cd MedGen/project
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node.js dependencies**
   ```bash
   npm install
   ```

5. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key
   DATABASE_URL=sqlite:///instance/telemedicine.db
   ```

6. **Initialize Database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. **Run the Application**
   
   **Backend (Flask):**
   ```bash
   python run.py
   ```
   
   **Frontend (Vite dev server):**
   ```bash
   npm run dev
   ```

8. **Access the Application**
   - Backend: http://localhost:5000
   - Frontend: http://localhost:5173

## 👥 User Roles & Demo Accounts

### Demo Credentials

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| Patient | `patient` | `patient123` | Patient dashboard, consultations |
| Doctor | `doctor` | `doctor123` | Doctor dashboard, patient management |
| Admin | `admin` | `admin123` | System administration, analytics |

### Role-Based Features

**Patient:**
- Symptom reporting with AI analysis
- Disease information lookup
- Doctor consultation booking
- Medical history tracking
- Voice-enabled interactions

**Doctor:**
- Patient consultation management
- Medical record review
- Treatment prescription
- Follow-up scheduling
- Video call capabilities

**Admin:**
- User management
- System analytics
- Platform configuration
- Emergency case monitoring

## 🤖 AI Integration

### DeepSeek AI Features

- **Symptom Analysis**: Intelligent assessment of patient symptoms
- **Disease Information**: Comprehensive medical knowledge base
- **Treatment Recommendations**: Evidence-based suggestions
- **Urgency Classification**: Critical case identification
- **Multilingual Processing**: English and Hindi support

### AI Service Architecture

```python
# Example AI service usage
from app.services.ai_service import AIService

service = AIService()
analysis = service.analyze_symptoms("fever, headache, body ache")
disease_info = service.get_disease_information("hypertension")
```

## 🌐 Multilingual Support

Complete internationalization with:
- **500+ Translation Keys**
- **Dynamic Language Switching**
- **Voice Support in Multiple Languages**
- **Cultural Adaptation**

Supported Languages:
- 🇬🇧 English
- 🇮🇳 Hindi (हिंदी)

## 📱 API Documentation

### Authentication Endpoints
```
POST /auth/login          # User login
POST /auth/register       # User registration
GET  /auth/logout         # User logout
```

### Patient Endpoints
```
GET  /patient/dashboard   # Patient dashboard
POST /patient/symptoms    # Submit symptoms
GET  /patient/history     # Medical history
GET  /patient/disease-info # Disease information
```

### Doctor Endpoints
```
GET  /doctor/dashboard    # Doctor dashboard
GET  /doctor/patients     # Patient list
POST /doctor/prescription # Create prescription
```

### Consultation Endpoints
```
POST /consultation/create    # Create consultation
GET  /consultation/:id       # Get consultation details
PUT  /consultation/:id/status # Update consultation status
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `development` |
| `SECRET_KEY` | Flask secret key | Required |
| `OPENROUTER_API_KEY` | AI service API key | Required |
| `DATABASE_URL` | Database connection | `sqlite:///instance/telemedicine.db` |

### AI Service Configuration

```python
# app/config.py
class Config:
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    AI_MODEL = 'deepseek/deepseek-chat'
    MAX_TOKENS = 1000
    TEMPERATURE = 0.3
```

## 🧪 Testing

Run the test suite:

```bash
# Python tests
python -m pytest

# Frontend tests
npm test

# Specific test files
python test_clarifying_questions.py
python test_followup.py
```

## 🚀 Deployment

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

### Production Configuration

```bash
# Build frontend for production
npm run build

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 run:app
```

## 📊 Database Schema

### Core Models

```sql
-- Users table
User {
  id: Primary Key
  username: Unique String
  password: Hashed String
  role: Enum (patient, doctor, admin)
  name, email, phone: String
  created_at: DateTime
}

-- Consultations table
Consultation {
  id: Primary Key
  patient_id: Foreign Key (User)
  doctor_id: Foreign Key (User)
  symptoms: Text
  ai_analysis: JSON
  severity: Enum (mild, moderate, critical)
  status: Enum (pending, reviewed, completed)
  created_at, updated_at: DateTime
}

-- Treatments table
Treatment {
  id: Primary Key
  consultation_id: Foreign Key (Consultation)
  doctor_id: Foreign Key (User)
  prescription: Text
  notes: Text
  follow_up_date: DateTime
}
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for React components
- Write comprehensive tests
- Update documentation
- Ensure mobile responsiveness

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Smart India Hackathon

This project was developed for the Smart India Hackathon 2024, addressing the challenge of healthcare accessibility in rural and underserved areas through innovative AI-powered telemedicine solutions.

### Problem Statement
Bridging healthcare accessibility gaps through:
- AI-powered medical consultations
- Multilingual support for diverse populations
- Emergency response integration
- Comprehensive patient management

## 📞 Support

For support and questions:
- **GitHub Issues**: [Create an issue](https://github.com/PriyanshuKr-2027/MedGen/issues)
- **Documentation**: [Wiki](https://github.com/PriyanshuKr-2027/MedGen/wiki)

## 🙏 Acknowledgments

- **DeepSeek AI** for advanced medical analysis capabilities
- **OpenRouter** for API infrastructure
- **Smart India Hackathon** for the opportunity to innovate
- **Open source community** for the amazing tools and libraries

---

<div align="center">
  <p>Built with ❤️ for accessible healthcare</p>
  <p>© 2024 MedGen Team. All rights reserved.</p>
</div>
