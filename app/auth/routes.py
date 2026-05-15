from flask import render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.forms import LoginForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
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
            
            session.permanent = True
            login_user(user, remember=True)
            current_app.logger.info(f"User {user.username} logged in successfully, session_permanent={session.permanent}")
            return redirect(url_for('main.main_index'))
        
        if form.is_submitted() and not form.validate():
            current_app.logger.error(f"Form validation failed: {form.errors}")
        
        return render_template('auth/login.html', title='Sign In', form=form)
    except Exception as e:
        import traceback
        error_msg = f"CRITICAL LOGIN ERROR: {str(e)}\n{traceback.format_exc()}"
        current_app.logger.error(error_msg)
        # Expose error directly to UI for debugging since we can't see Render logs easily
        return f"<h1>Production Debug: Login Error</h1><pre>{error_msg}</pre>", 500

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
