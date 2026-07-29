import re
from typing import Tuple, Optional, Dict, Any
from app.models.user import User

class AuthService:
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        return True, ""
    
    @staticmethod
    def validate_registration_number(reg_number: str) -> bool:
        pattern = r'^[A-Za-z]{2}/[A-Za-z]{2}/\d{4}/\d{2}/\d{2}$'
        return re.match(pattern, reg_number) is not None
    
    @staticmethod
    def register_student(full_name: str, registration_number: str, email: str, password: str) -> Tuple[bool, str]:
        if not full_name or len(full_name.strip()) < 2:
            return False, "Full name must be at least 2 characters"
        
        if not AuthService.validate_registration_number(registration_number):
            return False, "Invalid registration number format (expected: CS/MK/0792/09/23)"
        
        if User.registration_number_exists(registration_number):
            return False, "Registration number already in use"
        
        if not AuthService.validate_email(email):
            return False, "Invalid email format"
        
        if User.email_exists(email):
            return False, "Email already in use"
        
        is_valid, error_msg = AuthService.validate_password(password)
        if not is_valid:
            return False, error_msg
        
        result = User.create(
            full_name=full_name,
            email=email,
            password=password,
            role='student',
            registration_number=registration_number
        )
        
        if result:
            return True, "Registration successful"
        else:
            return False, "Registration failed. Please try again."
    
    @staticmethod
    def register_lecturer(full_name: str, staff_id: str, email: str, password: str, department: str) -> Tuple[bool, str]:
        if not full_name or len(full_name.strip()) < 2:
            return False, "Full name must be at least 2 characters"
        
        if not staff_id or len(staff_id.strip()) < 3:
            return False, "Staff ID is required"
        
        if User.staff_id_exists(staff_id):
            return False, "Staff ID already in use"
        
        if not AuthService.validate_email(email):
            return False, "Invalid email format"
        
        if User.email_exists(email):
            return False, "Email already in use"
        
        is_valid, error_msg = AuthService.validate_password(password)
        if not is_valid:
            return False, error_msg
        
        result = User.create(
            full_name=full_name,
            email=email,
            password=password,
            role='lecturer',
            staff_id=staff_id,
            department=department
        )
        
        if result:
            return True, "Registration successful"
        else:
            return False, "Registration failed. Please try again."
    
    @staticmethod
    def login(email: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        if not email or not password:
            return False, None, "Email and password are required"
        
        user = User.get_by_email(email)
        if not user:
            return False, None, "Invalid email or password"
        
        if not User.verify_password(password, user['password_hash']):
            return False, None, "Invalid email or password"
        
        user_data = {
            'user_id': user['user_id'],
            'full_name': user['full_name'],
            'email': user['email'],
            'role': user['role']
        }
        
        return True, user_data, "Login successful"
