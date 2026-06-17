from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
student_bp = Blueprint('student', __name__, url_prefix='/api/student')
lecturer_bp = Blueprint('lecturer', __name__, url_prefix='/api/lecturer')
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# Page routes (without /api prefix)
lecturer_pages_bp = Blueprint('lecturer_pages', __name__, url_prefix='/lecturer')
student_pages_bp = Blueprint('student_pages', __name__, url_prefix='/student')
admin_pages_bp = Blueprint('admin_pages', __name__, url_prefix='/admin')

from app.routes import auth, student, lecturer, admin
