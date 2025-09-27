// Speech-to-Text Client for TeleMed AI

class SpeechToTextClient {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.finalTranscript = '';
        this.interimTranscript = '';
        this.silenceTimer = null;
        this.silenceTimeout = 3000; // 3 seconds of silence before auto-stop
        this.hasReceivedSpeech = false;
        
        this.initializeRecognition();
    }
    
    initializeRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('Speech recognition not supported');
            this.recognition = null;
            return;
        }
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        // Configure recognition
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';
        this.recognition.maxAlternatives = 1;
        
        console.log('Speech recognition initialized successfully');
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        if (!this.recognition) return;
        
        this.recognition.onstart = () => {
            console.log('Speech recognition started');
            this.isListening = true;
            this.onStart && this.onStart();
        };
        
        this.recognition.onend = () => {
            console.log('Speech recognition ended');
            this.isListening = false;
            this.onEnd && this.onEnd();
        };
        
        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.isListening = false;
            this.onError && this.onError(event.error);
        };
        
        this.recognition.onresult = (event) => {
            // Clear any existing silence timer since we're receiving speech
            if (this.silenceTimer) {
                clearTimeout(this.silenceTimer);
                this.silenceTimer = null;
            }
            
            let interimTranscript = '';
            let finalTranscript = this.finalTranscript;
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                    this.hasReceivedSpeech = true;
                } else {
                    interimTranscript += transcript;
                    if (transcript.trim()) {
                        this.hasReceivedSpeech = true;
                    }
                }
            }
            
            this.finalTranscript = finalTranscript;
            this.interimTranscript = interimTranscript;
            
            this.onResult && this.onResult({
                final: finalTranscript,
                interim: interimTranscript,
                isFinal: event.results[event.results.length - 1].isFinal
            });
            
            // Start silence timer if we have received some speech
            if (this.hasReceivedSpeech && this.isListening) {
                this.startSilenceTimer();
            }
        };
    }
    
    startSilenceTimer() {
        // Clear any existing timer
        if (this.silenceTimer) {
            clearTimeout(this.silenceTimer);
        }
        
        // Start new silence timer
        this.silenceTimer = setTimeout(() => {
            console.log('Silence detected, stopping recognition');
            if (this.isListening) {
                this.stop();
            }
        }, this.silenceTimeout);
    }
    
    start() {
        return new Promise((resolve, reject) => {
            if (!this.recognition) {
                reject(new Error('Speech recognition not supported'));
                return;
            }
            
            if (this.isListening) {
                reject(new Error('Already listening'));
                return;
            }
            
            this.finalTranscript = '';
            this.interimTranscript = '';
            this.hasReceivedSpeech = false;
            
            // Clear any existing silence timer
            if (this.silenceTimer) {
                clearTimeout(this.silenceTimer);
                this.silenceTimer = null;
            }
            
            this.onEnd = () => {
                // Clear silence timer when stopping
                if (this.silenceTimer) {
                    clearTimeout(this.silenceTimer);
                    this.silenceTimer = null;
                }
                
                resolve({
                    success: true,
                    text: this.finalTranscript.trim(),
                    confidence: 0.8 // Approximate confidence
                });
            };
            
            this.onError = (error) => {
                reject(new Error(`Speech recognition failed: ${error}`));
            };
            
            try {
                this.recognition.start();
            } catch (error) {
                reject(error);
            }
        });
    }
    
    stop() {
        if (this.recognition && this.isListening) {
            // Clear silence timer
            if (this.silenceTimer) {
                clearTimeout(this.silenceTimer);
                this.silenceTimer = null;
            }
            this.recognition.stop();
        }
    }
    
    abort() {
        if (this.recognition && this.isListening) {
            // Clear silence timer
            if (this.silenceTimer) {
                clearTimeout(this.silenceTimer);
                this.silenceTimer = null;
            }
            this.recognition.abort();
        }
    }
    
    // Quick recognition for short phrases
    quickRecognition(timeout = 5000) {
        return new Promise((resolve, reject) => {
            if (!this.recognition) {
                reject(new Error('Speech recognition not supported'));
                return;
            }
            
            const oldContinuous = this.recognition.continuous;
            this.recognition.continuous = false;
            
            const timeoutId = setTimeout(() => {
                this.stop();
                reject(new Error('Recognition timeout'));
            }, timeout);
            
            this.onResult = (result) => {
                if (result.isFinal) {
                    clearTimeout(timeoutId);
                    this.recognition.continuous = oldContinuous;
                    resolve({
                        success: true,
                        text: result.final.trim(),
                        confidence: 0.8
                    });
                }
            };
            
            this.onError = (error) => {
                clearTimeout(timeoutId);
                this.recognition.continuous = oldContinuous;
                reject(new Error(`Quick recognition failed: ${error}`));
            };
            
            try {
                this.recognition.start();
            } catch (error) {
                clearTimeout(timeoutId);
                this.recognition.continuous = oldContinuous;
                reject(error);
            }
        });
    }
    
    // Configure silence timeout
    setSilenceTimeout(timeout) {
        this.silenceTimeout = timeout;
    }
    
    // Check if speech recognition is available
    static isSupported() {
        return !!(window.SpeechRecognition || window.webkitSpeechRecognition);
    }
    
    // Get available languages (approximate list)
    static getSupportedLanguages() {
        return [
            { code: 'en-US', name: 'English (US)' },
            { code: 'en-GB', name: 'English (UK)' },
            { code: 'es-ES', name: 'Spanish' },
            { code: 'fr-FR', name: 'French' },
            { code: 'de-DE', name: 'German' },
            { code: 'it-IT', name: 'Italian' },
            { code: 'pt-BR', name: 'Portuguese (Brazil)' },
            { code: 'ru-RU', name: 'Russian' },
            { code: 'ja-JP', name: 'Japanese' },
            { code: 'ko-KR', name: 'Korean' },
            { code: 'zh-CN', name: 'Chinese (Mandarin)' }
        ];
    }
}

// Fallback to server-side speech recognition
class ServerSpeechToText {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
    }
    
    async start() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    channelCount: 1,
                    sampleRate: 16000,
                    sampleSize: 16
                }
            });
            
            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=opus'
            });
            
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };
            
            return new Promise((resolve, reject) => {
                this.mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                    
                    try {
                        const result = await this.sendToServer(audioBlob);
                        resolve(result);
                    } catch (error) {
                        reject(error);
                    }
                };
                
                this.mediaRecorder.start();
                this.isRecording = true;
                
                // Auto-stop after 30 seconds
                setTimeout(() => {
                    if (this.isRecording) {
                        this.stop();
                    }
                }, 30000);
            });
            
        } catch (error) {
            throw new Error(`Failed to access microphone: ${error.message}`);
        }
    }
    
    stop() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            
            // Stop all tracks
            this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    }
    
    async sendToServer(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');
        
        const response = await fetch('/voice/speech-to-text', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Server speech recognition failed');
        }
        
        return await response.json();
    }
}

// Export global instance
window.SpeechToTextClient = SpeechToTextClient;
window.ServerSpeechToText = ServerSpeechToText;

if (SpeechToTextClient.isSupported()) {
    console.log('Initializing browser speech recognition');
    window.speechToText = new SpeechToTextClient();
} else {
    console.log('Browser speech recognition not supported, using server-side speech recognition');
    window.speechToText = new ServerSpeechToText();
}

console.log('speechToText initialized:', window.speechToText);