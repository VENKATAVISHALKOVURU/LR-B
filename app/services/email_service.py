from flask_mail import Message
from flask import render_template, current_app
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        try:
            # Avoid circular import by fetching mail from app extensions
            mail = app.extensions.get('mail')
            if mail:
                mail.send(msg)
            else:
                app.logger.error("Mail extension not found in app")
        except Exception as e:
            app.logger.error(f"Async mail error: {e}")

def send_email(subject, sender, recipients, text_body, html_body, trigger_source="Unknown"):
    app = current_app._get_current_object()
    
    # SAFE_MODE_EMAIL Routing Logic
    is_safe_mode = app.config.get('SAFE_MODE_EMAIL', True)
    dev_email = app.config.get('DEV_TEST_EMAIL')
    
    original_recipients = recipients
    if is_safe_mode:
        recipients = [dev_email] if dev_email else recipients
        app.logger.info(f" [SAFE_MODE] Redirecting email from {original_recipients} to {recipients}")
    
    # Detailed Debug Logging (Task 19.3)
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # SMTP Config Audit
    smtp_server = app.config.get('MAIL_SERVER')
    smtp_port = app.config.get('MAIL_PORT')
    use_tls = app.config.get('MAIL_USE_TLS')
    use_ssl = app.config.get('MAIL_USE_SSL')
    
    log_msg = (
        f"\n--- EMAIL DELIVERY AUDIT ---\n"
        f"Timestamp: {timestamp}\n"
        f"Trigger Source: {trigger_source}\n"
        f"Subject: {subject}\n"
        f"Intended Recipient(s): {original_recipients}\n"
        f"Actual Recipient(s): {recipients}\n"
        f"Safe Mode Active: {is_safe_mode}\n"
        f"SMTP Config: {smtp_server}:{smtp_port} (TLS: {use_tls}, SSL: {use_ssl})\n"
        f"----------------------------"
    )
    app.logger.info(log_msg)
    print(log_msg) # Visible in Render console logs
    
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    
    # Use threading for non-blocking cinematic experience
    Thread(target=send_async_email, 
           args=(app, msg)).start()

def send_gift_email(user_email):
    send_email(
        'Happy 19th Birthday, Likitha! 🎂',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user_email],
        text_body="Dear Likitha, You’ve officially reached the final memory of your birthday journey. Happy 19th Birthday!",
        html_body=render_template('email/gift_email.html'),
        trigger_source="GIFT_BUTTON_TRIGGER"
    )
