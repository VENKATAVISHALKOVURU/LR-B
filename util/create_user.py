import sys,os
sys.path.append(os.getcwd())
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    u = User.query.filter_by(username=sys.argv[1]).first()
    if u:
        u.set_password(sys.argv[2])
        print(f"Updated password for user: {sys.argv[1]}")
    else:
        u = User(username=sys.argv[1])
        u.set_password(sys.argv[2])
        db.session.add(u)
        print(f"Created new user: {sys.argv[1]}")
    db.session.commit()
