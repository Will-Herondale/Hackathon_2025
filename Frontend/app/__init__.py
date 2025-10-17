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

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.get(user_id)

    # Register blueprints
    from app.routes import auth, profile, events, jobs, main, dashboard, colleges

    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(events.bp)
    app.register_blueprint(jobs.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(colleges.bp)

    return app
