from app.database import db
from typing import Optional, Dict, Any, List
from datetime import datetime

class Session:
    @staticmethod
    def create(unit_id: int, lecturer_id: int, session_pin: str, 
               current_token: str, token_generated_at: datetime) -> Optional[int]:
        query = """
            INSERT INTO sessions (unit_id, lecturer_id, session_pin, current_token, token_generated_at, status)
            VALUES (%s, %s, %s, %s, %s, 'active')
        """
        try:
            result = db.execute_query(query, (unit_id, lecturer_id, session_pin, current_token, token_generated_at))
            return result
        except Exception:
            return None
    
    @staticmethod
    def get_by_id(session_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM sessions WHERE session_id = %s"
        return db.execute_query(query, (session_id,), fetch_one=True)
    
    @staticmethod
    def get_active_by_unit(unit_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM sessions WHERE unit_id = %s AND status = 'active' ORDER BY start_time DESC LIMIT 1"
        return db.execute_query(query, (unit_id,), fetch_one=True)
    
    @staticmethod
    def get_by_lecturer(lecturer_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        query = """
            SELECT * FROM sessions 
            WHERE lecturer_id = %s 
            ORDER BY start_time DESC 
            LIMIT %s
        """
        return db.execute_query(query, (lecturer_id, limit))
    
    @staticmethod
    def update_token(session_id: int, token: str, token_generated_at: datetime) -> bool:
        query = """
            UPDATE sessions 
            SET current_token = %s, token_generated_at = %s 
            WHERE session_id = %s
        """
        db.execute_query(query, (token, token_generated_at, session_id))
        return True
    
    @staticmethod
    def close(session_id: int) -> bool:
        query = """
            UPDATE sessions 
            SET status = 'closed', end_time = NOW() 
            WHERE session_id = %s
        """
        db.execute_query(query, (session_id,))
        return True
    
    @staticmethod
    def get_attendance_count(session_id: int) -> int:
        query = "SELECT COUNT(*) as count FROM attendance_records WHERE session_id = %s"
        result = db.execute_query(query, (session_id,), fetch_one=True)
        return result['count'] if result else 0
    
    @staticmethod
    def get_session_attendance(session_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT ar.*, u.full_name, u.registration_number
            FROM attendance_records ar
            INNER JOIN users u ON ar.student_id = u.user_id
            WHERE ar.session_id = %s
            ORDER BY ar.marked_at ASC
        """
        return db.execute_query(query, (session_id,))
