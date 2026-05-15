from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize extensions outside the factory
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    # Register Blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Configure Logging for Resiliency
    if not app.testing:
        # 1. Clear existing handlers to prevent duplicates
        app.logger.handlers.clear()
        
        # 2. Add StreamHandler (Stdout) - Best for Render/Docker/Heroku
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)

        # 3. Skip file logging on Render entirely to avoid permission issues
        if not app.config.get('RENDER'):
            try:
                if not os.path.exists('logs'):
                    os.mkdir('logs')
                file_handler = RotatingFileHandler('logs/birthday.log', maxBytes=10240, backupCount=10)
                file_handler.setFormatter(logging.Formatter(
                    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
                file_handler.setLevel(logging.INFO)
                app.logger.addHandler(file_handler)
            except:
                pass

        app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
        app.logger.info('Birthday Tribute application startup')

    # Auto-initialize database tables and admin user for Render/Production resilience
    with app.app_context():
        try:
            db.create_all()
            from app.models import User
            if not User.query.filter_by(username='admin').first():
                admin = User(username='admin')
                admin.set_password(os.environ.get('ADMIN_PASSWORD', 'Birthday2026'))
                db.session.add(admin)
                
            if not User.query.filter_by(username='Likitha').first():
                likitha = User(username='Likitha')
                likitha.set_password('Birthday2026')
                db.session.add(likitha)
                
            db.session.commit()
            app.logger.info("Database auto-initialization successful.")
        except Exception as e:
            app.logger.error(f"Database auto-initialization failed: {e}")

    return app

from app import models