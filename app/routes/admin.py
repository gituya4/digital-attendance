from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.routes import admin_bp
from app.models.user import User
from app.models.unit import Unit
from app.utils import role_required, write_audit_log
from app.database import db

# Admin routes will be added one by one and tested

# Function 1: Get all users
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_users():
    role = request.args.get('role')
    
    users = User.get_all(role)
    
    users_data = []
    for user in users:
        users_data.append({
            'user_id': user['user_id'],
            'full_name': user['full_name'],
            'email': user['email'],
            'role': user['role'],
            'registration_number': user['registration_number'],
            'staff_id': user['staff_id'],
            'department': user['department'],
            'is_active': user['is_active']
        })
    
    return jsonify({
        'success': True,
        'users': users_data
    }), 200

# Function 2: Create user
@admin_bp.route('/users', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    full_name = data.get('full_name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    role = data.get('role', '').lower()
    
    if not all([full_name, email, password, role]):
        return jsonify({'success': False, 'error': 'All fields are required'}), 400
    
    if User.email_exists(email):
        return jsonify({'success': False, 'error': 'Email already in use'}), 400
    
    if role == 'student':
        registration_number = data.get('registration_number', '').strip()
        if not registration_number:
            return jsonify({'success': False, 'error': 'Registration number is required for students'}), 400
        
        if User.registration_number_exists(registration_number):
            return jsonify({'success': False, 'error': 'Registration number already in use'}), 400
        
        result = User.create(full_name, email, password, role, registration_number=registration_number)
    
    elif role == 'lecturer':
        staff_id = data.get('staff_id', '').strip()
        department = data.get('department', '').strip()
        
        if not staff_id or not department:
            return jsonify({'success': False, 'error': 'Staff ID and department are required for lecturers'}), 400
        
        if User.staff_id_exists(staff_id):
            return jsonify({'success': False, 'error': 'Staff ID already in use'}), 400
        
        result = User.create(full_name, email, password, role, staff_id=staff_id, department=department)
    
    elif role == 'admin':
        result = User.create(full_name, email, password, role)
    
    else:
        return jsonify({'success': False, 'error': 'Invalid role'}), 400
    
    if result:
        return jsonify({
            'success': True,
            'message': 'User created successfully'
        }), 201
    else:
        return jsonify({'success': False, 'error': 'Failed to create user'}), 500

# Function 3: Get all units
@admin_bp.route('/units', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_units():
    units = Unit.get_all()
    
    return jsonify({
        'success': True,
        'units': units
    }), 200

# Function 4: Create unit
@admin_bp.route('/units', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_unit():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    unit_code = data.get('unit_code', '').strip()
    unit_name = data.get('unit_name', '').strip()
    department = data.get('department', '').strip()
    semester = data.get('semester', '').strip()
    academic_year = data.get('academic_year', '').strip()
    
    if not all([unit_code, unit_name, department, semester, academic_year]):
        return jsonify({'success': False, 'error': 'All fields are required'}), 400
    
    if Unit.code_exists(unit_code):
        return jsonify({'success': False, 'error': 'Unit code already exists'}), 400
    
    result = Unit.create(unit_code, unit_name, department, semester, academic_year)
    
    if result:
        return jsonify({
            'success': True,
            'message': 'Unit created successfully'
        }), 201
    else:
        return jsonify({'success': False, 'error': 'Failed to create unit'}), 500

# Function 5: Assign lecturer to unit
@admin_bp.route('/units/<int:unit_id>/assign-lecturer', methods=['POST'])
@jwt_required()
@role_required('admin')
def assign_lecturer(unit_id):
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    lecturer_id = data.get('lecturer_id')
    
    if not lecturer_id:
        return jsonify({'success': False, 'error': 'Lecturer ID is required'}), 400
    
    try:
        lecturer_id = int(lecturer_id)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Invalid lecturer ID'}), 400
    
    try:
        # Check if lecturer exists
        lecturer = User.get_by_id(lecturer_id)
        if not lecturer or lecturer['role'] != 'lecturer':
            return jsonify({'success': False, 'error': 'Lecturer not found'}), 404
        
        # Check if unit exists
        unit = Unit.get_by_id(unit_id)
        if not unit:
            return jsonify({'success': False, 'error': 'Unit not found'}), 404
        
        # Check if already assigned
        query = "SELECT id FROM lecturer_units WHERE lecturer_id = %s AND unit_id = %s"
        existing = db.execute_query(query, (lecturer_id, unit_id), fetch_one=True)
        if existing:
            return jsonify({'success': True, 'message': 'Lecturer already assigned to this unit'}), 200
        
        # Insert assignment using direct SQL
        query = "INSERT INTO lecturer_units (lecturer_id, unit_id) VALUES (%s, %s)"
        db.execute_query(query, (lecturer_id, unit_id))
        
        return jsonify({
            'success': True,
            'message': 'Lecturer assigned successfully'
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Get lecturers assigned to a unit
@admin_bp.route('/units/<int:unit_id>/lecturers', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_unit_lecturers(unit_id):
    unit = Unit.get_by_id(unit_id)
    if not unit:
        return jsonify({'success': False, 'error': 'Unit not found'}), 404
    
    query = """
        SELECT u.user_id, u.full_name, u.email, u.staff_id, u.department
        FROM users u
        INNER JOIN lecturer_units lu ON u.user_id = lu.lecturer_id
        WHERE lu.unit_id = %s AND u.role = 'lecturer'
    """
    lecturers = db.execute_query(query, (unit_id,))
    
    return jsonify({
        'success': True,
        'lecturers': lecturers
    }), 200

# Get all lecturers
@admin_bp.route('/lecturers', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_lecturers():
    try:
        lecturers = User.get_all('lecturer')
        
        return jsonify({
            'success': True,
            'lecturers': lecturers
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Get all students
@admin_bp.route('/students', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_students():
    try:
        students = User.get_all('student')
        
        return jsonify({
            'success': True,
            'students': students
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Enroll student in unit
@admin_bp.route('/units/<int:unit_id>/enroll-student', methods=['POST'])
@jwt_required()
@role_required('admin')
def enroll_student(unit_id):
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    student_id = data.get('student_id')
    
    if not student_id:
        return jsonify({'success': False, 'error': 'Student ID is required'}), 400
    
    try:
        student_id = int(student_id)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Invalid student ID'}), 400
    
    try:
        # Check if student exists
        student = User.get_by_id(student_id)
        if not student or student['role'] != 'student':
            return jsonify({'success': False, 'error': 'Student not found'}), 404
        
        # Check if unit exists
        unit = Unit.get_by_id(unit_id)
        if not unit:
            return jsonify({'success': False, 'error': 'Unit not found'}), 404
        
        # Check if already enrolled
        query = "SELECT id FROM enrollments WHERE student_id = %s AND unit_id = %s"
        existing = db.execute_query(query, (student_id, unit_id), fetch_one=True)
        if existing:
            return jsonify({'success': True, 'message': 'Student already enrolled in this unit'}), 200
        
        # Insert enrollment using direct SQL
        query = "INSERT INTO enrollments (student_id, unit_id) VALUES (%s, %s)"
        db.execute_query(query, (student_id, unit_id))
        
        write_audit_log(student_id, 'enrolled', f'Enrolled in unit {unit_id}')
        
        return jsonify({
            'success': True,
            'message': 'Student enrolled successfully'
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Get students enrolled in a unit
@admin_bp.route('/units/<int:unit_id>/students', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_unit_students(unit_id):
    unit = Unit.get_by_id(unit_id)
    if not unit:
        return jsonify({'success': False, 'error': 'Unit not found'}), 404
    
    query = """
        SELECT u.user_id, u.full_name, u.email, u.registration_number
        FROM users u
        INNER JOIN enrollments e ON u.user_id = e.student_id
        WHERE e.unit_id = %s AND u.role = 'student'
    """
    students = db.execute_query(query, (unit_id,))
    
    return jsonify({
        'success': True,
        'students': students
    }), 200

# Remove student from unit
@admin_bp.route('/units/<int:unit_id>/students/<int:student_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def remove_student(unit_id, student_id):
    try:
        query = "DELETE FROM enrollments WHERE student_id = %s AND unit_id = %s"
        db.execute_query(query, (student_id, unit_id))
        
        write_audit_log(student_id, 'unenrolled', f'Removed from unit {unit_id}')
        
        return jsonify({
            'success': True,
            'message': 'Student removed successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
