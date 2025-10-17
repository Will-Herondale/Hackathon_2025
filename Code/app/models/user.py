from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.db_models import User as DBUser
from app.database import db
import json


class User(UserMixin):
    """User model for Flask-Login (wraps database User model)"""

    def __init__(self, db_user):
        """Initialize from database User model"""
        self.id = db_user.id
        self.email = db_user.email
        self.name = db_user.name
        self.user_type = db_user.user_type
        self.password_hash = db_user.password_hash
        self.profile_public = db_user.profile_public
        self._db_user = db_user

    @property
    def profile_data(self):
        """Get profile data as dictionary for template compatibility"""
        try:
            # Refresh the db_user to ensure we have the latest data
            from app.models.db_models import Profile
            profile = Profile.query.filter_by(user_id=self.id).first()

            if not profile:
                return {
                    'avatar': None,
                    'bio': '',
                    'title': '',
                    'location': '',
                    'website': '',
                    'github': '',
                    'linkedin': '',
                    'twitter': '',
                    'skills': [],
                    'interests': []
                }

            # Parse JSON fields
            try:
                skills = json.loads(profile.skills) if profile.skills else []
            except:
                skills = []

            try:
                interests = json.loads(profile.interests) if profile.interests else []
            except:
                interests = []

            return {
                'avatar': profile.avatar_url,
                'bio': profile.bio,
                'title': profile.title,
                'location': profile.location,
                'website': profile.website,
                'github': profile.github,
                'linkedin': profile.linkedin,
                'twitter': profile.twitter,
                'resume_url': profile.resume_url,
                'skills': skills,
                'interests': interests
            }
        except Exception as e:
            # Return default values on any error
            return {
                'avatar': None,
                'bio': '',
                'title': '',
                'location': '',
                'website': '',
                'github': '',
                'linkedin': '',
                'twitter': '',
                'skills': [],
                'interests': []
            }

    @property
    def profile(self):
        """Get the profile object"""
        return self._db_user.profile

    @property
    def projects(self):
        """Get user's projects"""
        return self._db_user.projects

    @property
    def goals(self):
        """Get user's goals"""
        return self._db_user.goals

    @property
    def achievements(self):
        """Get user's achievements"""
        return self._db_user.achievements

    @staticmethod
    def get(user_id):
        """Fetch user from database by ID"""
        db_user = DBUser.query.get(int(user_id))
        if db_user:
            return User(db_user)
        return None

    @staticmethod
    def get_by_email(email):
        """Fetch user from database by email"""
        db_user = DBUser.query.filter_by(email=email).first()
        if db_user:
            return User(db_user)
        return None

    @staticmethod
    def create(name, email, password, user_type='adult'):
        """Create a new user in the database"""
        # Check if user already exists
        if DBUser.query.filter_by(email=email).first():
            return None

        # Create new user
        db_user = DBUser(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            user_type=user_type
        )

        db.session.add(db_user)
        db.session.commit()

        return User(db_user)

    def check_password(self, password):
        """Check if provided password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def update_profile(self, **kwargs):
        """Update user profile in database"""
        for key, value in kwargs.items():
            if hasattr(self._db_user, key):
                setattr(self._db_user, key, value)

        db.session.commit()

    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'user_type': self.user_type
        }
