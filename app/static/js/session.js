class SessionManager {
    constructor(sessionId) {
        this.sessionId = sessionId;
        this.qrRefreshInterval = null;
        this.sseConnection = null;
        this.lastTokenTime = null;
    }
    
    async startQRRefresh(updateCallback, interval = 5000) {
        await updateCallback();
        
        this.qrRefreshInterval = setInterval(async () => {
            try {
                await updateCallback();
            } catch (error) {
                console.error('QR refresh error:', error);
            }
        }, interval);
    }
    
    stopQRRefresh() {
        if (this.qrRefreshInterval) {
            clearInterval(this.qrRefreshInterval);
            this.qrRefreshInterval = null;
        }
    }
    
    connectLiveAttendance(updateCallback) {
        const eventSource = new EventSource(`/api/sessions/${this.sessionId}/live`);
        
        eventSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                updateCallback(data);
            } catch (error) {
                console.error('SSE parse error:', error);
            }
        };
        
        eventSource.onerror = (error) => {
            console.error('SSE connection error:', error);
            eventSource.close();
        };
        
        this.sseConnection = eventSource;
    }
    
    disconnectLiveAttendance() {
        if (this.sseConnection) {
            this.sseConnection.close();
            this.sseConnection = null;
        }
    }
    
    async closeSession() {
        try {
            const response = await API.post(`/sessions/${this.sessionId}/close`, {});
            this.stopQRRefresh();
            this.disconnectLiveAttendance();
            return response;
        } catch (error) {
            throw error;
        }
    }
    
    async exportAttendance() {
        try {
            const response = await fetch(`/api/sessions/${this.sessionId}/export`);
            if (!response.ok) throw new Error('Export failed');
            
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `attendance_${this.sessionId}.csv`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            return true;
        } catch (error) {
            throw error;
        }
    }
}

class AttendanceAnimator {
    static animateNewAttendee(name, container) {
        const entry = document.createElement('div');
        entry.style.cssText = `
            padding: 0.75rem;
            background-color: #D1FAE5;
            border-left: 4px solid #10B981;
            border-radius: 4px;
            margin-bottom: 0.5rem;
            animation: slideInLeft 0.3s ease-out;
        `;
        entry.textContent = name;
        
        container.insertBefore(entry, container.firstChild);
        
        setTimeout(() => {
            entry.style.backgroundColor = '#F4F6F9';
            entry.style.borderLeftColor = '#E5E7EB';
        }, 2000);
    }
    
    static animateSuccess() {
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(16, 185, 129, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            animation: fadeIn 0.3s ease-out;
        `;
        
        const checkmark = document.createElement('div');
        checkmark.style.cssText = `
            font-size: 4rem;
            animation: scaleIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        `;
        checkmark.textContent = '✓';
        
        overlay.appendChild(checkmark);
        document.body.appendChild(overlay);
        
        setTimeout(() => {
            overlay.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => overlay.remove(), 300);
        }, 1500);
    }
    
    static animateError(message) {
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(239, 68, 68, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            animation: fadeIn 0.3s ease-out;
        `;
        
        const content = document.createElement('div');
        content.style.cssText = `
            text-align: center;
            color: white;
            animation: shake 0.5s ease-out;
        `;
        content.innerHTML = `
            <div style="font-size: 3rem; margin-bottom: 1rem;">✕</div>
            <div style="font-size: 1.25rem;">${message}</div>
        `;
        
        overlay.appendChild(content);
        document.body.appendChild(overlay);
        
        setTimeout(() => {
            overlay.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => overlay.remove(), 300);
        }, 2000);
    }
}

const styles = document.createElement('style');
styles.textContent = `
    @keyframes slideInLeft {
        from {
            transform: translateX(-20px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    
    @keyframes scaleIn {
        from {
            transform: scale(0);
            opacity: 0;
        }
        to {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
        20%, 40%, 60%, 80% { transform: translateX(10px); }
    }
`;
document.head.appendChild(styles);
