import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', False)
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///attendance.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_SAMESITE = 'Strict'
    JWT_COOKIE_CSRF_PROTECT = False
    
    HMAC_SECRET_KEY = os.getenv('HMAC_SECRET_KEY', 'dev-hmac-key-change-in-production')
    
    ALLOWED_ORIGINS = [os.getenv('APP_DOMAIN', 'localhost:5000')]
    
    RATELIMIT_STORAGE_URL = 'memory://'
    
    SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    
    PREFERRED_URL_SCHEME = 'https' if os.getenv('FLASK_ENV') == 'production' else 'http'
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
