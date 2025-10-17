from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms.auth import LoginForm, RegisterForm
from app.models.user import User
from app.database import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        # Fetch user from database
        user = User.get_by_email(form.email.data)

        if user and user.check_password(form.password.data):
            # Log user in
            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome back, {user.name}!', 'success')

            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        # Create user in database
        user = User.create(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
            user_type=form.user_type.data
        )

        if user:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Email may already be in use.', 'danger')

    return render_template('auth/register.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))


@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page"""
    # TODO: Implement forgot password functionality
    return render_template('auth/forgot_password.html')
