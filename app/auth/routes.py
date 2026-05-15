from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.forms import LoginForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        current_app.logger.info(f"User {current_user.username} already authenticated, redirecting to main")
        return redirect(url_for('main.main_index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            current_app.logger.warning(f"Failed login attempt for username: {form.username.data}")
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        
        from flask import session
        session.permanent = True
        login_user(user)
        current_app.logger.info(f"User {user.username} logged in successfully, redirecting to main")
        return redirect(url_for('main.main_index'))
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
