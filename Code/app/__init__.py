from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv
import re

load_dotenv()

login_manager = LoginManager()
socketio = SocketIO()

def strip_html(text):
    """Remove HTML tags from text"""
    if not text:
        return ''
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', ' ', text)
    # Replace multiple spaces with single space
    clean = re.sub(r'\s+', ' ', clean)
    # Strip leading/trailing whitespace
    return clean.strip()

def format_salary_lakhs(amount):
    """Convert salary amount to lakhs format
    Examples: 700000 -> 7, 1500000 -> 15, 50000 -> 0.5
    """
    if not amount:
        return 0
    try:
        # Convert to float if string
        amount = float(amount)
        # Convert to lakhs (1 lakh = 100,000)
        lakhs = amount / 100000
        # Format with up to 1 decimal place, removing trailing zeros
        if lakhs == int(lakhs):
            return int(lakhs)
        else:
            return round(lakhs, 1)
    except (ValueError, TypeError):
        return amount

def create_app(config_name='default'):
    app = Flask(__name__)

    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])

    # Initialize database
    from app.database import init_db
    init_db(app)

    # Initialize extensions
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    socketio.init_app(app, cors_allowed_origins="*")

    # Register custom Jinja2 filters
    app.jinja_env.filters['strip_html'] = strip_html
    app.jinja_env.filters['lakhs'] = format_salary_lakhs

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.get(user_id)

    # Register blueprints
    from app.routes import auth, profile, events, jobs, main, dashboard, colleges, courses

    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(events.bp)
    app.register_blueprint(jobs.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(colleges.bp)
    app.register_blueprint(courses.bp)

    return app
