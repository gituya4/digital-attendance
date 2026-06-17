from flask import request, jsonify, Response, render_template
from flask_jwt_extended import jwt_required, get_jwt
from app.routes import lecturer_bp, lecturer_pages_bp
from app.models.user import User
from app.models.unit import Unit
from app.models.session import Session
from app.models.attendance import Attendance
from app.services.qr_service import QRService
from app.services.report_service import ReportService
from app.utils import role_required, write_audit_log
from datetime import datetime
from app.config import Config
from app.database import db
import csv
from io import StringIO

@lecturer_bp.route('/units', methods=['GET'])
@jwt_required()
@role_required('lecturer')
def get_units():
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    print(f"DEBUG: Loading units for lecturer_id: {lecturer_id}")
    
    units = Unit.get_lecturer_units(lecturer_id)
    print(f"DEBUG: Found {len(units)} units for lecturer")
    
    # Enrich each unit with stats
    units_with_stats = []
    for unit in units:
        unit_id = unit['unit_id']
        
        # Get enrolled count
        query = "SELECT COUNT(*) as count FROM enrollments WHERE unit_id = %s"
        enrolled = db.execute_query(query, (unit_id,), fetch_one=True)['count']
        
        # Get total sessions
        query = "SELECT COUNT(*) as count FROM sessions WHERE unit_id = %s"
        total_sessions = db.execute_query(query, (unit_id,), fetch_one=True)['count']
        
        # Get average attendance percentage
        query = """
            SELECT AVG(percentage) as avg_pct
            FROM (
                SELECT 
                    s.session_id,
                    (COUNT(ar.record_id) / COUNT(DISTINCT e.student_id) * 100) as percentage
                FROM sessions s
                LEFT JOIN enrollments e ON s.unit_id = e.unit_id
                LEFT JOIN attendance_records ar ON s.session_id = ar.session_id
                WHERE s.unit_id = %s AND s.status = 'closed'
                GROUP BY s.session_id
            ) as session_stats
        """
        avg_attendance = db.execute_query(query, (unit_id,), fetch_one=True)
        avg_pct = round(avg_attendance['avg_pct'], 2) if avg_attendance and avg_attendance['avg_pct'] else 0
        
        # Check for active session
        query = "SELECT session_id FROM sessions WHERE unit_id = %s AND status = 'active'"
        active_session = db.execute_query(query, (unit_id,), fetch_one=True)
        has_active = active_session is not None
        active_session_id = active_session['session_id'] if has_active else None
        
        units_with_stats.append({
            'unit_id': unit['unit_id'],
            'unit_code': unit['unit_code'],
            'unit_name': unit['unit_name'],
            'enrolled_count': enrolled,
            'total_sessions': total_sessions,
            'avg_attendance_pct': avg_pct,
            'has_active_session': has_active,
            'active_session_id': active_session_id
        })
    
    return jsonify({
        'success': True,
        'units': units_with_stats
    }), 200

# Render session page with QR code
@lecturer_pages_bp.route('/sessions/<int:session_id>', methods=['GET'])
@jwt_required()
@role_required('lecturer')
def session_page(session_id):
    print(f"DEBUG: Session page requested for session_id: {session_id}")
    
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    print(f"DEBUG: Lecturer ID: {lecturer_id}")
    
    session = Session.get_by_id(session_id)
    print(f"DEBUG: Session data: {session}")
    
    if not session:
        print(f"DEBUG: Session not found")
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    if int(session['lecturer_id']) != int(lecturer_id):
        print(f"DEBUG: Access forbidden - session lecturer_id: {session['lecturer_id']}, current lecturer_id: {lecturer_id}")
        return jsonify({'success': False, 'error': 'Access forbidden'}), 403
    
    unit = Unit.get_by_id(session['unit_id'])
    print(f"DEBUG: Unit data: {unit}")
    
    print(f"DEBUG: Rendering session page")
    return render_template('lecturer/session.html', session=session, unit=unit)

@lecturer_bp.route('/sessions/start', methods=['POST'])
@jwt_required()
@role_required('lecturer')
def start_session():
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    unit_id = data.get('unit_id')
    
    if not unit_id:
        return jsonify({'success': False, 'error': 'Unit ID is required'}), 400
    
    try:
        unit_id = int(unit_id)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Invalid unit ID'}), 400
    
    unit = Unit.get_by_id(unit_id)
    if not unit:
        return jsonify({'success': False, 'error': 'Unit not found'}), 404
    
    # Check if lecturer already has an active session for any unit
    query = "SELECT session_id FROM sessions WHERE lecturer_id = %s AND status = 'active'"
    active_session = db.execute_query(query, (lecturer_id,), fetch_one=True)
    if active_session:
        print(f"DEBUG: Lecturer already has active session: {active_session}")
        return jsonify({'success': False, 'error': 'You already have an active session. Please close it before starting a new one.'}), 400
    
    # Check if unit already has an active session
    active_session = Session.get_active_by_unit(unit_id)
    if active_session:
        return jsonify({'success': False, 'error': 'A session is already running for this unit.'}), 400
    
    pin = QRService.generate_pin()
    now = datetime.utcnow()
    token = QRService.generate_token(0, now, Config.HMAC_SECRET_KEY)
    
    session_id = Session.create(unit_id, lecturer_id, pin, token, now)
    print(f"DEBUG: Session created with ID: {session_id}")
    
    if not session_id:
        return jsonify({'success': False, 'error': 'Failed to create session'}), 500
    
    token = QRService.generate_token(session_id, now, Config.HMAC_SECRET_KEY)
    Session.update_token(session_id, token, now)
    
    write_audit_log(lecturer_id, 'session_started', f'Session started for unit {unit_id}')
    return jsonify({
        'success': True,
        'message': 'Session started successfully',
        'session': {
            'session_id': session_id,
            'unit_id': unit_id,
            'pin': pin,
            'token': token,
            'start_time': now.isoformat()
        }
    }), 201

@lecturer_bp.route('/sessions/<int:session_id>/qr', methods=['GET'])
@jwt_required()
@role_required('lecturer')
def get_qr_token(session_id):
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    session = Session.get_by_id(session_id)
    if not session:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    if int(session['lecturer_id']) != int(lecturer_id):
        return jsonify({'success': False, 'error': 'Access forbidden'}), 403
    
    now = datetime.utcnow()
    token_generated = session['token_generated_at']
    
    if (now - token_generated).total_seconds() > 30:
        token = QRService.generate_token(session_id, now, Config.HMAC_SECRET_KEY)
        Session.update_token(session_id, token, now)
    else:
        token = session['current_token']
    
    qr_base64 = QRService.generate_qr_base64(token)
    
    return jsonify({
        'success': True,
        'qr': {
            'token': token,
            'qr_image': qr_base64,
            'pin': session['session_pin'],
            'expires_in': 30 - int((now - token_generated).total_seconds())
        }
    }), 200

@lecturer_pages_bp.route('/sessions/<int:session_id>/live', methods=['GET'])
@jwt_required()
@role_required('lecturer')
def get_live_attendance(session_id):
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    session = Session.get_by_id(session_id)
    if not session:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    if int(session['lecturer_id']) != int(lecturer_id):
        return jsonify({'success': False, 'error': 'Access forbidden'}), 403
    
    attendance = Session.get_session_attendance(session_id)
    
    def generate():
        yield f"data: {{'success': true, 'attendance': {attendance}}}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@lecturer_bp.route('/sessions/<int:session_id>/close', methods=['POST'])
@jwt_required()
@role_required('lecturer')
def close_session(session_id):
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    session = Session.get_by_id(session_id)
    if not session:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    if int(session['lecturer_id']) != int(lecturer_id):
        return jsonify({'success': False, 'error': 'Access forbidden'}), 403
    
    if session['status'] == 'closed':
        return jsonify({'success': False, 'error': 'Session is already closed'}), 400
    
    Session.close(session_id)
    write_audit_log(lecturer_id, 'session_ended', f'Session {session_id} ended')
    
    attendance = Session.get_session_attendance(session_id)
    unit = Unit.get_by_id(session['unit_id'])
    enrolled = Unit.get_enrolled_students(session['unit_id'])
    
    return jsonify({
        'success': True,
        'message': 'Session closed successfully',
        'summary': {
            'session_id': session_id,
            'unit': unit,
            'attendance_count': len(attendance),
            'total_enrolled': len(enrolled),
            'percentage': round((len(attendance) / len(enrolled) * 100) if enrolled else 0, 2)
        }
    }), 200

@lecturer_bp.route('/sessions/<int:session_id>/export', methods=['GET'])
@jwt_required()
@role_required('lecturer')
def export_attendance(session_id):
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    session = Session.get_by_id(session_id)
    if not session:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    if int(session['lecturer_id']) != int(lecturer_id):
        return jsonify({'success': False, 'error': 'Access forbidden'}), 403
    
    attendance = Session.get_session_attendance(session_id)
    unit = Unit.get_by_id(session['unit_id'])
    
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Attendance Report'])
    writer.writerow(['Unit Code', unit['unit_code']])
    writer.writerow(['Unit Name', unit['unit_name']])
    writer.writerow(['Session ID', session_id])
    writer.writerow(['Start Time', session['start_time']])
    writer.writerow(['End Time', session['end_time']])
    writer.writerow([])
    
    writer.writerow(['Registration Number', 'Full Name', 'Marked At', 'Status'])
    for record in attendance:
        writer.writerow([
            record['registration_number'],
            record['full_name'],
            record['marked_at'],
            record['status']
        ])
    
    output.seek(0)
    
    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename=attendance_{session_id}.csv'
    
    return response, 200

@lecturer_bp.route('/sessions', methods=['GET'])
@jwt_required()
@role_required('lecturer')
def get_sessions():
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    query = """
        SELECT s.*, u.unit_code, u.unit_name,
               COUNT(ar.record_id) as attendance_count,
               COUNT(DISTINCT e.student_id) as total_enrolled
        FROM sessions s
        INNER JOIN units u ON s.unit_id = u.unit_id
        LEFT JOIN attendance_records ar ON s.session_id = ar.session_id
        LEFT JOIN enrollments e ON s.unit_id = e.unit_id
        WHERE s.lecturer_id = %s
        GROUP BY s.session_id
        ORDER BY s.start_time DESC
    """
    sessions = db.execute_query(query, (lecturer_id,))
    
    sessions_data = []
    for session in sessions:
        sessions_data.append({
            'session_id': session['session_id'],
            'unit_code': session['unit_code'],
            'unit_name': session['unit_name'],
            'start_time': session['start_time'].isoformat() if session['start_time'] else None,
            'end_time': session['end_time'].isoformat() if session['end_time'] else None,
            'status': session['status'],
            'attendance_count': session['attendance_count'],
            'total_enrolled': session['total_enrolled'],
            'percentage': round((session['attendance_count'] / session['total_enrolled'] * 100) if session['total_enrolled'] else 0, 2)
        })
    
    return jsonify({
        'success': True,
        'sessions': sessions_data
    }), 200

@lecturer_bp.route('/units/<int:unit_id>/export', methods=['GET'])
@jwt_required()
@role_required('lecturer')
def export_unit_attendance(unit_id):
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    # Verify lecturer is assigned to this unit
    unit = Unit.get_by_id(unit_id)
    if not unit:
        return jsonify({'success': False, 'error': 'Unit not found'}), 404
    
    lecturer_units = Unit.get_lecturer_units(lecturer_id)
    if not any(u['unit_id'] == unit_id for u in lecturer_units):
        return jsonify({'success': False, 'error': 'Access forbidden'}), 403
    
    from app.services.report_service import ReportService
    csv_data = ReportService.generate_unit_attendance_report(unit_id)
    
    response = Response(csv_data, mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename=unit_{unit_id}_attendance.csv'
    return response, 200

@lecturer_bp.route('/stats', methods=['GET'])
@jwt_required()
@role_required('lecturer')
def get_stats():
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    # Total units
    units = Unit.get_lecturer_units(lecturer_id)
    total_units = len(units)
    
    # Sessions this week
    query = """
        SELECT COUNT(*) as count
        FROM sessions
        WHERE lecturer_id = %s AND YEARWEEK(start_time) = YEARWEEK(NOW())
    """
    sessions_this_week = db.execute_query(query, (lecturer_id,), fetch_one=True)['count']
    
    # Students marked today
    query = """
        SELECT COUNT(DISTINCT ar.student_id) as count
        FROM attendance_records ar
        INNER JOIN sessions s ON ar.session_id = s.session_id
        WHERE s.lecturer_id = %s AND DATE(ar.marked_at) = CURDATE()
    """
    students_today = db.execute_query(query, (lecturer_id,), fetch_one=True)['count']
    
    # Average attendance rate
    query = """
        SELECT AVG(percentage) as avg_rate
        FROM (
            SELECT 
                s.session_id,
                (COUNT(ar.record_id) / COUNT(DISTINCT e.student_id) * 100) as percentage
            FROM sessions s
            INNER JOIN enrollments e ON s.unit_id = e.unit_id
            LEFT JOIN attendance_records ar ON s.session_id = ar.session_id
            WHERE s.lecturer_id = %s AND s.status = 'closed'
            GROUP BY s.session_id
        ) as session_stats
    """
    avg_attendance = db.execute_query(query, (lecturer_id,), fetch_one=True)
    avg_rate = round(avg_attendance['avg_rate'], 2) if avg_attendance and avg_attendance['avg_rate'] else 0
    
    return jsonify({
        'success': True,
        'stats': {
            'total_units': total_units,
            'sessions_this_week': sessions_this_week,
            'students_today': students_today,
            'average_attendance': avg_rate
        }
    }), 200

@lecturer_bp.route('/sessions/<int:session_id>/manual-mark', methods=['POST'])
@jwt_required()
@role_required('lecturer')
def manual_mark_attendance(session_id):
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    student_id = data.get('student_id', type=int)
    reason = data.get('reason', '').strip()
    
    if not student_id:
        return jsonify({'success': False, 'error': 'Student ID is required'}), 400
    
    if not reason or len(reason) < 10:
        return jsonify({'success': False, 'error': 'Reason is required and must be at least 10 characters'}), 400
    
    # Get session
    session = Session.get_by_id(session_id)
    if not session:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    # Check session belongs to lecturer's unit
    query = "SELECT * FROM lecturer_units WHERE lecturer_id = %s AND unit_id = %s"
    lecturer_unit = db.execute_query(query, (lecturer_id, session['unit_id']), fetch_one=True)
    if not lecturer_unit:
        return jsonify({'success': False, 'error': 'You do not have permission for this session'}), 403
    
    # Check student is enrolled in the unit
    if not Unit.is_student_enrolled(student_id, session['unit_id']):
        return jsonify({'success': False, 'error': 'Student is not enrolled in this unit'}), 400
    
    # Check student doesn't already have attendance for this session
    if Attendance.already_marked(session_id, student_id):
        return jsonify({'success': False, 'error': 'Student already has attendance for this session'}), 400
    
    # Get student info for audit log
    student = User.get_by_id(student_id)
    unit = Unit.get_by_id(session['unit_id'])
    
    # Mark attendance as manual
    result = Attendance.mark(session_id, student_id, session['unit_id'], 'manual')
    
    if result:
        write_audit_log(lecturer_id, 'MANUAL_ATTENDANCE_MARKED', 
                      f'Manually marked {student["full_name"]} ({student["registration_number"]}) for {unit["unit_code"]}. Reason: {reason}')
        return jsonify({
            'success': True,
            'student_name': student['full_name']
        }), 201
    else:
        return jsonify({'success': False, 'error': 'Failed to mark attendance'}), 500

@lecturer_bp.route('/sessions/<int:session_id>/students/not-marked', methods=['GET'])
@jwt_required()
@role_required('lecturer')
def get_not_marked_students(session_id):
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    # Get session
    session = Session.get_by_id(session_id)
    if not session:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    # Check session belongs to lecturer's unit
    query = "SELECT * FROM lecturer_units WHERE lecturer_id = %s AND unit_id = %s"
    lecturer_unit = db.execute_query(query, (lecturer_id, session['unit_id']), fetch_one=True)
    if not lecturer_unit:
        return jsonify({'success': False, 'error': 'Access forbidden'}), 403
    
    # Get students enrolled in unit who haven't marked attendance for this session
    query = """
        SELECT u.user_id, u.full_name, u.registration_number, u.email
        FROM users u
        INNER JOIN enrollments e ON u.user_id = e.student_id
        WHERE e.unit_id = %s AND u.is_active = TRUE
        AND u.user_id NOT IN (
            SELECT student_id FROM attendance_records WHERE session_id = %s
        )
        ORDER BY u.full_name
    """
    students = db.execute_query(query, (session['unit_id'], session_id))
    
    return jsonify({
        'success': True,
        'students': students
    }), 200

@lecturer_bp.route('/at-risk', methods=['GET'])
@jwt_required()
@role_required('lecturer')
def get_at_risk_students():
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    at_risk_students = ReportService.get_consecutive_absences(lecturer_id)
    
    return jsonify({
        'success': True,
        'at_risk_students': at_risk_students
    }), 200

@lecturer_bp.route('/notify/<int:student_id>', methods=['POST'])
@jwt_required()
@role_required('lecturer')
def notify_student(student_id):
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    unit_id = data.get('unit_id')
    if unit_id:
        unit_id = int(unit_id)
    message = data.get('message', '').strip()
    
    if not unit_id:
        return jsonify({'success': False, 'error': 'Unit ID is required'}), 400
    
    if not message:
        return jsonify({'success': False, 'error': 'Message is required'}), 400
    
    # Verify lecturer is assigned to this unit
    query = "SELECT * FROM lecturer_units WHERE lecturer_id = %s AND unit_id = %s"
    lecturer_unit = db.execute_query(query, (lecturer_id, unit_id), fetch_one=True)
    if not lecturer_unit:
        return jsonify({'success': False, 'error': 'You are not assigned to this unit'}), 403
    
    # Verify student is enrolled in this unit
    if not Unit.is_student_enrolled(student_id, unit_id):
        return jsonify({'success': False, 'error': 'Student is not enrolled in this unit'}), 400
    
    # Create notification
    query = """
        INSERT INTO notifications (from_user_id, to_user_id, unit_id, message, type)
        VALUES (%s, %s, %s, %s, 'absence_warning')
    """
    db.execute_query(query, (lecturer_id, student_id, unit_id, message))
    
    write_audit_log(lecturer_id, 'STUDENT_NOTIFIED', f'Notified student {student_id} for unit {unit_id}')
    
    return jsonify({
        'success': True
    }), 201

@lecturer_bp.route('/sessions/<int:session_id>/notes', methods=['PUT'])
@jwt_required()
@role_required('lecturer')
def update_session_notes(session_id):
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    notes = data.get('notes', '')
    
    # Get session
    session = Session.get_by_id(session_id)
    if not session:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    # Verify session belongs to lecturer
    if int(session['lecturer_id']) != int(lecturer_id):
        return jsonify({'success': False, 'error': 'Access forbidden'}), 403
    
    # Update session notes
    query = "UPDATE sessions SET session_notes = %s WHERE session_id = %s"
    db.execute_query(query, (notes, session_id))
    
    return jsonify({
        'success': True
    }), 200

@lecturer_bp.route('/sessions/<int:session_id>/summary', methods=['GET'])
@jwt_required()
@role_required('lecturer')
def get_session_summary(session_id):
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    # Get session
    session = Session.get_by_id(session_id)
    if not session:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    # Verify session belongs to lecturer
    if int(session['lecturer_id']) != int(lecturer_id):
        return jsonify({'success': False, 'error': 'Access forbidden'}), 403
    
    # Get unit info
    unit = Unit.get_by_id(session['unit_id'])
    
    # Get total enrolled
    query = "SELECT COUNT(*) as count FROM enrollments WHERE unit_id = %s"
    total_enrolled = db.execute_query(query, (session['unit_id'],), fetch_one=True)['count']
    
    # Get attendance records
    query = """
        SELECT ar.marked_at, ar.status, u.full_name, u.registration_number
        FROM attendance_records ar
        INNER JOIN users u ON ar.student_id = u.user_id
        WHERE ar.session_id = %s
        ORDER BY ar.marked_at ASC
    """
    attendance = db.execute_query(query, (session_id,))
    
    present_count = len([r for r in attendance if r['status'] == 'present'])
    manual_count = len([r for r in attendance if r['status'] == 'manual'])
    absent_count = total_enrolled - present_count - manual_count
    
    # Calculate duration
    duration_minutes = 0
    if session['start_time'] and session['end_time']:
        duration = session['end_time'] - session['start_time']
        duration_minutes = int(duration.total_seconds() / 60)
    
    # Get first and last arrival
    first_arrival = None
    last_arrival = None
    if attendance:
        first_arrival = attendance[0]['marked_at'].strftime('%H:%M:%S')
        last_arrival = attendance[-1]['marked_at'].strftime('%H:%M:%S')
    
    # Get absent students
    query = """
        SELECT u.full_name, u.registration_number
        FROM users u
        INNER JOIN enrollments e ON u.user_id = e.student_id
        WHERE e.unit_id = %s AND u.is_active = TRUE
        AND u.user_id NOT IN (
            SELECT student_id FROM attendance_records WHERE session_id = %s
        )
    """
    absent_students = db.execute_query(query, (session['unit_id'], session_id))
    
    # Calculate attendance percentage
    attendance_pct = 0
    if total_enrolled > 0:
        attendance_pct = round(((present_count + manual_count) / total_enrolled) * 100, 1)
    
    return jsonify({
        'success': True,
        'summary': {
            'unit_name': unit['unit_name'] if unit else 'Unknown',
            'date': session['start_time'].strftime('%Y-%m-%d') if session['start_time'] else None,
            'duration_minutes': duration_minutes,
            'total_enrolled': total_enrolled,
            'present_count': present_count,
            'manual_count': manual_count,
            'absent_count': absent_count,
            'attendance_pct': attendance_pct,
            'first_arrival': first_arrival,
            'last_arrival': last_arrival,
            'absent_students': absent_students
        }
    }), 200

@lecturer_bp.route('/analytics', methods=['GET'])
@jwt_required()
@role_required('lecturer')
def get_analytics():
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    # Get all units for this lecturer
    units = Unit.get_lecturer_units(lecturer_id)
    
    units_data = []
    total_sessions = 0
    overall_avg_sum = 0
    
    for unit in units:
        unit_id = unit['unit_id']
        
        # Get total sessions for this unit
        query = "SELECT COUNT(*) as count FROM sessions WHERE unit_id = %s AND status = 'closed'"
        unit_total_sessions = db.execute_query(query, (unit_id,), fetch_one=True)['count']
        total_sessions += unit_total_sessions
        
        # Get average attendance for this unit
        query = """
            SELECT AVG(percentage) as avg_pct
            FROM (
                SELECT 
                    (COUNT(ar.record_id) / COUNT(DISTINCT e.student_id) * 100) as percentage
                FROM sessions s
                LEFT JOIN enrollments e ON s.unit_id = e.unit_id
                LEFT JOIN attendance_records ar ON s.session_id = ar.session_id
                WHERE s.unit_id = %s AND s.status = 'closed'
                GROUP BY s.session_id
            ) as session_stats
        """
        avg_attendance = db.execute_query(query, (unit_id,), fetch_one=True)
        avg_pct = round(avg_attendance['avg_pct'], 2) if avg_attendance and avg_attendance['avg_pct'] else 0
        overall_avg_sum += avg_pct
        
        # Get best and worst session percentages
        query = """
            SELECT 
                (COUNT(ar.record_id) / COUNT(DISTINCT e.student_id) * 100) as percentage
            FROM sessions s
            LEFT JOIN enrollments e ON s.unit_id = e.unit_id
            LEFT JOIN attendance_records ar ON s.session_id = ar.session_id
            WHERE s.unit_id = %s AND s.status = 'closed'
            GROUP BY s.session_id
            ORDER BY percentage DESC
            LIMIT 1
        """
        best_session = db.execute_query(query, (unit_id,), fetch_one=True)
        best_pct = round(best_session['percentage'], 2) if best_session and best_session['percentage'] else 0
        
        query = """
            SELECT 
                (COUNT(ar.record_id) / COUNT(DISTINCT e.student_id) * 100) as percentage
            FROM sessions s
            LEFT JOIN enrollments e ON s.unit_id = e.unit_id
            LEFT JOIN attendance_records ar ON s.session_id = ar.session_id
            WHERE s.unit_id = %s AND s.status = 'closed'
            GROUP BY s.session_id
            ORDER BY percentage ASC
            LIMIT 1
        """
        worst_session = db.execute_query(query, (unit_id,), fetch_one=True)
        worst_pct = round(worst_session['percentage'], 2) if worst_session and worst_session['percentage'] else 0
        
        # Calculate trend (last 3 vs previous 3 sessions)
        query = """
            SELECT 
                s.session_id,
                (COUNT(ar.record_id) / COUNT(DISTINCT e.student_id) * 100) as percentage
            FROM sessions s
            LEFT JOIN enrollments e ON s.unit_id = e.unit_id
            LEFT JOIN attendance_records ar ON s.session_id = ar.session_id
            WHERE s.unit_id = %s AND s.status = 'closed'
            GROUP BY s.session_id
            ORDER BY s.start_time DESC
            LIMIT 6
        """
        recent_sessions = db.execute_query(query, (unit_id,))
        
        trend = 'stable'
        if len(recent_sessions) >= 6:
            last_3_avg = sum([s['percentage'] for s in recent_sessions[:3] if s['percentage']]) / 3
            prev_3_avg = sum([s['percentage'] for s in recent_sessions[3:6] if s['percentage']]) / 3
            
            if last_3_avg > prev_3_avg + 5:
                trend = 'improving'
            elif last_3_avg < prev_3_avg - 5:
                trend = 'declining'
        
        # Get sessions over time (last 10)
        query = """
            SELECT 
                DATE(s.start_time) as date,
                (COUNT(ar.record_id) / COUNT(DISTINCT e.student_id) * 100) as pct
            FROM sessions s
            LEFT JOIN enrollments e ON s.unit_id = e.unit_id
            LEFT JOIN attendance_records ar ON s.session_id = ar.session_id
            WHERE s.unit_id = %s AND s.status = 'closed'
            GROUP BY DATE(s.start_time)
            ORDER BY DATE(s.start_time) DESC
            LIMIT 10
        """
        sessions_over_time = db.execute_query(query, (unit_id,))
        sessions_over_time.reverse()  # Order ascending
        
        units_data.append({
            'unit_code': unit['unit_code'],
            'unit_name': unit['unit_name'],
            'total_sessions': unit_total_sessions,
            'avg_attendance_pct': avg_pct,
            'trend': trend,
            'best_session_pct': best_pct,
            'worst_session_pct': worst_pct,
            'sessions_over_time': [{'date': str(s['date']), 'pct': round(s['pct'], 1)} for s in sessions_over_time]
        })
    
    # Calculate overall stats
    overall_avg = round(overall_avg_sum / len(units), 2) if units else 0
    
    # Find most engaged and most at-risk units
    most_engaged = max(units_data, key=lambda x: x['avg_attendance_pct']) if units_data else None
    most_at_risk = min(units_data, key=lambda x: x['avg_attendance_pct']) if units_data else None
    
    return jsonify({
        'success': True,
        'analytics': {
            'units': units_data,
            'overall_avg': overall_avg,
            'total_sessions_this_semester': total_sessions,
            'most_engaged_unit': most_engaged['unit_code'] if most_engaged else None,
            'most_at_risk_unit': most_at_risk['unit_code'] if most_at_risk else None
        }
    }), 200

# Endpoint for lecturer to update their profile
@lecturer_bp.route('/profile', methods=['PUT'])
@jwt_required()
@role_required('lecturer')
def update_profile():
    claims = get_jwt()
    lecturer_id = claims.get('sub')
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    full_name = data.get('full_name', '').strip()
    email = data.get('email', '').strip()
    department = data.get('department', '').strip()
    staff_id = data.get('staff_id', '').strip()
    
    if not full_name:
        return jsonify({'success': False, 'error': 'Full name is required'}), 400
    
    if email and email != claims.get('email'):
        if User.email_exists(email):
            return jsonify({'success': False, 'error': 'Email already in use'}), 400
    
    if staff_id and staff_id != claims.get('staff_id'):
        if User.staff_id_exists(staff_id):
            return jsonify({'success': False, 'error': 'Staff ID already in use'}), 400
    
    # Update lecturer profile
    update_fields = {'full_name': full_name}
    if email:
        update_fields['email'] = email
    if department:
        update_fields['department'] = department
    if staff_id:
        update_fields['staff_id'] = staff_id
    
    if password := data.get('password', '').strip():
        update_fields['password'] = password
    
    if User.update(lecturer_id, update_fields):
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully'
        }), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to update profile'}), 500
