from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.models.user import User
from app.database import db

def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role not in roles:
                return jsonify({'success': False, 'error': 'Access forbidden'}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def log_action(action: str, detail: str = None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                user_id = claims.get('sub')
            except:
                user_id = None
            
            ip_address = request.remote_addr
            
            query = """
                INSERT INTO audit_log (user_id, action, detail, ip_address)
                VALUES (%s, %s, %s, %s)
            """
            db.execute_query(query, (user_id, action, detail, ip_address))
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def get_current_user():
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        user_id = claims.get('sub')
        return User.get_by_id(user_id)
    except:
        return None

def write_audit_log(user_id, action, detail=None):
    """Write an entry to the audit log table"""
    try:
        from flask import request
        ip_address = request.remote_addr if request else None
        query = """
            INSERT INTO audit_log (user_id, action, detail, ip_address)
            VALUES (%s, %s, %s, %s)
        """
        db.execute_query(query, (user_id, action, detail, ip_address))
    except Exception as e:
        print(f"Failed to write audit log: {e}")
