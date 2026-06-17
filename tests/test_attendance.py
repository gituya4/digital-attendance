import unittest
from datetime import datetime
from app import create_app
from app.services.qr_service import QRService
from app.config import Config

class TestAttendanceValidation(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_qr_token_generation(self):
        session_id = 1
        now = datetime.utcnow()
        token = QRService.generate_token(session_id, now, Config.HMAC_SECRET_KEY)
        
        self.assertIsNotNone(token)
        self.assertIn('.', token)
    
    def test_qr_token_verification_valid(self):
        session_id = 1
        now = datetime.utcnow()
        token = QRService.generate_token(session_id, now, Config.HMAC_SECRET_KEY)
        
        is_valid, payload = QRService.verify_token(token, Config.HMAC_SECRET_KEY)
        
        self.assertTrue(is_valid)
        self.assertIsNotNone(payload)
        self.assertEqual(payload['session_id'], session_id)
    
    def test_qr_token_verification_tampered(self):
        session_id = 1
        now = datetime.utcnow()
        token = QRService.generate_token(session_id, now, Config.HMAC_SECRET_KEY)
        
        tampered_token = token[:-5] + 'XXXXX'
        is_valid, payload = QRService.verify_token(tampered_token, Config.HMAC_SECRET_KEY)
        
        self.assertFalse(is_valid)
        self.assertIsNone(payload)
    
    def test_qr_token_verification_wrong_secret(self):
        session_id = 1
        now = datetime.utcnow()
        token = QRService.generate_token(session_id, now, Config.HMAC_SECRET_KEY)
        
        is_valid, payload = QRService.verify_token(token, 'wrong-secret-key')
        
        self.assertFalse(is_valid)
        self.assertIsNone(payload)
    
    def test_pin_generation(self):
        pin = QRService.generate_pin()
        
        self.assertEqual(len(pin), 4)
        self.assertTrue(pin.isdigit())
    
    def test_qr_code_generation(self):
        token = 'test.token'
        qr_bytes = QRService.generate_qr_code(token)
        
        self.assertIsNotNone(qr_bytes)
        self.assertGreater(len(qr_bytes), 0)
    
    def test_qr_code_base64_generation(self):
        token = 'test.token'
        qr_base64 = QRService.generate_qr_base64(token)
        
        self.assertIsNotNone(qr_base64)
        self.assertTrue(qr_base64.startswith('iVBOR'))

if __name__ == '__main__':
    unittest.main()
