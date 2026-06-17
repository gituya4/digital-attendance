class QRScanner {
    constructor(videoElementId, onScan) {
        this.videoElement = document.getElementById(videoElementId);
        this.onScan = onScan;
        this.stream = null;
        this.scanning = false;
        this.codeReader = null;
    }
    
    async start() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: { 
                    facingMode: 'environment',
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                }
            });
            
            this.videoElement.srcObject = this.stream;
            this.videoElement.play();
            this.scanning = true;
            
            // Use ZXing for QR decoding
            this.codeReader = new ZXing.BrowserQRCodeReader();
            this.codeReader.decodeFromVideoDevice(null, this.videoElement, (result, error) => {
                if (result) {
                    this.onScan(result.text);
                    this.stop();
                }
                if (error && error.name !== 'NotFoundException') {
                    console.error('QR decode error:', error);
                }
            });
            
        } catch (error) {
            console.error('Camera access error:', error);
            throw new Error('Camera access denied. Please enable camera permissions.');
        }
    }
    
    stop() {
        this.scanning = false;
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }
        if (this.codeReader) {
            this.codeReader.reset();
        }
    }
}

class CameraPermissionHandler {
    static async checkPermission() {
        try {
            const permission = await navigator.permissions.query({ name: 'camera' });
            return permission.state;
        } catch (error) {
            return 'unknown';
        }
    }
    
    static async requestPermission() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            stream.getTracks().forEach(track => track.stop());
            return true;
        } catch (error) {
            return false;
        }
    }
}
