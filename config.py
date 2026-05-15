import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'development-secret-key-12345'
    
    # Database
    # Priority: 1. Corrected DATABASE_URL, 2. SQLite in current dir, 3. SQLite in /tmp (fail-safe)
    _db_uri = os.environ.get('DATABASE_URL')
    if _db_uri and _db_uri.startswith("postgres://"):
        _db_uri = _db_uri.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = _db_uri or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Sessions
    SESSION_COOKIE_NAME = 'birthday_tribute_session'
    PERMANENT_SESSION_LIFETIME = 3600 # 1 hour
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_RECEIVER = os.environ.get('MAIL_RECEIVER') or 'likithreddyvaka2007@mail.com'
    
    # Application State
    RENDER = os.environ.get('RENDER', 'False').lower() == 'true'
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'
    TESTING = False