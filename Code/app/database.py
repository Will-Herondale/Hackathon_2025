from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Initialize SQLAlchemy
db = SQLAlchemy()


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)


def get_db():
    """Get database instance"""
    return db


def create_tables():
    """Create all database tables"""
    db.create_all()
    print("✓ Database tables created successfully!")


def drop_tables():
    """Drop all database tables"""
    db.drop_all()
    print("✓ Database tables dropped successfully!")
