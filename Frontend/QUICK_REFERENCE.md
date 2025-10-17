# Quick Reference: Direct Database Usage

This guide provides quick examples of how to use the database directly in your routes.

## Import Statements

```python
from app.models.db_models import User, Profile, Project, Event, EventEnrollment, Goal, Achievement, Job, Conversation, Message
from app.database import db
from flask_login import current_user
import json
```

## Common Database Operations

### 1. Querying Users

```python
# Get user by ID
user = User.query.get(user_id)

# Get user by email
user = User.query.filter_by(email='user@example.com').first()

# Get all users
users = User.query.all()

# Get users with filter
adult_users = User.query.filter_by(user_type='adult').all()
```

### 2. Creating Records

```python
# Create a new user
from werkzeug.security import generate_password_hash

user = User(
    name='John Doe',
    email='john@example.com',
    password_hash=generate_password_hash('password123'),
    user_type='adult'
)
db.session.add(user)
db.session.commit()

# Create a profile
profile = Profile(
    user_id=user.id,
    bio='Hello world',
    skills=json.dumps(['Python', 'JavaScript'])
)
db.session.add(profile)
db.session.commit()
```

### 3. Updating Records

```python
# Update a user
user = User.query.get(user_id)
user.name = 'Jane Doe'
user.user_type = 'kid'
db.session.commit()

# Update profile
profile = Profile.query.filter_by(user_id=user_id).first()
profile.bio = 'New bio'
profile.skills = json.dumps(['Python', 'JavaScript', 'React'])
db.session.commit()
```

### 4. Deleting Records

```python
# Delete a project
project = Project.query.get(project_id)
db.session.delete(project)
db.session.commit()

# Delete with verification
project = Project.query.get_or_404(project_id)
if project.user_id == current_user.id:
    db.session.delete(project)
    db.session.commit()
```

### 5. Relationships

```python
# Access related data
user = User.query.get(user_id)
profile = user.profile  # One-to-one relationship
projects = user.projects  # One-to-many relationship
goals = user.goals

# Reverse relationship
project = Project.query.get(project_id)
owner = project.user
```

### 6. Filtering and Queries

```python
# Filter with multiple conditions
events = Event.query.filter_by(
    category='programming',
    level='beginner'
).all()

# Filter with comparison operators
from datetime import datetime
upcoming_events = Event.query.filter(
    Event.start_date >= datetime.utcnow()
).order_by(Event.start_date.asc()).all()

# Count records
total_projects = Project.query.filter_by(user_id=user_id).count()
```

### 7. Pagination

```python
# Paginate results
page = request.args.get('page', 1, type=int)
per_page = 20

events_pagination = Event.query.order_by(
    Event.created_at.desc()
).paginate(page=page, per_page=per_page, error_out=False)

events = events_pagination.items
total_pages = events_pagination.pages
has_next = events_pagination.has_next
has_prev = events_pagination.has_prev
```

### 8. Joins

```python
# Join tables
from sqlalchemy import and_

# Get user's enrolled events
enrolled_events = Event.query.join(EventEnrollment).filter(
    and_(
        EventEnrollment.user_id == current_user.id,
        EventEnrollment.status == 'enrolled'
    )
).all()
```

### 9. Aggregations

```python
from sqlalchemy import func

# Count enrollments per event
enrollment_counts = db.session.query(
    Event.id,
    Event.title,
    func.count(EventEnrollment.id).label('enrollment_count')
).join(EventEnrollment).group_by(Event.id, Event.title).all()
```

### 10. JSON Fields

```python
# Storing JSON data
skills = ['Python', 'JavaScript', 'React']
profile.skills = json.dumps(skills)
db.session.commit()

# Reading JSON data
profile = Profile.query.filter_by(user_id=user_id).first()
if profile.skills:
    skills = json.loads(profile.skills)
else:
    skills = []
```

## Password Handling

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hash password
password_hash = generate_password_hash('mypassword')

# Verify password
user = User.query.filter_by(email=email).first()
if user and check_password_hash(user.password_hash, password):
    # Password is correct
    login_user(user)
```

## Error Handling

```python
# Get or 404
user = User.query.get_or_404(user_id)  # Returns 404 if not found

# Try/except for database errors
try:
    db.session.add(new_record)
    db.session.commit()
except Exception as e:
    db.session.rollback()
    flash('An error occurred', 'danger')
    app.logger.error(f'Database error: {e}')
```

## Transaction Management

```python
# Explicit transaction
try:
    user = User(name='Test', email='test@example.com', ...)
    db.session.add(user)
    db.session.flush()  # Get the ID without committing

    profile = Profile(user_id=user.id, bio='Test bio')
    db.session.add(profile)

    db.session.commit()  # Commit everything
except Exception as e:
    db.session.rollback()  # Rollback on error
    raise
```

## Common Patterns

### Check if exists

```python
# Check if enrollment exists
existing = EventEnrollment.query.filter_by(
    user_id=current_user.id,
    event_id=event_id
).first()

if existing:
    flash('Already enrolled', 'warning')
else:
    # Create enrollment
    pass
```

### Get or create

```python
# Get profile or create if doesn't exist
profile = Profile.query.filter_by(user_id=user_id).first()
if not profile:
    profile = Profile(user_id=user_id)
    db.session.add(profile)
    db.session.flush()

# Now update profile
profile.bio = 'Updated bio'
db.session.commit()
```

### Ownership verification

```python
project = Project.query.get_or_404(project_id)
if project.user_id != current_user.id:
    flash('You do not have permission', 'danger')
    return redirect(url_for('main.index'))

# User owns the project, proceed with operation
```

## Tips

1. Always use `db.session.commit()` after making changes
2. Use `db.session.rollback()` if an error occurs
3. Use `filter_by()` for simple equality checks
4. Use `filter()` for complex conditions
5. Use `first()` to get one result or `all()` for multiple
6. Use `get()` when searching by primary key
7. Use `get_or_404()` to automatically return 404 if not found
8. Always verify ownership before modifying/deleting records
9. Use JSON for storing arrays and objects in TEXT fields
10. Use indexes on frequently queried fields for better performance

## Migration from API to Database

### Before (API)
```python
response = APIClient.get(f'users/{user_id}')
user_data = response.get('user', {})
```

### After (Database)
```python
user = User.query.get(user_id)
# Access user.name, user.email, etc. directly
```

---

For more details, see `MIGRATION_SUMMARY.md`
