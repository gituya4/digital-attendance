import qrcode
import hmac
import hashlib
import json
import base64
import random
import string
from datetime import datetime
from io import BytesIO
import os

class QRService:
    @staticmethod
    def generate_pin() -> str:
        return ''.join(random.choices(string.digits, k=4))
    
    @staticmethod
    def generate_token(session_id: int, timestamp: datetime, secret_key: str) -> str:
        payload = {
            'session_id': session_id,
            'timestamp': timestamp.isoformat()
        }
        payload_json = json.dumps(payload, sort_keys=True)
        payload_b64 = base64.b64encode(payload_json.encode()).decode()
        
        signature = hmac.new(
            secret_key.encode(),
            payload_b64.encode(),
            hashlib.sha256
        ).hexdigest()
        
        token = f"{payload_b64}.{signature}"
        return token
    
    @staticmethod
    def verify_token(token: str, secret_key: str) -> tuple:
        try:
            parts = token.split('.')
            if len(parts) != 2:
                return False, None
            
            payload_b64, signature = parts
            
            expected_signature = hmac.new(
                secret_key.encode(),
                payload_b64.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                return False, None
            
            payload_json = base64.b64decode(payload_b64).decode()
            payload = json.loads(payload_json)
            
            return True, payload
        except Exception:
            return False, None
    
    @staticmethod
    def generate_qr_code(token: str) -> bytes:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(token)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()
    
    @staticmethod
    def generate_qr_base64(token: str) -> str:
        qr_bytes = QRService.generate_qr_code(token)
        return base64.b64encode(qr_bytes).decode()
