from app.database import db
from typing import Optional, Dict, Any, List
from datetime import datetime

class Attendance:
    @staticmethod
    def mark(session_id: int, student_id: int, unit_id: int, status: str = 'present') -> Optional[int]:
        query = """
            INSERT INTO attendance_records (session_id, student_id, unit_id, status)
            VALUES (%s, %s, %s, %s)
        """
        try:
            result = db.execute_query(query, (session_id, student_id, unit_id, status))
            return result
        except Exception:
            return None
    
    @staticmethod
    def already_marked(session_id: int, student_id: int) -> bool:
        query = "SELECT record_id FROM attendance_records WHERE session_id = %s AND student_id = %s"
        return db.execute_query(query, (session_id, student_id), fetch_one=True) is not None
    
    @staticmethod
    def get_student_attendance(student_id: int, unit_id: Optional[int] = None) -> List[Dict[str, Any]]:
        if unit_id:
            query = """
                SELECT ar.*, s.start_time, s.end_time, u.unit_code, u.unit_name
                FROM attendance_records ar
                INNER JOIN sessions s ON ar.session_id = s.session_id
                INNER JOIN units u ON ar.unit_id = u.unit_id
                WHERE ar.student_id = %s AND ar.unit_id = %s
                ORDER BY ar.marked_at DESC
            """
            return db.execute_query(query, (student_id, unit_id))
        else:
            query = """
                SELECT ar.*, s.start_time, s.end_time, u.unit_code, u.unit_name
                FROM attendance_records ar
                INNER JOIN sessions s ON ar.session_id = s.session_id
                INNER JOIN units u ON ar.unit_id = u.unit_id
                WHERE ar.student_id = %s
                ORDER BY ar.marked_at DESC
            """
            return db.execute_query(query, (student_id,))
    
    @staticmethod
    def get_unit_attendance_stats(unit_id: int) -> Dict[str, Any]:
        query = """
            SELECT 
                COUNT(DISTINCT ar.student_id) as present_count,
                COUNT(DISTINCT e.student_id) as total_enrolled,
                ROUND(COUNT(DISTINCT ar.student_id) / COUNT(DISTINCT e.student_id) * 100, 2) as percentage
            FROM enrollments e
            LEFT JOIN attendance_records ar ON e.student_id = ar.student_id AND ar.unit_id = e.unit_id
            WHERE e.unit_id = %s
        """
        result = db.execute_query(query, (unit_id,), fetch_one=True)
        return result if result else {'present_count': 0, 'total_enrolled': 0, 'percentage': 0}
    
    @staticmethod
    def get_student_unit_attendance_percentage(student_id: int, unit_id: int) -> float:
        query = """
            SELECT COUNT(*) as attendance_count
            FROM attendance_records
            WHERE student_id = %s AND unit_id = %s
        """
        result = db.execute_query(query, (student_id, unit_id), fetch_one=True)
        attendance_count = result['attendance_count'] if result else 0
        
        query = """
            SELECT COUNT(*) as session_count
            FROM sessions
            WHERE unit_id = %s AND status = 'closed'
        """
        result = db.execute_query(query, (unit_id,), fetch_one=True)
        session_count = result['session_count'] if result else 0
        
        if session_count == 0:
            return 0.0
        
        return round((attendance_count / session_count) * 100, 2)
    
    @staticmethod
    def get_at_risk_students(threshold: float = 75.0) -> List[Dict[str, Any]]:
        query = """
            SELECT 
                u.user_id, u.full_name, u.registration_number, u.email,
                un.unit_id, un.unit_code, un.unit_name,
                COUNT(ar.record_id) as attendance_count,
                COUNT(s.session_id) as total_sessions,
                ROUND(COUNT(ar.record_id) / COUNT(s.session_id) * 100, 2) as percentage
            FROM users u
            INNER JOIN enrollments e ON u.user_id = e.student_id
            INNER JOIN units un ON e.unit_id = un.unit_id
            LEFT JOIN sessions s ON un.unit_id = s.unit_id AND s.status = 'closed'
            LEFT JOIN attendance_records ar ON u.user_id = ar.student_id AND s.session_id = ar.session_id
            WHERE u.role = 'student' AND u.is_active = TRUE
            GROUP BY u.user_id, un.unit_id
            HAVING percentage < %s OR percentage IS NULL
            ORDER BY percentage ASC
        """
        return db.execute_query(query, (threshold,))
