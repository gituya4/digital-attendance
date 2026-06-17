from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from app.routes import auth_bp
from app.services.auth_service import AuthService
from app.models.user import User
from app.utils import log_action, write_audit_log
from app import limiter

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    role = data.get('role', 'student').lower()
    
    if role == 'student':
        full_name = data.get('full_name', '').strip()
        registration_number = data.get('registration_number', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        success, message = AuthService.register_student(full_name, registration_number, email, password)
        
        if success:
            return jsonify({'success': True, 'message': message}), 201
        else:
            return jsonify({'success': False, 'error': message}), 400
    
    elif role == 'lecturer':
        full_name = data.get('full_name', '').strip()
        staff_id = data.get('staff_id', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        department = data.get('department', '').strip()
        
        success, message = AuthService.register_lecturer(full_name, staff_id, email, password, department)
        
        if success:
            return jsonify({'success': True, 'message': message}), 201
        else:
            return jsonify({'success': False, 'error': message}), 400
    
    else:
        return jsonify({'success': False, 'error': 'Invalid role'}), 400

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per 10 minutes")
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    success, user_data, message = AuthService.login(email, password)
    
    if success:
        access_token = create_access_token(
            identity=str(user_data['user_id']),
            additional_claims={'role': user_data['role'], 'name': user_data['full_name']}
        )
        
        write_audit_log(user_data['user_id'], 'login', f'User {user_data["email"]} logged in')
        
        response = jsonify({
            'success': True,
            'message': message,
            'user': user_data
        })
        response.set_cookie('access_token_cookie', access_token, httponly=True, secure=False, samesite='Strict')
        
        return response, 200
    else:
        return jsonify({'success': False, 'error': message}), 401

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    claims = get_jwt()
    user_id = int(claims.get('sub'))
    write_audit_log(user_id, 'logout', f'User logged out')
    
    response = jsonify({'success': True, 'message': 'Logged out successfully'})
    response.delete_cookie('access_token_cookie')
    return response, 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    from flask_jwt_extended import get_jwt
    claims = get_jwt()
    user_id = int(claims.get('sub'))
    
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'user': {
            'user_id': user['user_id'],
            'full_name': user['full_name'],
            'email': user['email'],
            'role': user['role'],
            'registration_number': user['registration_number'],
            'staff_id': user['staff_id'],
            'department': user['department']
        }
    }), 200
