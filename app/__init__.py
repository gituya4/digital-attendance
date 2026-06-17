from flask import Flask, request, redirect
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config['ALLOWED_ORIGINS']}})
    limiter.init_app(app)
    
    @app.before_request
    def enforce_https():
        if app.config['FLASK_ENV'] == 'production':
            if not request.is_secure and request.headers.get('X-Forwarded-Proto', 'http') != 'https':
                url = request.url.replace('http://', 'https://', 1)
                return redirect(url, code=301)
    
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/attendance.log', maxBytes=10240000, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Attendance system startup')
    
    from app.routes import auth_bp, student_bp, lecturer_bp, admin_bp, lecturer_pages_bp, student_pages_bp, admin_pages_bp
    from app.routes.pages import pages_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(lecturer_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(lecturer_pages_bp)
    app.register_blueprint(student_pages_bp)
    app.register_blueprint(admin_pages_bp)
    app.register_blueprint(pages_bp)
    
    @app.shell_context_processor
    def make_shell_context():
        from app.models.user import User
        return {'User': User}
    
    return app
