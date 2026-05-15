import os
import sys
import traceback
from app import create_app, db
from app.models import User

def init():
    print("Starting aggressive database initialization...")
    app = create_app()
    with app.app_context():
        try:
            # FORCE REFRESH: Drop tables to ensure UUID schema is applied
            # This is necessary because we changed 'id' from Integer to String(36)
            print("Dropping old tables to sync schema...")
            db.drop_all()
            
            print("Creating fresh tables...")
            db.create_all()
            
            # 1. Admin Account
            admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
            admin_password = os.environ.get('ADMIN_PASSWORD', 'Birthday2026')
            
            admin_user = User(username=admin_username)
            admin_user.set_password(admin_password)
            db.session.add(admin_user)
            print(f"Created administrative user: {admin_username}")
            
            # 2. Likitha Account
            likitha_username = 'Likitha'
            likitha_password = 'Birthday2026' 
            
            likitha_user = User(username=likitha_username)
            likitha_user.set_password(likitha_password)
            db.session.add(likitha_user)
            print(f"Created user: {likitha_username}")
                
            db.session.commit()
            print("Database initialization completed successfully.")
            
        except Exception as e:
            print("CRITICAL DATABASE INIT ERROR:")
            print(str(e))
            traceback.print_exc()
            db.session.rollback()
            sys.exit(1) # Exit with error so gunicorn doesn't start on a broken DB

if __name__ == "__main__":
    init()
