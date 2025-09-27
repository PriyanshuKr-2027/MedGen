// Main JavaScript functionality for TeleMed AI

// Global variables
window.telemed = {
    currentUser: null,
    notifications: [],
    settings: {
        voiceEnabled: true,
        notificationsEnabled: true
    }
};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Check for browser compatibility
    checkBrowserCompatibility();
    
    // Initialize voice services if available
    initializeVoiceServices();
    
    // Set up event listeners
    setupEventListeners();
    
    // Initialize notification system
    initializeNotifications();
    
    // Auto-hide flash messages
    autoHideFlashMessages();
}

function checkBrowserCompatibility() {
    const features = {
        webrtc: !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia),
        speechRecognition: !!(window.SpeechRecognition || window.webkitSpeechRecognition),
        speechSynthesis: !!window.speechSynthesis,
        webAudio: !!(window.AudioContext || window.webkitAudioContext)
    };
    
    window.telemed.browserSupport = features;
    
    if (!features.webrtc) {
        console.warn('WebRTC not supported - video calls may not work');
    }
    
    if (!features.speechRecognition) {
        console.warn('Speech Recognition not supported - voice input may not work');
    }
}

function initializeVoiceServices() {
    if (window.telemed.browserSupport.speechRecognition) {
        window.speechToText = new SpeechToTextClient();
    }
    
    if (window.telemed.browserSupport.speechSynthesis) {
        window.textToSpeech = new TextToSpeechClient();
    }
}

function setupEventListeners() {
    // Language toggle functionality
    setupLanguageToggle();
    
    // Emergency call button
    setupEmergencyCall();
    
    // Form validation
    setupFormValidation();
}

function initializeNotifications() {
    // Request notification permission if supported
    if ('Notification' in window) {
        if (Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }
    
    // Set up service worker for push notifications (future enhancement)
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(registration => console.log('SW registered'))
            .catch(error => console.log('SW registration failed'));
    }
}

function autoHideFlashMessages() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100%)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
}

// Notification system
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm ${getNotificationClass(type)}`;
    notification.innerHTML = `
        <div class="flex items-center">
            <i class="fas ${getNotificationIcon(type)} mr-3"></i>
            <span class="flex-1">${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-3 text-lg">&times;</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }
    }, duration);
    
    // Browser notification
    if (Notification.permission === 'granted' && window.telemed.settings.notificationsEnabled) {
        new Notification('TeleMed AI', {
            body: message,
            icon: '/static/images/logo.png'
        });
    }
}

function getNotificationClass(type) {
    const classes = {
        success: 'bg-green-100 text-green-800 border border-green-200',
        error: 'bg-red-100 text-red-800 border border-red-200',
        warning: 'bg-yellow-100 text-yellow-800 border border-yellow-200',
        info: 'bg-blue-100 text-blue-800 border border-blue-200'
    };
    return classes[type] || classes.info;
}

function getNotificationIcon(type) {
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    return icons[type] || icons.info;
}

// Modal management
function closeAllModals() {
    const modals = document.querySelectorAll('.fixed.inset-0');
    modals.forEach(modal => {
        if (modal.classList.contains('flex')) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }
    });
}

// Network status handlers
function handleOnlineStatus() {
    showNotification('Connection restored', 'success');
    document.body.classList.remove('offline');
}

function handleOfflineStatus() {
    showNotification('Connection lost - some features may not work', 'warning');
    document.body.classList.add('offline');
}

// Utility functions
function formatTime(date) {
    return date.toLocaleTimeString('en-US', { 
        hour12: false, 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
    });
}

function formatDate(date) {
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// API helpers
async function apiCall(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const config = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(endpoint, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'API call failed');
        }
        
        return data;
    } catch (error) {
        console.error('API call error:', error);
        showNotification('Network error: ' + error.message, 'error');
        throw error;
    }
}

// Form validation helpers
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^\+?[\d\s\-\(\)]+$/;
    return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
}



// Language Toggle
function setupLanguageToggle() {
    const languageToggle = document.getElementById('languageToggle');
    const languageDropdown = document.getElementById('languageDropdown');
    const currentLang = document.getElementById('currentLang');
    const langOptions = document.querySelectorAll('.lang-option');

    if (languageToggle && languageDropdown) {
        // Toggle dropdown
        languageToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            languageDropdown.classList.toggle('hidden');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!languageToggle.contains(e.target) && !languageDropdown.contains(e.target)) {
                languageDropdown.classList.add('hidden');
            }
        });

        // Handle language selection
        langOptions.forEach(option => {
            option.addEventListener('click', function(e) {
                e.preventDefault();
                const selectedLang = this.getAttribute('data-lang');
                
                // Update current language display
                if (currentLang) {
                    currentLang.textContent = selectedLang.toUpperCase();
                }
                
                // Close dropdown
                languageDropdown.classList.add('hidden');
                
                // Change language using translation manager
                if (window.translationManager) {
                    window.translationManager.changeLanguage(selectedLang);
                    showNotification('Language changed to ' + (selectedLang === 'hi' ? 'Hindi' : 'English'), 'info', 2000);
                } else {
                    localStorage.setItem('selectedLanguage', selectedLang);
                    showNotification('Language preference saved', 'info', 2000);
                }
            });
        });

        // Initialize current language display
        const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
        if (currentLang) {
            currentLang.textContent = savedLanguage.toUpperCase();
        }
    }
    
    // Clean up any old dark mode settings
    localStorage.removeItem('theme');
}

// Emergency Call
function setupEmergencyCall() {
    // Emergency call functionality is handled in layout.html
    // This function can be extended for additional emergency features
}

// Form Validation
function setupFormValidation() {
    // Add real-time form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const isValid = value !== '' && (
        type !== 'email' || validateEmail(value)
    ) && (
        type !== 'tel' || validatePhone(value)
    );
    
    if (isValid) {
        field.classList.remove('border-red-500');
        field.classList.add('border-green-500');
    } else {
        field.classList.remove('border-green-500');
        field.classList.add('border-red-500');
    }
    
    return isValid;
}

// Loading states
function showLoading(element) {
    const originalContent = element.innerHTML;
    element.dataset.originalContent = originalContent;
    element.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Loading...';
    element.disabled = true;
}

function hideLoading(element) {
    element.innerHTML = element.dataset.originalContent || 'Submit';
    element.disabled = false;
    delete element.dataset.originalContent;
}

// Export for global use
window.telemed.utils = {
    showNotification,
    closeAllModals,
    formatTime,
    formatDate,
    debounce,
    throttle,
    apiCall,
    validateEmail,
    validatePhone,
    showLoading,
    hideLoading
};