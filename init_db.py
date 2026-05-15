import os
from app import create_app, db
from app.models import User

def init():
    app = create_app()
    with app.app_context():
        # Create database and tables
        db.create_all()
        
        # 1. Admin Account
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'Birthday2026')
        
        admin_user = User.query.filter_by(username=admin_username).first()
        if not admin_user:
            admin_user = User(username=admin_username)
            admin_user.set_password(admin_password)
            db.session.add(admin_user)
            print(f"Created administrative user: {admin_username}")
        
        # 2. Likitha Account
        likitha_username = 'likitha'
        likitha_password = 'likitha_birthday_2026' # Safe default or specific as requested
        
        likitha_user = User.query.filter_by(username=likitha_username).first()
        if not likitha_user:
            likitha_user = User(username=likitha_username)
            likitha_user.set_password(likitha_password)
            db.session.add(likitha_user)
            print(f"Created user: {likitha_username}")
            
        db.session.commit()

if __name__ == "__main__":
    init()
