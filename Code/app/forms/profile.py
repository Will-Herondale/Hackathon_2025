from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, FieldList, FormField
from wtforms.validators import DataRequired, Length, URL, Optional


class SkillForm(FlaskForm):
    """Sub-form for skills"""
    name = StringField('Skill', validators=[DataRequired()])


class ProjectForm(FlaskForm):
    """Form for adding/editing projects"""
    title = StringField('Project Title', validators=[
        DataRequired(message='Title is required'),
        Length(max=200)
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(message='Description is required'),
        Length(max=2000)
    ])
    technologies = StringField('Technologies (comma-separated)', validators=[
        DataRequired(message='At least one technology is required')
    ])
    project_url = StringField('Project URL', validators=[Optional(), URL()])
    github_url = StringField('GitHub URL', validators=[Optional(), URL()])
    image = FileField('Project Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    featured = BooleanField('Feature this project')


class ProfileEditForm(FlaskForm):
    """Form for editing user profile"""
    name = StringField('Full Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100)
    ])
    bio = TextAreaField('Bio', validators=[
        Length(max=500, message='Bio must be less than 500 characters')
    ])
    title = StringField('Professional Title', validators=[
        Length(max=100)
    ])
    location = StringField('Location', validators=[
        Length(max=100)
    ])
    website = StringField('Website', validators=[Optional(), URL()])
    github = StringField('GitHub Username')
    linkedin = StringField('LinkedIn URL', validators=[Optional(), URL()])
    twitter = StringField('Twitter Handle')

    # Skills
    skills = StringField('Skills (comma-separated)', validators=[
        DataRequired(message='At least one skill is required')
    ])

    # Interests
    interests = StringField('Interests (comma-separated)')

    # Profile visibility
    profile_public = BooleanField('Make profile public')

    # Avatar
    avatar = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])

    # Resume
    resume = FileField('Resume (PDF)', validators=[
        FileAllowed(['pdf'], 'PDF files only!')
    ])
