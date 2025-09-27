// Multilanguage Translation System for TeleMed AI

class TranslationManager {
    constructor() {
        this.currentLanguage = localStorage.getItem('telemed_language') || 'en';
        this.translations = {
            en: {
                // Navigation
                'logout': 'Logout',
                'online': 'Online',
                
                // Common UI Elements
                'loading': 'Loading...',
                'submit': 'Submit',
                'cancel': 'Cancel',
                'save': 'Save',
                'edit': 'Edit',
                'delete': 'Delete',
                'back': 'Back',
                'next': 'Next',
                'previous': 'Previous',
                'search': 'Search',
                'filter': 'Filter',
                'clear': 'Clear',
                'close': 'Close',
                'yes': 'Yes',
                'no': 'No',
                'ok': 'OK',
                
                // Dashboard
                'welcome': 'Welcome',
                'dashboard': 'Dashboard',
                'profile': 'Profile',
                'settings': 'Settings',
                'notifications': 'Notifications',
                
                // Patient Dashboard
                'patient_dashboard': 'Patient Dashboard',
                'book_consultation': 'Book Consultation',
                'view_history': 'View History',
                'ai_symptom_checker': 'AI Symptom Checker',
                'emergency_call': 'Emergency Call',
                'upcoming_appointments': 'Upcoming Appointments',
                'recent_consultations': 'Recent Consultations',
                'health_metrics': 'Health Metrics',
                'start_reporting': 'Start Reporting',
                'connect_now': 'Connect Now',
                'learn_more': 'Learn More',
                
                // Doctor Dashboard
                'doctor_dashboard': 'Doctor Dashboard',
                'patient_queue': 'Patient Queue',
                'schedule': 'Schedule',
                'patient_records': 'Patient Records',
                'video_consultation': 'Video Consultation',
                'pending_consultations': 'Pending Consultations',
                'today_schedule': 'Today\'s Schedule',
                
                // Admin Dashboard
                'admin_dashboard': 'Admin Dashboard',
                'manage_users': 'Manage Users',
                'system_stats': 'System Statistics',
                'reports': 'Reports',
                'total_users': 'Total Users',
                'active_consultations': 'Active Consultations',
                'system_health': 'System Health',
                
                // Symptom Checker
                'symptom_analysis': 'AI Symptom Analysis',
                'describe_symptoms': 'Describe your symptoms for personalized health insights',
                'type_symptoms': 'Type your symptoms here...',
                'voice_input': 'Voice Input',
                'ai_analysis': 'AI Analysis',
                'possible_causes': 'Possible Causes',
                'recommendations': 'Recommendations',
                'severity': 'Severity',
                'consult_doctor': 'Consult a Doctor',
                'emergency_warning': 'If this is an emergency, please call emergency services immediately',
                
                // Consultation
                'book_appointment': 'Book Appointment',
                'consultation_history': 'Consultation History',
                'prescription': 'Prescription',
                'diagnosis': 'Diagnosis',
                'treatment_plan': 'Treatment Plan',
                'follow_up': 'Follow-up',
                'doctor_notes': 'Doctor Notes',
                'patient_info': 'Patient Information',
                
                // Voice/Audio
                'listening': 'Listening...',
                'click_to_speak': 'Click to speak',
                'microphone_access_denied': 'Microphone access denied. Please enable microphone permissions.',
                'voice_not_supported': 'Voice input is not available on this device.',
                'speak_now': 'Speak clearly about your symptoms',
                'voice_input_stopped': 'Voice input stopped',
                'stop': 'Stop',
                'use_text': 'Use Text',
                
                // Forms
                'username': 'Username',
                'password': 'Password',
                'email': 'Email',
                'phone': 'Phone',
                'name': 'Name',
                'age': 'Age',
                'gender': 'Gender',
                'user_id': 'User ID',
                'select_role': 'Select Role',
                'sign_in': 'Sign In',
                'quick_demo_access': 'Quick Demo Access:',
                'demo_patient': 'Demo Patient',
                'demo_doctor': 'Demo Doctor',
                'demo_admin': 'Demo Admin',
                'address': 'Address',
                'medical_history': 'Medical History',
                'current_medications': 'Current Medications',
                'allergies': 'Allergies',
                
                // Messages
                'success': 'Success',
                'error': 'Error',
                'warning': 'Warning',
                'info': 'Information',
                'connection_lost': 'Connection lost - some features may not work',
                'connection_restored': 'Connection restored',
                'processing': 'Processing...',
                'please_wait': 'Please wait...',
                
                // Time/Date
                'today': 'Today',
                'yesterday': 'Yesterday',
                'tomorrow': 'Tomorrow',
                'this_week': 'This Week',
                'last_week': 'Last Week',
                'this_month': 'This Month',
                'last_month': 'Last Month',
                
                // Emergency Call
                'emergency_call': 'Emergency Call 108',
                'confirm_emergency_call': 'Are you sure you want to call emergency services (108)?',
                'emergency_number_fallback': 'Please dial 108 for emergency services.',
                
                // Disease Information
                'know_your_disease': 'Know Your Disease',
                'search_learn_diseases': 'Search and learn about medical conditions and diseases',
                'search_disease_info': 'Search for comprehensive information about medical conditions',
                'search_disease': 'Search for a Disease',
                'search_placeholder': 'Enter disease name (e.g., Diabetes, Hypertension, Asthma)',
                'common_diseases': 'Common Diseases & Conditions',
                'loading_disease_info': 'Loading disease information...',
                'medical_disclaimer': 'This information is for educational purposes only. Always consult a healthcare professional for medical advice.',
                'overview': 'Overview',
                'symptoms': 'Symptoms',
                'causes': 'Causes',
                'treatment': 'Treatment',
                'home_remedies': 'Home Remedies',
                'otc_medications': 'OTC Medications',
                'prevention': 'Prevention',
                'when_to_see_doctor': 'When to See a Doctor',
                'connect_doctor': 'Connect with Doctor',
                'report_symptoms': 'Report Symptoms',
                'search_again': 'Search Again',
                'error_loading': 'Error loading disease information. Please try again.',
                'back_to_dashboard': 'Back to Dashboard',
                
                // Disease Categories
                'cardiovascular': 'Cardiovascular',
                'respiratory': 'Respiratory',
                'endocrine': 'Endocrine',
                'infectious': 'Infectious',
                'gastrointestinal': 'Gastrointestinal',
                'mental_health': 'Mental Health',
                'dermatological': 'Dermatological',
                'musculoskeletal': 'Musculoskeletal',
                
                // Common Diseases
                'hypertension': 'Hypertension',
                'heart_disease': 'Heart Disease',
                'arrhythmia': 'Arrhythmia',
                'asthma': 'Asthma',
                'copd': 'COPD',
                'pneumonia': 'Pneumonia',
                'diabetes': 'Diabetes',
                'thyroid_disorders': 'Thyroid Disorders',
                'obesity': 'Obesity',
                'common_cold': 'Common Cold',
                'influenza': 'Influenza',
                'covid19': 'COVID-19',
                'gerd': 'GERD',
                'ibs': 'IBS',
                'peptic_ulcer': 'Peptic Ulcer',
                'anxiety': 'Anxiety',
                'depression': 'Depression',
                'insomnia': 'Insomnia',
                'eczema': 'Eczema',
                'psoriasis': 'Psoriasis',
                'acne': 'Acne',
                'arthritis': 'Arthritis',
                'osteoporosis': 'Osteoporosis',
                'back_pain': 'Back Pain',
            },
            hi: {
                // Navigation
                'logout': 'लॉगआउट',
                'online': 'ऑनलाइन',
                
                // Common UI Elements
                'loading': 'लोड हो रहा है...',
                'submit': 'प्रस्तुत करें',
                'cancel': 'रद्द करें',
                'save': 'सेव करें',
                'edit': 'संपादित करें',
                'delete': 'हटाएं',
                'back': 'वापस',
                'next': 'आगे',
                'previous': 'पिछला',
                'search': 'खोजें',
                'filter': 'फिल्टर',
                'clear': 'साफ़ करें',
                'close': 'बंद करें',
                'yes': 'हाँ',
                'no': 'नहीं',
                'ok': 'ठीक है',
                
                // Dashboard
                'welcome': 'स्वागत है',
                'dashboard': 'डैशबोर्ड',
                'profile': 'प्रोफ़ाइल',
                'settings': 'सेटिंग्स',
                'notifications': 'सूचनाएं',
                
                // Patient Dashboard
                'patient_dashboard': 'रोगी डैशबोर्ड',
                'book_consultation': 'परामर्श बुक करें',
                'view_history': 'इतिहास देखें',
                'ai_symptom_checker': 'AI लक्षण जांचकर्ता',
                'emergency_call': 'आपातकालीन कॉल',
                'upcoming_appointments': 'आगामी अपॉइंटमेंट',
                'recent_consultations': 'हाल की परामर्श',
                'health_metrics': 'स्वास्थ्य मेट्रिक्स',
                'start_reporting': 'रिपोर्टिंग शुरू करें',
                'connect_now': 'अभी कनेक्ट करें',
                'learn_more': 'और जानें',
                
                // Doctor Dashboard
                'doctor_dashboard': 'डॉक्टर डैशबोर्ड',
                'patient_queue': 'रोगी कतार',
                'schedule': 'कार्यक्रम',
                'patient_records': 'रोगी रिकॉर्ड',
                'video_consultation': 'वीडियो परामर्श',
                'pending_consultations': 'लंबित परामर्श',
                'today_schedule': 'आज का कार्यक्रम',
                
                // Admin Dashboard
                'admin_dashboard': 'व्यवस्थापक डैशबोर्ड',
                'manage_users': 'उपयोगकर्ता प्रबंधन',
                'system_stats': 'सिस्टम आंकड़े',
                'reports': 'रिपोर्ट',
                'total_users': 'कुल उपयोगकर्ता',
                'active_consultations': 'सक्रिय परामर्श',
                'system_health': 'सिस्टम स्वास्थ्य',
                
                // Symptom Checker
                'symptom_analysis': 'AI लक्षण विश्लेषण',
                'describe_symptoms': 'व्यक्तिगत स्वास्थ्य जानकारी के लिए अपने लक्षणों का वर्णन करें',
                'type_symptoms': 'यहाँ अपने लक्षण लिखें...',
                'voice_input': 'आवाज़ इनपुट',
                'ai_analysis': 'AI विश्लेषण',
                'possible_causes': 'संभावित कारण',
                'recommendations': 'सिफारिशें',
                'severity': 'गंभीरता',
                'consult_doctor': 'डॉक्टर से सलाह लें',
                'emergency_warning': 'यदि यह आपातकाल है, तो कृपया तुरंत आपातकालीन सेवाओं को कॉल करें',
                
                // Consultation
                'book_appointment': 'अपॉइंटमेंट बुक करें',
                'consultation_history': 'परामर्श इतिहास',
                'prescription': 'नुस्खा',
                'diagnosis': 'निदान',
                'treatment_plan': 'उपचार योजना',
                'follow_up': 'फॉलो-अप',
                'doctor_notes': 'डॉक्टर के नोट्स',
                'patient_info': 'रोगी की जानकारी',
                
                // Voice/Audio
                'listening': 'सुन रहा है...',
                'click_to_speak': 'बोलने के लिए क्लिक करें',
                'microphone_access_denied': 'माइक्रोफ़ोन एक्सेस अस्वीकृत। कृपया माइक्रोफ़ोन अनुमतियां सक्षम करें।',
                'voice_not_supported': 'इस डिवाइस पर आवाज़ इनपुट उपलब्ध नहीं है।',
                'speak_now': 'अपने लक्षणों के बारे में स्पष्ट रूप से बोलें',
                'voice_input_stopped': 'आवाज़ इनपुट बंद',
                'stop': 'रुकें',
                'use_text': 'टेक्स्ट का उपयोग करें',
                
                // Forms
                'username': 'उपयोगकर्ता नाम',
                'password': 'पासवर्ड',
                'email': 'ईमेल',
                'phone': 'फ़ोन',
                'name': 'नाम',
                'age': 'उम्र',
                'gender': 'लिंग',
                'user_id': 'उपयोगकर्ता आईडी',
                'select_role': 'भूमिका चुनें',
                'sign_in': 'साइन इन',
                'quick_demo_access': 'त्वरित डेमो एक्सेस:',
                'demo_patient': 'डेमो मरीज़',
                'demo_doctor': 'डेमो डॉक्टर',
                'demo_admin': 'डेमो एडमिन',
                'address': 'पता',
                'medical_history': 'चिकित्सा इतिहास',
                'current_medications': 'वर्तमान दवाएं',
                'allergies': 'एलर्जी',
                
                // Messages
                'success': 'सफलता',
                'error': 'त्रुटि',
                'warning': 'चेतावनी',
                'info': 'जानकारी',
                'connection_lost': 'कनेक्शन खो गया - कुछ सुविधाएं काम नहीं कर सकती हैं',
                'connection_restored': 'कनेक्शन बहाल',
                'processing': 'प्रोसेसिंग...',
                'please_wait': 'कृपया प्रतीक्षा करें...',
                
                // Time/Date
                'today': 'आज',
                'yesterday': 'कल',
                'tomorrow': 'कल',
                'this_week': 'इस सप्ताह',
                'last_week': 'पिछला सप्ताह',
                'this_month': 'इस महीने',
                'last_month': 'पिछला महीना',
                
                // Emergency Call
                'emergency_call': 'आपातकालीन कॉल 108',
                'confirm_emergency_call': 'क्या आप वाकई आपातकालीन सेवाओं (108) को कॉल करना चाहते हैं?',
                'emergency_number_fallback': 'कृपया आपातकालीन सेवाओं के लिए 108 डायल करें।',
                
                // Disease Information
                'know_your_disease': 'अपनी बीमारी को जानें',
                'search_learn_diseases': 'चिकित्सा स्थितियों और बीमारियों के बारे में खोजें और जानें',
                'search_disease_info': 'चिकित्सा स्थितियों के बारे में व्यापक जानकारी खोजें',
                'search_disease': 'बीमारी खोजें',
                'search_placeholder': 'बीमारी का नाम दर्ज करें (जैसे, मधुमेह, उच्च रक्तचाप, अस्थमा)',
                'common_diseases': 'सामान्य बीमारियां और स्थितियां',
                'loading_disease_info': 'बीमारी की जानकारी लोड हो रही है...',
                'medical_disclaimer': 'यह जानकारी केवल शैक्षिक उद्देश्यों के लिए है। चिकित्सा सलाह के लिए हमेशा स्वास्थ्य पेशेवर से सलाह लें।',
                'overview': 'अवलोकन',
                'symptoms': 'लक्षण',
                'causes': 'कारण',
                'treatment': 'उपचार',
                'home_remedies': 'घरेलू उपचार',
                'otc_medications': 'बिना पर्चे की दवाएं',
                'prevention': 'रोकथाम',
                'when_to_see_doctor': 'डॉक्टर को कब दिखाना चाहिए',
                'connect_doctor': 'डॉक्टर से जुड़ें',
                'report_symptoms': 'लक्षण बताएं',
                'search_again': 'फिर से खोजें',
                'error_loading': 'बीमारी की जानकारी लोड करने में त्रुटि। कृपया पुनः प्रयास करें।',
                'back_to_dashboard': 'डैशबोर्ड पर वापस जाएं',
                
                // Disease Categories
                'cardiovascular': 'हृदय संबंधी',
                'respiratory': 'श्वसन संबंधी',
                'endocrine': 'अंतःस्रावी',
                'infectious': 'संक्रामक',
                'gastrointestinal': 'पाचन संबंधी',
                'mental_health': 'मानसिक स्वास्थ्य',
                'dermatological': 'त्वचा संबंधी',
                'musculoskeletal': 'मांसपेशियों और हड्डियों संबंधी',
                
                // Common Diseases
                'hypertension': 'उच्च रक्तचाप',
                'heart_disease': 'हृदय रोग',
                'arrhythmia': 'अतालता',
                'asthma': 'दमा',
                'copd': 'सीओपीडी',
                'pneumonia': 'निमोनिया',
                'diabetes': 'मधुमेह',
                'thyroid_disorders': 'थायराइड विकार',
                'obesity': 'मोटापा',
                'common_cold': 'सामान्य सर्दी',
                'influenza': 'इन्फ्लूएंजा',
                'covid19': 'कोविड-19',
                'gerd': 'जीईआरडी',
                'ibs': 'आईबीएस',
                'peptic_ulcer': 'पेप्टिक अल्सर',
                'anxiety': 'चिंता',
                'depression': 'अवसाद',
                'insomnia': 'अनिद्रा',
                'eczema': 'एक्जिमा',
                'psoriasis': 'सोरायसिस',
                'acne': 'मुंहासे',
                'arthritis': 'गठिया',
                'osteoporosis': 'ऑस्टियोपोरोसिस',
                'back_pain': 'पीठ दर्द',
            }
        };
        
        this.init();
    }
    
    init() {
        this.updateLanguageDisplay();
        this.translatePage();
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Main navigation language toggle
        this.setupLanguageToggle('languageToggle', 'languageDropdown', 'currentLang', '.lang-option');
        
        // Floating language toggle for public pages
        this.setupLanguageToggle('floatingLanguageToggle', 'floatingLanguageDropdown', 'floatingCurrentLang', '.floating-lang-option');
    }
    
    setupLanguageToggle(toggleId, dropdownId, currentLangId, optionSelector) {
        const languageToggle = document.getElementById(toggleId);
        const languageDropdown = document.getElementById(dropdownId);
        const currentLangEl = document.getElementById(currentLangId);
        
        if (languageToggle && languageDropdown) {
            languageToggle.addEventListener('click', (e) => {
                e.stopPropagation();
                languageDropdown.classList.toggle('hidden');
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', (e) => {
                if (!languageToggle.contains(e.target)) {
                    languageDropdown.classList.add('hidden');
                }
            });
            
            // Language option selection
            const langOptions = document.querySelectorAll(optionSelector);
            langOptions.forEach(option => {
                option.addEventListener('click', (e) => {
                    const selectedLang = e.target.closest(optionSelector).dataset.lang;
                    this.setLanguage(selectedLang);
                    languageDropdown.classList.add('hidden');
                });
            });
        }
        
        // Update current language display
        if (currentLangEl) {
            currentLangEl.textContent = this.currentLanguage.toUpperCase();
        }
    }
    
    setLanguage(lang) {
        if (this.translations[lang]) {
            this.currentLanguage = lang;
            localStorage.setItem('telemed_language', lang);
            this.updateLanguageDisplay();
            this.translatePage();
            
            // Update HTML lang attribute
            document.documentElement.lang = lang;
            
            // Trigger custom event for other components
            document.dispatchEvent(new CustomEvent('languageChanged', {
                detail: { language: lang }
            }));
        }
    }
    
    updateLanguageDisplay() {
        const currentLangEl = document.getElementById('currentLang');
        const floatingCurrentLangEl = document.getElementById('floatingCurrentLang');
        
        if (currentLangEl) {
            currentLangEl.textContent = this.currentLanguage.toUpperCase();
        }
        if (floatingCurrentLangEl) {
            floatingCurrentLangEl.textContent = this.currentLanguage.toUpperCase();
        }
    }
    
    translatePage() {
        const elements = document.querySelectorAll('[data-translate]');
        elements.forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.translate(key);
            
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                if (element.type === 'submit' || element.type === 'button') {
                    element.value = translation;
                } else {
                    element.placeholder = translation;
                }
            } else {
                element.textContent = translation;
            }
        });
        
        // Handle placeholder translations
        const placeholderElements = document.querySelectorAll('[data-translate-placeholder]');
        placeholderElements.forEach(element => {
            const key = element.getAttribute('data-translate-placeholder');
            const translation = this.translate(key);
            element.placeholder = translation;
        });
    }
    
    translate(key, defaultText = null) {
        const translation = this.translations[this.currentLanguage][key] || 
                          this.translations['en'][key] || 
                          defaultText || 
                          key;
        return translation;
    }
    
    getCurrentLanguage() {
        return this.currentLanguage;
    }
    
    changeLanguage(lang) {
        if (this.translations[lang]) {
            this.currentLanguage = lang;
            localStorage.setItem('telemed_language', lang);
            localStorage.setItem('selectedLanguage', lang);
            this.updatePageTranslations();
            
            // Update language display in navigation
            const currentLangElements = document.querySelectorAll('#currentLang, #formCurrentLang');
            currentLangElements.forEach(element => {
                if (element) {
                    element.textContent = lang.toUpperCase();
                }
            });
            
            // Trigger custom event for other components
            document.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
        }
    }
    
    addTranslations(lang, translations) {
        if (!this.translations[lang]) {
            this.translations[lang] = {};
        }
        Object.assign(this.translations[lang], translations);
    }
}

// Initialize translation manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.translationManager = new TranslationManager();
    
    // Sync with saved language preference
    const savedLanguage = localStorage.getItem('selectedLanguage') || localStorage.getItem('telemed_language') || 'en';
    if (savedLanguage !== window.translationManager.getCurrentLanguage()) {
        window.translationManager.changeLanguage(savedLanguage);
    }
    
    // Update current language display
    const currentLangElements = document.querySelectorAll('#currentLang, #formCurrentLang');
    currentLangElements.forEach(element => {
        if (element) {
            element.textContent = savedLanguage.toUpperCase();
        }
    });
});

// Export for global use
window.TranslationManager = TranslationManager;