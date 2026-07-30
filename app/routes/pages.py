from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def index():
    return redirect(url_for('pages.login'))

@pages_bp.route('/login')
def login():
    return render_template('auth/login.html')

@pages_bp.route('/register')
def register():
    return render_template('auth/register.html')

@pages_bp.route('/dashboard')
@jwt_required()
def dashboard():
    claims = get_jwt()
    role = claims.get('role')
    
    if role == 'student':
        return render_template('student/dashboard.html')
    elif role == 'lecturer':
        return render_template('lecturer/dashboard.html')
    elif role == 'admin':
        return render_template('admin/dashboard.html')
    else:
        return redirect(url_for('pages.login'))

@pages_bp.route('/admin/dashboard')
@jwt_required()
def admin_dashboard():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return redirect(url_for('pages.login'))
    return render_template('admin/dashboard.html')

@pages_bp.route('/admin/users')
@jwt_required()
def admin_users():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return redirect(url_for('pages.login'))
    return render_template('admin/users.html')

@pages_bp.route('/admin/units')
@jwt_required()
def admin_units():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return redirect(url_for('pages.login'))
    return render_template('admin/units.html')

@pages_bp.route('/reports')
@jwt_required()
def reports():
    claims = get_jwt()
    if claims.get('role') != 'lecturer':
        return redirect(url_for('pages.login'))
    return render_template('lecturer/reports.html')
