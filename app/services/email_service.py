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

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    
    # Use threading for non-blocking cinematic experience
    Thread(target=send_async_email, 
           args=(current_app._get_current_object(), msg)).start()

def send_gift_email(user_email):
    send_email(
        'Happy 19th Birthday, Likitha! 🎂',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user_email],
        text_body="Dear Likitha, You’ve officially reached the final memory of your birthday journey. Happy 19th Birthday!",
        html_body=render_template('email/gift_email.html')
    )
