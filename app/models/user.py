import bcrypt
from app.database import db
from typing import Optional, Dict, Any

class User:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    @staticmethod
    def create(full_name: str, email: str, password: str, role: str, 
               registration_number: Optional[str] = None, 
               staff_id: Optional[str] = None,
               department: Optional[str] = None) -> Optional[int]:
        password_hash = User.hash_password(password)
        query = """
            INSERT INTO users (full_name, email, password_hash, role, registration_number, staff_id, department)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            result = db.execute_query(query, (full_name, email, password_hash, role, registration_number, staff_id, department))
            return result
        except Exception as e:
            return None
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM users WHERE email = %s AND is_active = TRUE"
        return db.execute_query(query, (email,), fetch_one=True)
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM users WHERE user_id = %s AND is_active = TRUE"
        return db.execute_query(query, (user_id,), fetch_one=True)
    
    @staticmethod
    def get_all(role: Optional[str] = None) -> list:
        if role:
            query = "SELECT * FROM users WHERE role = %s AND is_active = TRUE ORDER BY created_at DESC"
            return db.execute_query(query, (role,))
        else:
            query = "SELECT * FROM users WHERE is_active = TRUE ORDER BY created_at DESC"
            return db.execute_query(query)
    
    @staticmethod
    def email_exists(email: str) -> bool:
        query = "SELECT user_id FROM users WHERE email = %s"
        return db.execute_query(query, (email,), fetch_one=True) is not None
    
    @staticmethod
    def registration_number_exists(reg_number: str) -> bool:
        query = "SELECT user_id FROM users WHERE registration_number = %s"
        return db.execute_query(query, (reg_number,), fetch_one=True) is not None
    
    @staticmethod
    def staff_id_exists(staff_id: str) -> bool:
        query = "SELECT user_id FROM users WHERE staff_id = %s"
        return db.execute_query(query, (staff_id,), fetch_one=True) is not None
    
    @staticmethod
    def update(user_id: int, **kwargs) -> bool:
        allowed_fields = {'full_name', 'email', 'department', 'is_active'}
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return False
        
        set_clause = ', '.join([f"{k} = %s" for k in updates.keys()])
        values = list(updates.values()) + [user_id]
        query = f"UPDATE users SET {set_clause} WHERE user_id = %s"
        
        db.execute_query(query, tuple(values))
        return True
    
    @staticmethod
    def deactivate(user_id: int) -> bool:
        query = "UPDATE users SET is_active = FALSE WHERE user_id = %s"
        db.execute_query(query, (user_id,))
        return True
