// WebRTC Client for TeleMed AI Video Consultations

class WebRTCClient {
    constructor(roomId, userRole) {
        this.roomId = roomId;
        this.userRole = userRole;
        this.localStream = null;
        this.remoteStream = null;
        this.peerConnection = null;
        this.signaling = null;
        this.isConnected = false;
        this.isMuted = false;
        this.isVideoOff = false;
        
        // WebRTC configuration
        this.config = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' },
                { urls: 'stun:stun1.l.google.com:19302' }
            ]
        };
    }
    
    async init() {
        try {
            await this.setupMedia();
            this.setupPeerConnection();
            await this.setupSignaling();
            console.log('WebRTC initialized successfully');
        } catch (error) {
            console.error('WebRTC initialization failed:', error);
            throw error;
        }
    }
    
    async setupMedia() {
        try {
            this.localStream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { min: 320, ideal: 640, max: 1280 },
                    height: { min: 240, ideal: 480, max: 720 }
                },
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                }
            });
            
            // Display local video
            this.displayLocalVideo();
            console.log('Local media stream obtained');
            
        } catch (error) {
            console.error('Failed to access media devices:', error);
            // Fallback: try audio only
            try {
                this.localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                console.log('Audio-only stream obtained');
            } catch (audioError) {
                throw new Error('Failed to access microphone and camera');
            }
        }
    }
    
    setupPeerConnection() {
        this.peerConnection = new RTCPeerConnection(this.config);
        
        // Add local stream to peer connection
        if (this.localStream) {
            this.localStream.getTracks().forEach(track => {
                this.peerConnection.addTrack(track, this.localStream);
            });
        }
        
        // Handle remote stream
        this.peerConnection.ontrack = (event) => {
            console.log('Received remote track');
            this.remoteStream = event.streams[0];
            this.displayRemoteVideo();
        };
        
        // Handle ICE candidates
        this.peerConnection.onicecandidate = (event) => {
            if (event.candidate) {
                this.sendSignal('ice-candidate', event.candidate);
            }
        };
        
        // Connection state changes
        this.peerConnection.onconnectionstatechange = () => {
            console.log('Connection state:', this.peerConnection.connectionState);
            this.isConnected = this.peerConnection.connectionState === 'connected';
            
            if (this.isConnected) {
                this.onConnected && this.onConnected();
            }
        };
        
        // Handle data channel (for chat)
        this.peerConnection.ondatachannel = (event) => {
            const channel = event.channel;
            channel.onmessage = (event) => {
                this.onChatMessage && this.onChatMessage(JSON.parse(event.data));
            };
        };
    }
    
    async setupSignaling() {
        // For demo purposes, we'll simulate signaling
        // In production, use WebSockets or Socket.IO
        console.log('Setting up signaling for room:', this.roomId);
        
        // Simulate signaling delay
        setTimeout(() => {
            if (this.userRole === 'patient') {
                this.createOffer();
            }
        }, 1000);
    }
    
    async createOffer() {
        try {
            const offer = await this.peerConnection.createOffer();
            await this.peerConnection.setLocalDescription(offer);
            this.sendSignal('offer', offer);
            console.log('Offer created and sent');
        } catch (error) {
            console.error('Failed to create offer:', error);
        }
    }
    
    async createAnswer(offer) {
        try {
            await this.peerConnection.setRemoteDescription(offer);
            const answer = await this.peerConnection.createAnswer();
            await this.peerConnection.setLocalDescription(answer);
            this.sendSignal('answer', answer);
            console.log('Answer created and sent');
        } catch (error) {
            console.error('Failed to create answer:', error);
        }
    }
    
    async handleAnswer(answer) {
        try {
            await this.peerConnection.setRemoteDescription(answer);
            console.log('Answer received and processed');
        } catch (error) {
            console.error('Failed to handle answer:', error);
        }
    }
    
    async handleIceCandidate(candidate) {
        try {
            await this.peerConnection.addIceCandidate(candidate);
            console.log('ICE candidate added');
        } catch (error) {
            console.error('Failed to add ICE candidate:', error);
        }
    }
    
    sendSignal(type, data) {
        // In a real implementation, this would send via WebSocket
        console.log('Sending signal:', type, data);
        
        // Simulate signaling for demo
        if (type === 'offer' && this.userRole === 'patient') {
            setTimeout(() => this.simulateDoctor(data), 2000);
        }
    }
    
    // Demo simulation - remove in production
    simulateDoctor(offer) {
        console.log('Simulating doctor response...');
        // In reality, the doctor would receive this offer and create an answer
    }
    
    displayLocalVideo() {
        const localVideo = document.querySelector('.local-video') || this.createVideoElement('local');
        localVideo.srcObject = this.localStream;
        localVideo.muted = true; // Prevent audio feedback
    }
    
    displayRemoteVideo() {
        const remoteVideo = document.querySelector('.remote-video') || this.createVideoElement('remote');
        remoteVideo.srcObject = this.remoteStream;
    }
    
    createVideoElement(type) {
        const video = document.createElement('video');
        video.autoplay = true;
        video.playsInline = true;
        video.className = `${type}-video`;
        
        if (type === 'local') {
            // Add to picture-in-picture container
            const pipContainer = document.querySelector('.video-pip');
            if (pipContainer) {
                pipContainer.innerHTML = '';
                pipContainer.appendChild(video);
            }
        } else {
            // Add to main video area
            const mainContainer = document.querySelector('.video-container');
            if (mainContainer) {
                mainContainer.innerHTML = '';
                mainContainer.appendChild(video);
            }
        }
        
        return video;
    }
    
    toggleVideo() {
        if (this.localStream) {
            const videoTrack = this.localStream.getVideoTracks()[0];
            if (videoTrack) {
                videoTrack.enabled = !videoTrack.enabled;
                this.isVideoOff = !videoTrack.enabled;
                return !this.isVideoOff;
            }
        }
        return false;
    }
    
    toggleAudio() {
        if (this.localStream) {
            const audioTrack = this.localStream.getAudioTracks()[0];
            if (audioTrack) {
                audioTrack.enabled = !audioTrack.enabled;
                this.isMuted = !audioTrack.enabled;
                return !this.isMuted;
            }
        }
        return false;
    }
    
    async shareScreen() {
        try {
            const screenStream = await navigator.mediaDevices.getDisplayMedia({
                video: true,
                audio: true
            });
            
            const videoTrack = screenStream.getVideoTracks()[0];
            const sender = this.peerConnection.getSenders().find(s => 
                s.track && s.track.kind === 'video'
            );
            
            if (sender) {
                await sender.replaceTrack(videoTrack);
            }
            
            videoTrack.onended = () => {
                this.stopScreenShare();
            };
            
            return true;
        } catch (error) {
            console.error('Screen sharing failed:', error);
            return false;
        }
    }
    
    async stopScreenShare() {
        if (this.localStream) {
            const videoTrack = this.localStream.getVideoTracks()[0];
            const sender = this.peerConnection.getSenders().find(s => 
                s.track && s.track.kind === 'video'
            );
            
            if (sender && videoTrack) {
                await sender.replaceTrack(videoTrack);
            }
        }
    }
    
    sendChatMessage(message) {
        const dataChannel = this.peerConnection.createDataChannel('chat');
        dataChannel.send(JSON.stringify({
            type: 'chat',
            message: message,
            timestamp: new Date().toISOString(),
            sender: this.userRole
        }));
    }
    
    disconnect() {
        if (this.localStream) {
            this.localStream.getTracks().forEach(track => track.stop());
        }
        
        if (this.peerConnection) {
            this.peerConnection.close();
        }
        
        this.isConnected = false;
        console.log('WebRTC disconnected');
    }
    
    getConnectionStats() {
        if (this.peerConnection) {
            return this.peerConnection.getStats();
        }
        return null;
    }
}

// WebRTC Helper Functions
class WebRTCHelper {
    static async checkSupport() {
        const support = {
            webrtc: !!(window.RTCPeerConnection),
            mediaDevices: !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia),
            screenShare: !!(navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia)
        };
        
        console.log('WebRTC support:', support);
        return support;
    }
    
    static async getMediaDevices() {
        try {
            const devices = await navigator.mediaDevices.enumerateDevices();
            return {
                cameras: devices.filter(device => device.kind === 'videoinput'),
                microphones: devices.filter(device => device.kind === 'audioinput'),
                speakers: devices.filter(device => device.kind === 'audiooutput')
            };
        } catch (error) {
            console.error('Failed to enumerate devices:', error);
            return { cameras: [], microphones: [], speakers: [] };
        }
    }
    
    static formatBandwidth(bytes) {
        const kb = bytes / 1024;
        const mb = kb / 1024;
        
        if (mb >= 1) {
            return `${mb.toFixed(1)} MB/s`;
        } else if (kb >= 1) {
            return `${kb.toFixed(1)} KB/s`;
        } else {
            return `${bytes} B/s`;
        }
    }
}

// Export for global use
window.WebRTCClient = WebRTCClient;
window.WebRTCHelper = WebRTCHelper;

// Initialize support check
document.addEventListener('DOMContentLoaded', async () => {
    const support = await WebRTCHelper.checkSupport();
    if (!support.webrtc) {
        console.warn('WebRTC not supported - video calls will not work');
    }
    
    window.telemed = window.telemed || {};
    window.telemed.webrtcSupport = support;
});