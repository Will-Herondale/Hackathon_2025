from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DateTimeField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, URL, Optional, NumberRange
from datetime import datetime


class EventCreateForm(FlaskForm):
    """Form for creating events/courses"""
    title = StringField('Event Title', validators=[
        DataRequired(message='Title is required'),
        Length(max=200)
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(message='Description is required'),
        Length(max=2000)
    ])
    event_type = SelectField('Type', choices=[
        ('workshop', 'Workshop'),
        ('course', 'Course'),
        ('webinar', 'Webinar'),
        ('meetup', 'Meetup'),
        ('hackathon', 'Hackathon'),
        ('conference', 'Conference')
    ], validators=[DataRequired()])

    category = SelectField('Category', choices=[
        ('programming', 'Programming'),
        ('design', 'Design'),
        ('business', 'Business'),
        ('marketing', 'Marketing'),
        ('data-science', 'Data Science'),
        ('ai-ml', 'AI & Machine Learning'),
        ('career', 'Career Development'),
        ('soft-skills', 'Soft Skills')
    ], validators=[DataRequired()])

    level = SelectField('Difficulty Level', choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('all', 'All Levels')
    ], validators=[DataRequired()])

    start_date = DateTimeField('Start Date & Time', format='%Y-%m-%dT%H:%M', validators=[
        DataRequired(message='Start date is required')
    ])
    end_date = DateTimeField('End Date & Time', format='%Y-%m-%dT%H:%M', validators=[
        DataRequired(message='End date is required')
    ])

    location_type = SelectField('Location Type', choices=[
        ('online', 'Online'),
        ('in-person', 'In-Person'),
        ('hybrid', 'Hybrid')
    ], validators=[DataRequired()])

    location = StringField('Location/Meeting Link', validators=[
        DataRequired(message='Location or meeting link is required'),
        Length(max=500)
    ])

    max_participants = IntegerField('Maximum Participants', validators=[
        Optional(),
        NumberRange(min=1, max=10000)
    ])

    price = IntegerField('Price (0 for free)', default=0, validators=[
        Optional(),
        NumberRange(min=0)
    ])

    tags = StringField('Tags (comma-separated)')

    registration_url = StringField('Registration URL', validators=[
        Optional(),
        URL(message='Must be a valid URL'),
        Length(max=500)
    ])

    image = FileField('Event Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])

    featured = BooleanField('Feature this event')

    age_appropriate_for_kids = BooleanField('Appropriate for students (kid mode)')


class EventEnrollForm(FlaskForm):
    """Form for enrolling in events"""
    notes = TextAreaField('Notes (optional)', validators=[
        Length(max=500)
    ])
