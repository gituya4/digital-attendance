from app.database import db
from typing import Optional, Dict, Any, List

class Unit:
    @staticmethod
    def create(unit_code: str, unit_name: str, department: str, 
               semester: str, academic_year: str) -> Optional[int]:
        query = """
            INSERT INTO units (unit_code, unit_name, department, semester, academic_year)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            result = db.execute_query(query, (unit_code, unit_name, department, semester, academic_year))
            return result
        except Exception:
            return None
    
    @staticmethod
    def get_by_id(unit_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM units WHERE unit_id = %s"
        return db.execute_query(query, (unit_id,), fetch_one=True)
    
    @staticmethod
    def get_by_code(unit_code: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM units WHERE unit_code = %s"
        return db.execute_query(query, (unit_code,), fetch_one=True)
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        query = "SELECT * FROM units ORDER BY unit_code"
        return db.execute_query(query)
    
    @staticmethod
    def code_exists(unit_code: str) -> bool:
        query = "SELECT unit_id FROM units WHERE unit_code = %s"
        return db.execute_query(query, (unit_code,), fetch_one=True) is not None
    
    @staticmethod
    def assign_lecturer(lecturer_id: int, unit_id: int) -> bool:
        # Check if already assigned
        query = "SELECT id FROM lecturer_units WHERE lecturer_id = %s AND unit_id = %s"
        existing = db.execute_query(query, (lecturer_id, unit_id), fetch_one=True)
        if existing:
            return True  # Already assigned, consider it success
        
        # Insert new assignment
        query = "INSERT INTO lecturer_units (lecturer_id, unit_id) VALUES (%s, %s)"
        try:
            db.execute_query(query, (lecturer_id, unit_id))
            return True
        except Exception:
            return False
    
    @staticmethod
    def remove_lecturer(lecturer_id: int, unit_id: int) -> bool:
        query = "DELETE FROM lecturer_units WHERE lecturer_id = %s AND unit_id = %s"
        db.execute_query(query, (lecturer_id, unit_id))
        return True
    
    @staticmethod
    def get_lecturer_units(lecturer_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT u.* FROM units u
            INNER JOIN lecturer_units lu ON u.unit_id = lu.unit_id
            WHERE lu.lecturer_id = %s
            ORDER BY u.unit_code
        """
        return db.execute_query(query, (lecturer_id,))
    
    @staticmethod
    def enroll_student(student_id: int, unit_id: int) -> bool:
        query = "INSERT INTO enrollments (student_id, unit_id) VALUES (%s, %s)"
        try:
            db.execute_query(query, (student_id, unit_id))
            return True
        except Exception:
            return False
    
    @staticmethod
    def unenroll_student(student_id: int, unit_id: int) -> bool:
        query = "DELETE FROM enrollments WHERE student_id = %s AND unit_id = %s"
        db.execute_query(query, (student_id, unit_id))
        return True
    
    @staticmethod
    def get_student_units(student_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT u.* FROM units u
            INNER JOIN enrollments e ON u.unit_id = e.unit_id
            WHERE e.student_id = %s
            ORDER BY u.unit_code
        """
        return db.execute_query(query, (student_id,))
    
    @staticmethod
    def get_enrolled_students(unit_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT u.* FROM users u
            INNER JOIN enrollments e ON u.user_id = e.student_id
            WHERE e.unit_id = %s AND u.is_active = TRUE
            ORDER BY u.full_name
        """
        return db.execute_query(query, (unit_id,))
    
    @staticmethod
    def is_student_enrolled(student_id: int, unit_id: int) -> bool:
        query = "SELECT id FROM enrollments WHERE student_id = %s AND unit_id = %s"
        return db.execute_query(query, (student_id, unit_id), fetch_one=True) is not None
