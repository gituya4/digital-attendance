from app.database import db
from datetime import datetime
from typing import Optional, Dict, Any, List
import csv
from io import StringIO

class ReportService:
    @staticmethod
    def generate_unit_attendance_report(unit_id: int) -> str:
        """Generate CSV report for unit attendance"""
        query = """
            SELECT 
                u.registration_number,
                u.full_name,
                u.email,
                COUNT(ar.record_id) as sessions_attended,
                COUNT(s.session_id) as total_sessions,
                ROUND(COUNT(ar.record_id) / COUNT(s.session_id) * 100, 2) as attendance_percentage
            FROM enrollments e
            INNER JOIN users u ON e.student_id = u.user_id
            LEFT JOIN sessions s ON e.unit_id = s.unit_id AND s.status = 'closed'
            LEFT JOIN attendance_records ar ON s.session_id = ar.session_id AND u.user_id = ar.student_id
            WHERE e.unit_id = %s AND u.is_active = TRUE
            GROUP BY u.user_id
            ORDER BY u.full_name
        """
        students = db.execute_query(query, (unit_id,))
        
        # Get unit info
        unit_query = "SELECT * FROM units WHERE unit_id = %s"
        unit = db.execute_query(unit_query, (unit_id,), fetch_one=True)
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Unit Attendance Report'])
        writer.writerow(['Unit Code', unit['unit_code']])
        writer.writerow(['Unit Name', unit['unit_name']])
        writer.writerow(['Department', unit['department']])
        writer.writerow(['Generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow([])
        
        # Column headers
        writer.writerow(['Registration Number', 'Full Name', 'Email', 'Sessions Attended', 'Total Sessions', 'Attendance Percentage'])
        
        # Data rows
        for student in students:
            writer.writerow([
                student['registration_number'],
                student['full_name'],
                student['email'],
                student['sessions_attended'],
                student['total_sessions'],
                f"{student['attendance_percentage']}%"
            ])
        
        output.seek(0)
        return output.getvalue()
    
    @staticmethod
    def generate_student_attendance_report(student_id: int) -> str:
        """Generate CSV report for student attendance history"""
        query = """
            SELECT 
                u.unit_code,
                u.unit_name,
                s.session_id,
                s.start_time,
                s.end_time,
                ar.marked_at,
                ar.status
            FROM attendance_records ar
            INNER JOIN sessions s ON ar.session_id = s.session_id
            INNER JOIN units u ON ar.unit_id = u.unit_id
            WHERE ar.student_id = %s
            ORDER BY ar.marked_at DESC
        """
        records = db.execute_query(query, (student_id,))
        
        # Get student info
        student_query = "SELECT * FROM users WHERE user_id = %s"
        student = db.execute_query(student_query, (student_id,), fetch_one=True)
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Student Attendance Report'])
        writer.writerow(['Registration Number', student['registration_number']])
        writer.writerow(['Full Name', student['full_name']])
        writer.writerow(['Email', student['email']])
        writer.writerow(['Generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow([])
        
        # Column headers
        writer.writerow(['Unit Code', 'Unit Name', 'Session ID', 'Start Time', 'End Time', 'Marked At', 'Status'])
        
        # Data rows
        for record in records:
            writer.writerow([
                record['unit_code'],
                record['unit_name'],
                record['session_id'],
                record['start_time'].strftime('%Y-%m-%d %H:%M:%S') if record['start_time'] else 'N/A',
                record['end_time'].strftime('%Y-%m-%d %H:%M:%S') if record['end_time'] else 'N/A',
                record['marked_at'].strftime('%Y-%m-%d %H:%M:%S') if record['marked_at'] else 'N/A',
                record['status']
            ])
        
        output.seek(0)
        return output.getvalue()
    
    @staticmethod
    def generate_session_attendance_report(session_id: int) -> str:
        """Generate CSV report for a specific session"""
        query = """
            SELECT 
                u.registration_number,
                u.full_name,
                u.email,
                ar.marked_at,
                ar.status
            FROM attendance_records ar
            INNER JOIN users u ON ar.student_id = u.user_id
            WHERE ar.session_id = %s
            ORDER BY ar.marked_at ASC
        """
        records = db.execute_query(query, (session_id,))
        
        # Get session info
        session_query = """
            SELECT s.*, u.unit_code, u.unit_name 
            FROM sessions s
            INNER JOIN units u ON s.unit_id = u.unit_id
            WHERE s.session_id = %s
        """
        session = db.execute_query(session_query, (session_id,), fetch_one=True)
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Session Attendance Report'])
        writer.writerow(['Session ID', session['session_id']])
        writer.writerow(['Unit Code', session['unit_code']])
        writer.writerow(['Unit Name', session['unit_name']])
        writer.writerow(['Start Time', session['start_time'].strftime('%Y-%m-%d %H:%M:%S') if session['start_time'] else 'N/A'])
        writer.writerow(['End Time', session['end_time'].strftime('%Y-%m-%d %H:%M:%S') if session['end_time'] else 'N/A'])
        writer.writerow(['Status', session['status']])
        writer.writerow([])
        
        # Column headers
        writer.writerow(['Registration Number', 'Full Name', 'Email', 'Marked At', 'Status'])
        
        # Data rows
        for record in records:
            writer.writerow([
                record['registration_number'],
                record['full_name'],
                record['email'],
                record['marked_at'].strftime('%Y-%m-%d %H:%M:%S') if record['marked_at'] else 'N/A',
                record['status']
            ])
        
        output.seek(0)
        return output.getvalue()
    
    @staticmethod
    def get_consecutive_absences(lecturer_id: int) -> List[Dict[str, Any]]:
        """
        Get students with 3+ consecutive absences for a lecturer's units.
        Returns list of at-risk students with consecutive absence counts.
        """
        # Get all units assigned to this lecturer
        query = """
            SELECT DISTINCT u.unit_id, u.unit_code, u.unit_name
            FROM units u
            INNER JOIN lecturer_units lu ON u.unit_id = lu.unit_id
            WHERE lu.lecturer_id = %s
        """
        units = db.execute_query(query, (lecturer_id,))
        
        at_risk_students = []
        
        for unit in units:
            unit_id = unit['unit_id']
            
            # Get all closed sessions for this unit, ordered chronologically
            query = """
                SELECT session_id, start_time
                FROM sessions
                WHERE unit_id = %s AND status = 'closed'
                ORDER BY start_time ASC
            """
            sessions = db.execute_query(query, (unit_id,))
            
            if len(sessions) < 3:
                continue  # Need at least 3 sessions to track consecutive absences
            
            # Get all enrolled students in this unit
            query = """
                SELECT u.user_id, u.full_name, u.registration_number
                FROM users u
                INNER JOIN enrollments e ON u.user_id = e.student_id
                WHERE e.unit_id = %s AND u.is_active = TRUE
            """
            students = db.execute_query(query, (unit_id,))
            
            for student in students:
                student_id = student['user_id']
                
                # Walk through sessions to find consecutive absences
                current_streak = 0
                missed_dates = []
                last_attended_date = None
                
                for session in sessions:
                    session_id = session['session_id']
                    session_date = session['start_time']
                    
                    # Check if student attended this session
                    query = """
                        SELECT marked_at
                        FROM attendance_records
                        WHERE session_id = %s AND student_id = %s
                    """
                    attendance = db.execute_query(query, (session_id, student_id), fetch_one=True)
                    
                    if attendance:
                        # Student attended - reset streak
                        current_streak = 0
                        missed_dates = []
                        last_attended_date = attendance['marked_at']
                    else:
                        # Student absent - increment streak
                        current_streak += 1
                        missed_dates.append(session_date.strftime('%Y-%m-%d'))
                
                # If student has 3+ consecutive absences, add to at-risk list
                if current_streak >= 3:
                    at_risk_students.append({
                        'student_id': student_id,
                        'student_name': student['full_name'],
                        'reg_number': student['registration_number'],
                        'unit_id': unit_id,
                        'unit_code': unit['unit_code'],
                        'unit_name': unit['unit_name'],
                        'consecutive_misses': current_streak,
                        'last_attended': last_attended_date.strftime('%Y-%m-%d') if last_attended_date else 'Never attended',
                        'missed_session_dates': missed_dates[-current_streak:]  # Last N missed dates
                    })
        
        # Sort by consecutive misses descending
        at_risk_students.sort(key=lambda x: x['consecutive_misses'], reverse=True)
        
        return at_risk_students
