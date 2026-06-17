from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.routes import student_bp
from app.models.user import User
from app.models.unit import Unit
from app.models.session import Session
from app.models.attendance import Attendance
from app.services.qr_service import QRService
from app.utils import role_required, write_audit_log
from app.database import db
from datetime import datetime, timedelta
from app.config import Config

@student_bp.route('/units', methods=['GET'])
@jwt_required()
@role_required('student')
def get_units():
    claims = get_jwt()
    student_id = claims.get('sub')
    
    units = Unit.get_student_units(student_id)
    
    units_with_stats = []
    for unit in units:
        stats = Attendance.get_student_unit_attendance_percentage(student_id, unit['unit_id'])
        units_with_stats.append({
            'unit_id': unit['unit_id'],
            'unit_code': unit['unit_code'],
            'unit_name': unit['unit_name'],
            'department': unit['department'],
            'semester': unit['semester'],
            'academic_year': unit['academic_year'],
            'attendance_percentage': stats
        })
    
    return jsonify({
        'success': True,
        'units': units_with_stats
    }), 200

@student_bp.route('/attendance', methods=['GET'])
@jwt_required()
@role_required('student')
def get_attendance():
    claims = get_jwt()
    student_id = claims.get('sub')
    
    unit_id = request.args.get('unit_id', type=int)
    
    records = Attendance.get_student_attendance(student_id, unit_id)
    
    attendance_data = []
    for record in records:
        attendance_data.append({
            'record_id': record['record_id'],
            'session_id': record['session_id'],
            'unit_code': record['unit_code'],
            'unit_name': record['unit_name'],
            'marked_at': record['marked_at'].isoformat() if record['marked_at'] else None,
            'status': record['status']
        })
    
    return jsonify({
        'success': True,
        'attendance': attendance_data
    }), 200

@student_bp.route('/mark', methods=['POST'])
@jwt_required()
@role_required('student')
def mark_attendance():
    claims = get_jwt()
    student_id = claims.get('sub')
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    token = data.get('token', '').strip()
    pin = data.get('pin', '').strip()
    
    if not token or not pin:
        return jsonify({'success': False, 'error': 'Token and PIN are required'}), 400
    
    is_valid, payload = QRService.verify_token(token, Config.HMAC_SECRET_KEY)
    if not is_valid:
        print(f"DEBUG: Invalid QR code - token: {token[:20]}...")
        return jsonify({'success': False, 'error': 'Invalid QR code'}), 400
    
    session_id = payload.get('session_id')
    token_timestamp = datetime.fromisoformat(payload.get('timestamp'))
    
    now = datetime.utcnow()
    if (now - token_timestamp).total_seconds() > 30:
        print(f"DEBUG: QR expired - token age: {(now - token_timestamp).total_seconds()}s")
        return jsonify({'success': False, 'error': 'QR code has expired. Please scan the latest code.'}), 400
    
    session = Session.get_by_id(session_id)
    if not session:
        print(f"DEBUG: Session not found - session_id: {session_id}")
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    if session['status'] != 'active':
        print(f"DEBUG: Session not active - status: {session['status']}")
        return jsonify({'success': False, 'error': 'This session has ended'}), 400
    
    if session['session_pin'] != pin:
        print(f"DEBUG: Incorrect PIN - provided: {pin}, expected: {session['session_pin']}")
        return jsonify({'success': False, 'error': 'Incorrect PIN'}), 400
    
    if Attendance.already_marked(session_id, student_id):
        print(f"DEBUG: Already marked - session_id: {session_id}, student_id: {student_id}")
        return jsonify({'success': False, 'error': 'Attendance already recorded for this session'}), 400
    
    if not Unit.is_student_enrolled(student_id, session['unit_id']):
        print(f"DEBUG: Not enrolled - student_id: {student_id}, unit_id: {session['unit_id']}")
        return jsonify({'success': False, 'error': 'You are not enrolled in this unit'}), 400
    
    result = Attendance.mark(session_id, student_id, session['unit_id'])
    if result:
        write_audit_log(student_id, 'attendance_marked', f'Attendance marked for session {session_id}')
        return jsonify({
            'success': True,
            'message': 'Attendance marked successfully',
            'session_id': session_id
        }), 201
    else:
        return jsonify({'success': False, 'error': 'Failed to mark attendance'}), 500

@student_bp.route('/request', methods=['POST'])
@jwt_required()
@role_required('student')
def submit_correction_request():
    claims = get_jwt()
    student_id = claims.get('sub')
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    session_id = data.get('session_id', type=int)
    reason = data.get('reason', '').strip()
    
    if not session_id or not reason:
        return jsonify({'success': False, 'error': 'Session ID and reason are required'}), 400
    
    session = Session.get_by_id(session_id)
    if not session:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    # Check for duplicate request
    query = """
        SELECT request_id FROM correction_requests 
        WHERE student_id = %s AND session_id = %s AND status = 'pending'
    """
    from app.database import db
    existing = db.execute_query(query, (student_id, session_id), fetch_one=True)
    if existing:
        return jsonify({'success': False, 'error': 'You already have a pending request for this session'}), 400
    
    query = """
        INSERT INTO correction_requests (student_id, session_id, reason)
        VALUES (%s, %s, %s)
    """
    try:
        db.execute_query(query, (student_id, session_id, reason))
        return jsonify({
            'success': True,
            'message': 'Correction request submitted successfully'
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': 'Failed to submit request'}), 500

@student_bp.route('/requests', methods=['GET'])
@jwt_required()
@role_required('student')
def get_correction_requests():
    claims = get_jwt()
    student_id = claims.get('sub')
    
    query = """
        SELECT cr.*, u.unit_code, u.unit_name, s.start_time
        FROM correction_requests cr
        INNER JOIN sessions s ON cr.session_id = s.session_id
        INNER JOIN units u ON s.unit_id = u.unit_id
        WHERE cr.student_id = %s
        ORDER BY cr.submitted_at DESC
    """
    from app.database import db
    requests = db.execute_query(query, (student_id,))
    
    requests_data = []
    for req in requests:
        requests_data.append({
            'request_id': req['request_id'],
            'session_id': req['session_id'],
            'unit_code': req['unit_code'],
            'unit_name': req['unit_name'],
            'session_date': req['start_time'].isoformat() if req['start_time'] else None,
            'reason': req['reason'],
            'status': req['status'],
            'admin_comment': req['admin_comment'],
            'submitted_at': req['submitted_at'].isoformat() if req['submitted_at'] else None,
            'reviewed_at': req['reviewed_at'].isoformat() if req['reviewed_at'] else None
        })
    
    return jsonify({
        'success': True,
        'requests': requests_data
    }), 200

@student_bp.route('/attendance/export', methods=['GET'])
@jwt_required()
@role_required('student')
def export_attendance():
    claims = get_jwt()
    student_id = claims.get('sub')
    
    from app.services.report_service import ReportService
    csv_data = ReportService.generate_student_attendance_report(student_id)
    
    from flask import Response
    response = Response(csv_data, mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename=attendance_history_{student_id}.csv'
    return response, 200

@student_bp.route('/change-password', methods=['POST'])
@jwt_required()
@role_required('student')
def change_password():
    claims = get_jwt()
    student_id = claims.get('sub')
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')
    
    if not old_password or not new_password:
        return jsonify({'success': False, 'error': 'Old and new passwords are required'}), 400
    
    user = User.get_by_id(student_id)
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    if not User.verify_password(old_password, user['password_hash']):
        return jsonify({'success': False, 'error': 'Old password is incorrect'}), 400
    
    # Validate new password
    from app.services.auth_service import AuthService
    is_valid, error_msg = AuthService.validate_password(new_password)
    if not is_valid:
        return jsonify({'success': False, 'error': error_msg}), 400
    
    # Update password
    new_hash = User.hash_password(new_password)
    query = "UPDATE users SET password_hash = %s WHERE user_id = %s"
    from app.database import db
    db.execute_query(query, (new_hash, student_id))
    
    return jsonify({
        'success': True,
        'message': 'Password changed successfully'
    }), 200

@student_bp.route('/notifications', methods=['GET'])
@jwt_required()
@role_required('student')
def get_notifications():
    claims = get_jwt()
    student_id = claims.get('sub')
    
    query = """
        SELECT n.*, u_from.full_name as from_name, u_from.role as from_role, u.unit_code, u.unit_name
        FROM notifications n
        LEFT JOIN users u_from ON n.from_user_id = u_from.user_id
        LEFT JOIN units u ON n.unit_id = u.unit_id
        WHERE n.to_user_id = %s
        ORDER BY n.created_at DESC
    """
    notifications = db.execute_query(query, (student_id,))
    
    return jsonify({
        'success': True,
        'notifications': notifications
    }), 200

@student_bp.route('/notifications/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
@role_required('student')
def mark_notification_read(notification_id):
    claims = get_jwt()
    student_id = claims.get('sub')
    
    # Verify notification belongs to this student
    query = "SELECT * FROM notifications WHERE notification_id = %s AND to_user_id = %s"
    notification = db.execute_query(query, (notification_id, student_id), fetch_one=True)
    if not notification:
        return jsonify({'success': False, 'error': 'Notification not found'}), 404
    
    # Mark as read
    query = "UPDATE notifications SET is_read = TRUE WHERE notification_id = %s"
    db.execute_query(query, (notification_id,))
    
    return jsonify({
        'success': True
    }), 200
