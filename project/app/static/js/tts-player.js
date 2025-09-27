// Text-to-Speech Player for TeleMed AI

class TextToSpeechClient {
    constructor() {
        this.synth = window.speechSynthesis;
        this.voices = [];
        this.defaultVoice = null;
        this.currentUtterance = null;
        this.isPlaying = false;
        
        this.initializeVoices();
    }
    
    initializeVoices() {
        if (!this.synth) {
            console.warn('Speech synthesis not supported');
            return;
        }
        
        // Load voices
        this.loadVoices();
        
        // Voices might not be loaded immediately
        if (speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = () => {
                this.loadVoices();
            };
        }
    }
    
    loadVoices() {
        this.voices = this.synth.getVoices();
        
        // Find a good default voice (prefer female, English)
        this.defaultVoice = this.voices.find(voice => 
            voice.lang.startsWith('en') && 
            (voice.name.toLowerCase().includes('female') || 
             voice.name.toLowerCase().includes('zira') ||
             voice.name.toLowerCase().includes('samantha'))
        ) || this.voices.find(voice => voice.lang.startsWith('en')) || this.voices[0];
        
        console.log('Available voices:', this.voices.length);
        console.log('Default voice:', this.defaultVoice?.name);
    }
    
    speak(text, options = {}) {
        return new Promise((resolve, reject) => {
            if (!this.synth) {
                // Fallback to server-side TTS
                this.serverSpeak(text, options).then(resolve).catch(reject);
                return;
            }
            
            if (!text || text.trim() === '') {
                reject(new Error('No text provided'));
                return;
            }
            
            // Stop any current speech
            this.stop();
            
            const utterance = new SpeechSynthesisUtterance(text);
            
            // Configure utterance
            utterance.voice = options.voice || this.defaultVoice;
            utterance.rate = options.rate || 0.9;
            utterance.pitch = options.pitch || 1.0;
            utterance.volume = options.volume || 0.8;
            utterance.lang = options.lang || 'en-US';
            
            // Event listeners
            utterance.onstart = () => {
                this.isPlaying = true;
                console.log('Speech started');
            };
            
            utterance.onend = () => {
                this.isPlaying = false;
                this.currentUtterance = null;
                console.log('Speech ended');
                resolve({ success: true });
            };
            
            utterance.onerror = (event) => {
                this.isPlaying = false;
                this.currentUtterance = null;
                console.error('Speech error:', event.error);
                reject(new Error(`Speech synthesis failed: ${event.error}`));
            };
            
            utterance.onpause = () => {
                console.log('Speech paused');
            };
            
            utterance.onresume = () => {
                console.log('Speech resumed');
            };
            
            this.currentUtterance = utterance;
            
            try {
                this.synth.speak(utterance);
            } catch (error) {
                this.isPlaying = false;
                this.currentUtterance = null;
                reject(error);
            }
        });
    }
    
    async serverSpeak(text, options = {}) {
        try {
            const response = await fetch('/voice/text-to-speech', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    text: text,
                    ...options 
                })
            });
            
            if (!response.ok) {
                throw new Error('Server TTS failed');
            }
            
            const result = await response.json();
            
            if (result.success && result.audio_url) {
                return this.playAudioFile(result.audio_url);
            } else {
                throw new Error(result.error || 'TTS generation failed');
            }
            
        } catch (error) {
            throw new Error(`Server TTS failed: ${error.message}`);
        }
    }
    
    playAudioFile(audioUrl) {
        return new Promise((resolve, reject) => {
            const audio = new Audio(audioUrl);
            
            audio.oncanplaythrough = () => {
                this.isPlaying = true;
                audio.play()
                    .then(() => resolve({ success: true }))
                    .catch(reject);
            };
            
            audio.onended = () => {
                this.isPlaying = false;
            };
            
            audio.onerror = () => {
                this.isPlaying = false;
                reject(new Error('Audio playback failed'));
            };
            
            audio.load();
        });
    }
    
    stop() {
        if (this.synth && this.isPlaying) {
            this.synth.cancel();
            this.isPlaying = false;
            this.currentUtterance = null;
        }
    }
    
    pause() {
        if (this.synth && this.isPlaying) {
            this.synth.pause();
        }
    }
    
    resume() {
        if (this.synth && this.currentUtterance) {
            this.synth.resume();
        }
    }
    
    getVoices() {
        return this.voices;
    }
    
    setDefaultVoice(voiceName) {
        const voice = this.voices.find(v => v.name === voiceName);
        if (voice) {
            this.defaultVoice = voice;
            return true;
        }
        return false;
    }
    
    // Speak with medical context (adjust speed, emphasize important parts)
    speakMedical(text, options = {}) {
        // Slower rate for medical information
        const medicalOptions = {
            rate: 0.8,
            pitch: 1.0,
            volume: 0.9,
            ...options
        };
        
        // Add pauses after important medical terms
        let processedText = text
            .replace(/\b(emergency|urgent|critical|severe)\b/gi, '$1... ')
            .replace(/\b(medication|dosage|treatment)\b/gi, '$1... ')
            .replace(/\./g, '... '); // Add pauses after sentences
        
        return this.speak(processedText, medicalOptions);
    }
    
    // Check if TTS is supported
    static isSupported() {
        return !!(window.speechSynthesis && window.SpeechSynthesisUtterance);
    }
    
    // Get supported languages
    getSupportedLanguages() {
        return [...new Set(this.voices.map(voice => voice.lang))];
    }
}

// TTS Helper Functions
class TTSHelper {
    static createSpeechButton(text, options = {}) {
        const button = document.createElement('button');
        button.innerHTML = '<i class="fas fa-volume-up"></i>';
        button.className = 'ml-2 p-1 text-gray-600 hover:text-indigo-600 transition-colors';
        button.title = 'Listen to this text';
        
        button.addEventListener('click', async () => {
            try {
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                button.disabled = true;
                
                await window.textToSpeech.speak(text, options);
                
            } catch (error) {
                console.error('TTS error:', error);
                window.telemed?.utils?.showNotification('Text-to-speech failed', 'error');
            } finally {
                button.innerHTML = '<i class="fas fa-volume-up"></i>';
                button.disabled = false;
            }
        });
        
        return button;
    }
    
    static addSpeechToElement(element, text = null) {
        const textContent = text || element.textContent.trim();
        if (textContent) {
            const button = TTSHelper.createSpeechButton(textContent);
            element.appendChild(button);
        }
    }
    
    // Add speech buttons to medical content
    static enhanceMedicalContent() {
        const selectors = [
            '.medical-analysis p',
            '.treatment-notes',
            '.prescription-text',
            '.symptom-description'
        ];
        
        selectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                if (!element.querySelector('.fa-volume-up')) {
                    TTSHelper.addSpeechToElement(element);
                }
            });
        });
    }
}

// Initialize TTS client
if (TextToSpeechClient.isSupported()) {
    window.textToSpeech = new TextToSpeechClient();
    console.log('Client-side TTS initialized');
} else {
    // Create a mock client that uses server-side TTS
    window.textToSpeech = {
        speak: async (text, options = {}) => {
            const response = await fetch('/voice/text-to-speech', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, ...options })
            });
            
            const result = await response.json();
            if (result.success && result.audio_url) {
                const audio = new Audio(result.audio_url);
                return new Promise((resolve, reject) => {
                    audio.onended = () => resolve({ success: true });
                    audio.onerror = reject;
                    audio.play();
                });
            }
            throw new Error(result.error || 'TTS failed');
        },
        stop: () => {},
        pause: () => {},
        resume: () => {}
    };
    console.log('Server-side TTS initialized');
}

// Auto-enhance medical content when page loads
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(TTSHelper.enhanceMedicalContent, 1000);
});

// Export helper
window.TTSHelper = TTSHelper;