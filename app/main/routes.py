from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from app.main import bp
from app import mail
from flask_mail import Message
from config import Config

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/index.html')

@bp.route('/health')
def health():
    return "Application is Healthy", 200

@bp.route('/main')
@login_required
def main_index():
    try:
        # Safer logging to prevent AnonymousUser crashes or missing attribute errors
        username = getattr(current_user, 'username', 'Unknown')
        current_app.logger.info(f"Accessing main_index as user: {username}")
        return render_template('main/main.html')
    except Exception as e:
        import traceback
        current_app.logger.error(f"MAIN INDEX RENDER ERROR: {str(e)}\n{traceback.format_exc()}")
        raise e

@bp.route('/sendMail')
@login_required
def send_mail():
    from app.services.email_service import send_gift_email
    try:
        receiver = current_app.config['MAIL_RECEIVER']
        if not receiver:
            return ({'error': 'Mail receiver not configured'}, 500)
            
        send_gift_email(receiver)
        return ('', 204)
    except Exception as e:
        current_app.logger.error(f"Route mail error: {e}")
        return ({'status': 'error', 'message': str(e)}, 500)
