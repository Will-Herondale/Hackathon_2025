from app.database import db
from datetime import datetime
from sqlalchemy import Index
import json


class User(db.Model):
    """User model for database"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(50), default='adult')  # 'kid' or 'adult'
    profile_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete-orphan')
    projects = db.relationship('Project', backref='user', cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', cascade='all, delete-orphan')
    achievements = db.relationship('Achievement', backref='user', cascade='all, delete-orphan')
    enrollments = db.relationship('EventEnrollment', backref='user', cascade='all, delete-orphan')

    @property
    def profile_data(self):
        """Get profile data as dictionary for template compatibility"""
        if not self.profile:
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
            skills = json.loads(self.profile.skills) if self.profile.skills else []
        except:
            skills = []

        try:
            interests = json.loads(self.profile.interests) if self.profile.interests else []
        except:
            interests = []

        return {
            'avatar': self.profile.avatar_url,
            'bio': self.profile.bio,
            'title': self.profile.title,
            'location': self.profile.location,
            'website': self.profile.website,
            'github': self.profile.github,
            'linkedin': self.profile.linkedin,
            'twitter': self.profile.twitter,
            'resume_url': self.profile.resume_url,
            'skills': skills,
            'interests': interests
        }

    def __repr__(self):
        return f'<User {self.email}>'


class Profile(db.Model):
    """User profile information"""
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    bio = db.Column(db.Text)
    title = db.Column(db.String(255))
    location = db.Column(db.String(255))
    website = db.Column(db.String(500))
    github = db.Column(db.String(255))
    linkedin = db.Column(db.String(500))
    twitter = db.Column(db.String(255))
    avatar_url = db.Column(db.String(500))
    resume_url = db.Column(db.String(500))
    skills = db.Column(db.Text)  # JSON array stored as text
    interests = db.Column(db.Text)  # JSON array stored as text
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Profile {self.user_id}>'


class Project(db.Model):
    """Portfolio projects"""
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    technologies = db.Column(db.Text)  # JSON array stored as text
    project_url = db.Column(db.String(500))
    github_url = db.Column(db.String(500))
    image_url = db.Column(db.String(500))
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('idx_user_projects', 'user_id'),
    )

    def __repr__(self):
        return f'<Project {self.title}>'


class Event(db.Model):
    """Events and courses"""
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50))  # workshop, course, webinar, etc.
    category = db.Column(db.String(100))
    level = db.Column(db.String(50))  # beginner, intermediate, advanced
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    location_type = db.Column(db.String(50))  # online, in-person, hybrid
    location = db.Column(db.String(500))
    max_participants = db.Column(db.Integer)
    price = db.Column(db.Integer, default=0)
    tags = db.Column(db.Text)  # JSON array
    image_url = db.Column(db.String(500))
    registration_url = db.Column(db.String(500))  # External registration link
    featured = db.Column(db.Boolean, default=False)
    age_appropriate_for_kids = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    enrollments = db.relationship('EventEnrollment', backref='event', cascade='all, delete-orphan')

    __table_args__ = (
        Index('idx_event_category', 'category'),
        Index('idx_event_type', 'event_type'),
        Index('idx_event_dates', 'start_date', 'end_date'),
    )

    def __repr__(self):
        return f'<Event {self.title}>'


class EventEnrollment(db.Model):
    """Event enrollment records"""
    __tablename__ = 'event_enrollments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    status = db.Column(db.String(50), default='enrolled')  # enrolled, completed, cancelled
    notes = db.Column(db.Text)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    __table_args__ = (
        Index('idx_user_enrollments', 'user_id'),
        Index('idx_event_enrollments', 'event_id'),
        db.UniqueConstraint('user_id', 'event_id', name='unique_user_event_enrollment'),
    )

    def __repr__(self):
        return f'<EventEnrollment user:{self.user_id} event:{self.event_id}>'


class Goal(db.Model):
    """User goals (dream colleges, companies, etc.)"""
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # education, career, skill, personal
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    progress = db.Column(db.Integer, default=0)  # 0-100
    status = db.Column(db.String(50), default='active')  # active, completed, abandoned
    target_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    __table_args__ = (
        Index('idx_user_goals', 'user_id'),
        Index('idx_goal_status', 'status'),
    )

    def __repr__(self):
        return f'<Goal {self.title}>'


class Achievement(db.Model):
    """User achievements and badges"""
    __tablename__ = 'achievements'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_type = db.Column(db.String(100), nullable=False)  # first_course, bookworm, etc.
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # emoji or icon name
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_user_achievements', 'user_id'),
        db.UniqueConstraint('user_id', 'badge_type', name='unique_user_badge'),
    )

    def __repr__(self):
        return f'<Achievement {self.title}>'


class Job(db.Model):
    """Job listings - WARNING: Table has NO primary key in database!"""
    __tablename__ = 'jobs'

    # CRITICAL: The database table has NO primary key or id column!
    # Using jobId as primary key for SQLAlchemy to work, though it's not a real PK in DB
    __table_args__ = {'extend_existing': True}

    # All columns from actual database (18 total, NO id column exists!)
    jobId = db.Column(db.BigInteger, primary_key=True)  # Using as PK for SQLAlchemy
    title = db.Column(db.String(255))
    currency = db.Column(db.String(255))
    jobUploaded = db.Column(db.String(255))  # Stored as VARCHAR in DB
    companyName = db.Column(db.String(255))
    tagsAndSkills = db.Column(db.String(None))  # VARCHAR(MAX)
    experience = db.Column(db.String(255))
    salary = db.Column(db.String(255))
    location = db.Column(db.String(255))
    companyId = db.Column(db.BigInteger)  # BIGINT in DB
    ReviewsCount = db.Column(db.Float)  # FLOAT in DB
    AggregateRating = db.Column(db.Float)
    jobDescription = db.Column(db.String(None))  # VARCHAR(MAX)
    minimumSalary = db.Column(db.Float)  # FLOAT in DB
    maximumSalary = db.Column(db.Float)  # FLOAT in DB
    minimumExperience = db.Column(db.Float)  # FLOAT in DB
    maximumExperience = db.Column(db.Float)  # FLOAT in DB
    application_url = db.Column(db.String(500))  # Cached application URL

    def __repr__(self):
        return f'<Job {self.title} at {self.companyName}>'


class Conversation(db.Model):
    """Messaging conversations"""
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  # For group chats
    conversation_type = db.Column(db.String(50), nullable=False)  # direct, group
    group_type = db.Column(db.String(50))  # public, private
    description = db.Column(db.Text)
    avatar_url = db.Column(db.String(500))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    messages = db.relationship('Message', backref='conversation', cascade='all, delete-orphan')
    participants = db.relationship('ConversationParticipant', backref='conversation', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Conversation {self.id} ({self.conversation_type})>'


class ConversationParticipant(db.Model):
    """Participants in conversations"""
    __tablename__ = 'conversation_participants'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_read_at = db.Column(db.DateTime)

    __table_args__ = (
        Index('idx_conversation_participants', 'conversation_id'),
        Index('idx_user_conversations', 'user_id'),
        db.UniqueConstraint('conversation_id', 'user_id', name='unique_conversation_participant'),
    )

    def __repr__(self):
        return f'<Participant user:{self.user_id} conversation:{self.conversation_id}>'


class Message(db.Model):
    """Messages in conversations"""
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    attachment_url = db.Column(db.String(500))
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_conversation_messages', 'conversation_id', 'sent_at'),
        Index('idx_sender_messages', 'sender_id'),
    )

    def __repr__(self):
        return f'<Message {self.id} in conversation {self.conversation_id}>'


class Activity(db.Model):
    """User activity log"""
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    reference_id = db.Column(db.Integer)  # ID of related entity
    reference_type = db.Column(db.String(50))  # Type of related entity
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_user_activities', 'user_id', 'created_at'),
    )

    def __repr__(self):
        return f'<Activity {self.activity_type} by user {self.user_id}>'


class College(db.Model):
    """College/University data - Uses existing college_collages table (alias for browsing)"""
    __tablename__ = 'college_collages'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    college_name = db.Column(db.String(255), nullable=False)
    stream = db.Column(db.String(100))  # Engineering, Medical, Arts, etc.
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    entrance_exams = db.Column(db.String(255))  # Comma-separated or JSON
    eligibility_criteria = db.Column(db.String(500))
    required_skills = db.Column(db.String(500))  # Comma-separated or JSON
    typical_exam_cutoffs = db.Column(db.String(255))  # JSON string
    fee_structure = db.Column(db.Integer)  # Total fee
    seat_intake = db.Column(db.Integer)
    college_type = db.Column(db.String(50))  # Government, Private, Deemed, etc.
    tier_rank = db.Column(db.Integer)  # 1, 2, 3
    website_url = db.Column(db.String(255))
    placement_average_salary = db.Column(db.Integer)  # In lakhs
    located_in_campus = db.Column(db.String(10))  # "Yes" or "No"
    year_established = db.Column(db.Integer)
    accreditation = db.Column(db.String(100))  # NAAC A++, NBA, etc.
    gender_ratio = db.Column(db.String(50))  # e.g., "70:30 (M:F)"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<College {self.college_name}>'


class CollegeCollage(db.Model):
    """User's dream college collage for kids mode - Same table as College"""
    __tablename__ = 'college_collages'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  # Optional for public colleges
    college_name = db.Column(db.String(255), nullable=False)
    stream = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    entrance_exams = db.Column(db.String(255))
    eligibility_criteria = db.Column(db.String(500))
    required_skills = db.Column(db.String(500))
    typical_exam_cutoffs = db.Column(db.String(255))
    fee_structure = db.Column(db.Integer)
    seat_intake = db.Column(db.Integer)
    college_type = db.Column(db.String(50))
    tier_rank = db.Column(db.Integer)
    website_url = db.Column(db.String(255))
    placement_average_salary = db.Column(db.Integer)
    located_in_campus = db.Column(db.String(10))
    year_established = db.Column(db.Integer)
    accreditation = db.Column(db.String(100))
    gender_ratio = db.Column(db.String(50))
    # Legacy fields for kids mode
    college_logo_url = db.Column(db.String(500))
    college_images = db.Column(db.Text)
    motivation_text = db.Column(db.Text)
    why_this_college = db.Column(db.Text)
    target_year = db.Column(db.Integer)
    display_order = db.Column(db.Integer, default=0)
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<CollegeCollage {self.college_name}>'


class Course(db.Model):
    """Online courses - WARNING: Table has NO primary key in database!"""
    __tablename__ = 'courses'

    __table_args__ = {'extend_existing': True}

    # Using url as primary key for SQLAlchemy (not a real PK in DB)
    url = db.Column(db.String(None), primary_key=True)
    type = db.Column(db.String(None))
    course_name = db.Column(db.String(None))
    organization = db.Column(db.String(None))
    instructor = db.Column(db.String(None))
    rating = db.Column(db.String(None))  # VARCHAR in DB, not FLOAT
    nu_reviews = db.Column(db.String(None))  # VARCHAR in DB
    description = db.Column(db.String(None))
    skills = db.Column(db.String(None))
    level = db.Column(db.String(None))
    Duration = db.Column(db.Float)
    reviews = db.Column(db.String(None))  # VARCHAR in DB

    # Total counts for different content types
    total_assignment = db.Column(db.Float)
    total_app = db.Column(db.Float)
    total_programming = db.Column(db.Float)
    total_reading = db.Column(db.Float)
    total_plugin = db.Column(db.Float)
    total_ungraded = db.Column(db.Float)
    total_quiz = db.Column(db.Float)
    total_teammate = db.Column(db.Float)
    total_peer = db.Column(db.Float)
    total_discussion = db.Column(db.Float)
    total_video = db.Column(db.Float)

    # Boolean flags (stored as BIGINT in DB)
    has_assignment = db.Column(db.BigInteger)
    has_app = db.Column(db.BigInteger)
    has_programming = db.Column(db.BigInteger)
    has_reading = db.Column(db.BigInteger)
    has_plugin = db.Column(db.BigInteger)
    has_ungraded = db.Column(db.BigInteger)
    has_quiz = db.Column(db.BigInteger)
    has_teammate = db.Column(db.BigInteger)
    has_peer = db.Column(db.BigInteger)
    has_discussion = db.Column(db.BigInteger)
    has_video = db.Column(db.BigInteger)

    # Additional metadata
    has_no_enrol = db.Column(db.BigInteger)
    enrollments = db.Column(db.Float)
    has_rating = db.Column(db.BigInteger)
    subject = db.Column(db.Float)
    has_subject = db.Column(db.BigInteger)
    provider = db.Column(db.String(None))

    # Extra columns from actual database
    allowed_in = db.Column(db.String(None))
    value_per_lead_usa = db.Column(db.Float)
    recent_enrollment_count = db.Column(db.Float)
    card_image_url = db.Column(db.String(None))
    value_per_lead_international = db.Column(db.Float)
    blocked_in = db.Column(db.String(None))
    value_per_click_international = db.Column(db.Float)
    min_effort = db.Column(db.Float)
    subscription_prices = db.Column(db.String(None))
    product_marketing_video_url = db.Column(db.Float)
    uuid = db.Column(db.String(None))
    primary_description = db.Column(db.String(None))
    learning_type_exp = db.Column(db.String(None))
    course_titles = db.Column(db.String(None))
    objectID = db.Column(db.String(None))
    subscription_eligible = db.Column(db.Float)
    active_run_start = db.Column(db.Float)
    organization_short_code_override = db.Column(db.String(None))
    tags = db.Column(db.String(None))
    _highlightResult = db.Column(db.String(None))
    value_per_click_usa = db.Column(db.Float)
    product_source = db.Column(db.String(None))
    active_run_key = db.Column(db.Float)
    availability_rank = db.Column(db.Float)
    availability = db.Column(db.String(None))
    weeks_to_complete = db.Column(db.Float)
    owners = db.Column(db.String(None))
    max_effort = db.Column(db.Float)
    language = db.Column(db.String(None))
    contentful_fields = db.Column(db.Float)
    tertiary_description = db.Column(db.String(None))
    program_type = db.Column(db.String(None))
    partner_keys = db.Column(db.String(None))
    organization_logo_override = db.Column(db.String(None))
    active_run_type = db.Column(db.Float)
    product_key = db.Column(db.Float)
    external_url = db.Column(db.Float)
    meta_title = db.Column(db.Float)
    secondary_description = db.Column(db.String(None))
    learning_type = db.Column(db.String(None))
    display_on_org_page = db.Column(db.Float)
    _geoloc = db.Column(db.String(None))
    translation_languages = db.Column(db.String(None))

    def __repr__(self):
        return f'<Course {self.course_name}>'
