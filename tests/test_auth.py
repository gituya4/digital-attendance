import unittest
from app import create_app
from app.models.user import User
from app.database import db

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_student_registration_valid(self):
        response = self.client.post('/api/auth/register', json={
            'role': 'student',
            'full_name': 'John Doe',
            'registration_number': 'CS/MK/0792/09/23',
            'email': 'john@example.com',
            'password': 'TestPassword123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json['success'])
    
    def test_student_registration_invalid_reg_number(self):
        response = self.client.post('/api/auth/register', json={
            'role': 'student',
            'full_name': 'John Doe',
            'registration_number': 'INVALID',
            'email': 'john@example.com',
            'password': 'TestPassword123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json['success'])
    
    def test_student_registration_weak_password(self):
        response = self.client.post('/api/auth/register', json={
            'role': 'student',
            'full_name': 'John Doe',
            'registration_number': 'CS/MK/0792/09/23',
            'email': 'john@example.com',
            'password': 'weak'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json['success'])
    
    def test_student_registration_duplicate_email(self):
        self.client.post('/api/auth/register', json={
            'role': 'student',
            'full_name': 'John Doe',
            'registration_number': 'CS/MK/0792/09/23',
            'email': 'john@example.com',
            'password': 'TestPassword123'
        })
        
        response = self.client.post('/api/auth/register', json={
            'role': 'student',
            'full_name': 'Jane Doe',
            'registration_number': 'CS/MK/0793/09/23',
            'email': 'john@example.com',
            'password': 'TestPassword123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json['success'])
    
    def test_login_valid(self):
        self.client.post('/api/auth/register', json={
            'role': 'student',
            'full_name': 'John Doe',
            'registration_number': 'CS/MK/0792/09/23',
            'email': 'john@example.com',
            'password': 'TestPassword123'
        })
        
        response = self.client.post('/api/auth/login', json={
            'email': 'john@example.com',
            'password': 'TestPassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertIn('user', response.json)
    
    def test_login_invalid_password(self):
        self.client.post('/api/auth/register', json={
            'role': 'student',
            'full_name': 'John Doe',
            'registration_number': 'CS/MK/0792/09/23',
            'email': 'john@example.com',
            'password': 'TestPassword123'
        })
        
        response = self.client.post('/api/auth/login', json={
            'email': 'john@example.com',
            'password': 'WrongPassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json['success'])
    
    def test_login_nonexistent_user(self):
        response = self.client.post('/api/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'TestPassword123'
        })
        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json['success'])

if __name__ == '__main__':
    unittest.main()
