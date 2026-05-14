import os
from app import create_app, db
from app.models import User

def init():
    app = create_app()
    with app.app_context():
        # Create database and tables
        db.create_all()
        
        # Get credentials from environment
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        password = os.environ.get('ADMIN_PASSWORD', 'birthday2026')
        
        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"✅ Created administrative user: {username}")
        else:
            print(f"ℹ️ User {username} already exists.")

if __name__ == "__main__":
    init()
