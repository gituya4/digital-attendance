import unittest
from datetime import datetime, timedelta
from app import create_app
from app.models.user import User
from app.models.unit import Unit
from app.models.session import Session
from app.models.attendance import Attendance
from app.services.qr_service import QRService
from app.config import Config
from app.database import db

class TestAttendanceValidation(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        self.student_id = User.create('Test Student', 'student@test.com', 'TestPassword123', 'student', registration_number='CS/MK/0792/09/23')
        self.lecturer_id = User.create('Test Lecturer', 'lecturer@test.com', 'TestPassword123', 'lecturer', staff_id='LEC001', department='CS')
        self.unit_id = Unit.create('CS101', 'Introduction to CS', 'Computer Science', '1', '2024')
        
        Unit.assign_lecturer(self.lecturer_id, self.unit_id)
        Unit.enroll_student(self.student_id, self.unit_id)
    
    def test_valid_qr_token_generation(self):
        session_id = 1
        now = datetime.utcnow()
        token = QRService.generate_token(session_id, now, Config.HMAC_SECRET_KEY)
        
        is_valid, payload = QRService.verify_token(token, Config.HMAC_SECRET_KEY)
        
        self.assertTrue(is_valid)
        self.assertEqual(payload['session_id'], session_id)
    
    def test_expired_qr_token(self):
        session_id = 1
        old_time = datetime.utcnow() - timedelta(seconds=35)
        token = QRService.generate_token(session_id, old_time, Config.HMAC_SECRET_KEY)
        
        is_valid, payload = QRService.verify_token(token, Config.HMAC_SECRET_KEY)
        
        self.assertTrue(is_valid)
        self.assertIsNotNone(payload)
        
        if payload:
            token_time = datetime.fromisoformat(payload['timestamp'])
            age = (datetime.utcnow() - token_time).total_seconds()
            self.assertGreater(age, 30)
    
    def test_tampered_qr_token(self):
        session_id = 1
        now = datetime.utcnow()
        token = QRService.generate_token(session_id, now, Config.HMAC_SECRET_KEY)
        
        tampered = token[:-5] + 'XXXXX'
        is_valid, payload = QRService.verify_token(tampered, Config.HMAC_SECRET_KEY)
        
        self.assertFalse(is_valid)
        self.assertIsNone(payload)
    
    def test_wrong_secret_key(self):
        session_id = 1
        now = datetime.utcnow()
        token = QRService.generate_token(session_id, now, Config.HMAC_SECRET_KEY)
        
        is_valid, payload = QRService.verify_token(token, 'wrong-secret-key')
        
        self.assertFalse(is_valid)
        self.assertIsNone(payload)
    
    def test_pin_generation_format(self):
        pin = QRService.generate_pin()
        
        self.assertEqual(len(pin), 4)
        self.assertTrue(pin.isdigit())
    
    def test_session_creation(self):
        now = datetime.utcnow()
        pin = QRService.generate_pin()
        token = QRService.generate_token(1, now, Config.HMAC_SECRET_KEY)
        
        session_id = Session.create(self.unit_id, self.lecturer_id, pin, token, now)
        
        self.assertIsNotNone(session_id)
        
        session = Session.get_by_id(session_id)
        self.assertIsNotNone(session)
        self.assertEqual(session['status'], 'active')
        self.assertEqual(session['session_pin'], pin)
    
    def test_duplicate_attendance_prevention(self):
        now = datetime.utcnow()
        pin = QRService.generate_pin()
        token = QRService.generate_token(1, now, Config.HMAC_SECRET_KEY)
        
        session_id = Session.create(self.unit_id, self.lecturer_id, pin, token, now)
        
        Attendance.mark(session_id, self.student_id, self.unit_id)
        
        is_duplicate = Attendance.already_marked(session_id, self.student_id)
        self.assertTrue(is_duplicate)
    
    def test_student_enrollment_check(self):
        unenrolled_student_id = User.create('Unenrolled', 'unenrolled@test.com', 'TestPassword123', 'student', registration_number='CS/MK/0793/09/23')
        
        is_enrolled = Unit.is_student_enrolled(unenrolled_student_id, self.unit_id)
        self.assertFalse(is_enrolled)
        
        is_enrolled = Unit.is_student_enrolled(self.student_id, self.unit_id)
        self.assertTrue(is_enrolled)
    
    def test_attendance_percentage_calculation(self):
        now = datetime.utcnow()
        pin = QRService.generate_pin()
        token = QRService.generate_token(1, now, Config.HMAC_SECRET_KEY)
        
        session_id = Session.create(self.unit_id, self.lecturer_id, pin, token, now)
        Session.close(session_id)
        
        Attendance.mark(session_id, self.student_id, self.unit_id)
        
        percentage = Attendance.get_student_unit_attendance_percentage(self.student_id, self.unit_id)
        
        self.assertEqual(percentage, 100.0)
    
    def test_session_closure(self):
        now = datetime.utcnow()
        pin = QRService.generate_pin()
        token = QRService.generate_token(1, now, Config.HMAC_SECRET_KEY)
        
        session_id = Session.create(self.unit_id, self.lecturer_id, pin, token, now)
        
        session = Session.get_by_id(session_id)
        self.assertEqual(session['status'], 'active')
        
        Session.close(session_id)
        
        session = Session.get_by_id(session_id)
        self.assertEqual(session['status'], 'closed')
    
    def test_qr_code_generation(self):
        token = 'test.token.data'
        qr_bytes = QRService.generate_qr_code(token)
        
        self.assertIsNotNone(qr_bytes)
        self.assertGreater(len(qr_bytes), 0)
        self.assertTrue(qr_bytes.startswith(b'\x89PNG'))
    
    def test_qr_code_base64_encoding(self):
        token = 'test.token.data'
        qr_base64 = QRService.generate_qr_base64(token)
        
        self.assertIsNotNone(qr_base64)
        self.assertTrue(qr_base64.startswith('iVBOR'))
    
    def test_session_attendance_count(self):
        now = datetime.utcnow()
        pin = QRService.generate_pin()
        token = QRService.generate_token(1, now, Config.HMAC_SECRET_KEY)
        
        session_id = Session.create(self.unit_id, self.lecturer_id, pin, token, now)
        
        count = Session.get_attendance_count(session_id)
        self.assertEqual(count, 0)
        
        Attendance.mark(session_id, self.student_id, self.unit_id)
        
        count = Session.get_attendance_count(session_id)
        self.assertEqual(count, 1)
    
    def test_get_session_attendance_records(self):
        now = datetime.utcnow()
        pin = QRService.generate_pin()
        token = QRService.generate_token(1, now, Config.HMAC_SECRET_KEY)
        
        session_id = Session.create(self.unit_id, self.lecturer_id, pin, token, now)
        Attendance.mark(session_id, self.student_id, self.unit_id)
        
        records = Session.get_session_attendance(session_id)
        
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['student_id'], self.student_id)
        self.assertEqual(records[0]['full_name'], 'Test Student')

if __name__ == '__main__':
    unittest.main()
