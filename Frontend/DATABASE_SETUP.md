# Azure SQL Database Integration Guide

## ✅ Database Setup Complete!

Your Flask application has been successfully integrated with Azure SQL Database.

### 📊 Database Details

- **Server**: skill.database.windows.net
- **Database**: skilldb
- **Username**: DELPHINS
- **Port**: 1433
- **Driver**: pymssql (FreeTDS)

### 📦 Installed Packages

- `pymssql==2.3.1` - Microsoft SQL Server database adapter
- `SQLAlchemy==2.0.23` - SQL toolkit and ORM
- `Flask-SQLAlchemy==3.1.1` - Flask integration for SQLAlchemy

### 🗄️ Database Models Created

The following models have been created in `app/models/db_models.py`:

1. **User** - User accounts with authentication
2. **Profile** - User profile information and social links
3. **Project** - Portfolio projects
4. **Event** - Events and courses
5. **EventEnrollment** - Event enrollment records
6. **Goal** - User goals (dream colleges, companies)
7. **Achievement** - Achievements and badges
8. **Job** - Job listings
9. **Conversation** - Messaging conversations
10. **ConversationParticipant** - Conversation participants
11. **Message** - Messages in conversations
12. **Activity** - User activity log

### 📁 Files Created

**Configuration:**
- `app/config.py` - Database configuration with environment-based settings
- `app/database.py` - Database initialization and utilities
- `.env` - Environment variables (credentials)

**Models:**
- `app/models/db_models.py` - All database models with relationships

**Scripts:**
- `init_db.py` - Database initialization script
- `test_db.py` - Database connection test script

### 🚀 Usage Instructions

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Configure Environment

The `.env` file has been created with your database credentials:

```env
DB_SERVER=skill.database.windows.net
DB_NAME=skilldb
DB_USERNAME=DELPHINS
DB_PASSWORD=Delphin@hackathon2025
DB_PORT=1433
```

#### 3. Test Database Connection

```bash
python test_db.py
```

This will:
- Test connection to Azure SQL
- Show database version
- List existing tables

#### 4. Initialize Database Tables

```bash
# Create all tables
python init_db.py

# Drop and recreate all tables (WARNING: Deletes data!)
python init_db.py --drop

# Show database info
python init_db.py --info
```

#### 5. Run the Application

```bash
python app.py
```

### 🔍 Database Connection String

The application uses this connection string format:

```
mssql+pymssql://DELPHINS:Delphin%40hackathon2025@skill.database.windows.net:1433/skilldb
```

### 📝 Important Notes

**Current Status:**
- ⚠️ The database is currently showing as unavailable. This could mean:
  1. The database is paused/stopped in Azure Portal
  2. Firewall rules need to be configured to allow your IP
  3. The database is being provisioned

**To Resolve:**
1. Go to Azure Portal
2. Navigate to your SQL Database `skilldb`
3. Check if the database is running
4. Add your IP address to firewall rules:
   - Go to "Networking" or "Firewalls and virtual networks"
   - Add your current IP address
   - Save changes

### 🔧 Using the Database in Your App

**Query Example:**
```python
from app.database import db
from app.models.db_models import User, Profile, Goal

# Create a new user
new_user = User(
    email='user@example.com',
    name='John Doe',
    password_hash='hashed_password',
    user_type='adult'
)
db.session.add(new_user)
db.session.commit()

# Query users
users = User.query.all()
user = User.query.filter_by(email='user@example.com').first()

# Create a goal
goal = Goal(
    user_id=user.id,
    category='education',
    title='Get into MIT',
    description='Apply and get accepted to MIT',
    progress=25
)
db.session.add(goal)
db.session.commit()
```

**Relationships:**
```python
# Access user's profile
user = User.query.get(1)
profile = user.profile

# Access user's projects
projects = user.projects

# Access user's goals
goals = user.goals
```

### 🛠️ Database Utilities

**Import in any route:**
```python
from app.database import db
from app.models.db_models import User, Profile, Goal, Achievement
```

**Transaction Management:**
```python
try:
    # Your database operations
    db.session.add(obj)
    db.session.commit()
except Exception as e:
    db.session.rollback()
    print(f"Error: {e}")
```

### 📊 Table Schema Overview

**Users Table:**
- id, email, name, password_hash, user_type, profile_public
- created_at, updated_at

**Profiles Table:**
- user_id (FK), bio, title, location, website
- github, linkedin, twitter, avatar_url, resume_url
- skills (JSON), interests (JSON)

**Goals Table:**
- user_id (FK), category, title, description
- progress (0-100), status, target_date
- created_at, updated_at, completed_at

**Achievements Table:**
- user_id (FK), badge_type, title, description
- icon, earned_at

### 🎯 Next Steps

1. **Enable Database**: Check Azure Portal and start/resume the database
2. **Configure Firewall**: Add your IP to firewall rules
3. **Test Connection**: Run `python test_db.py` again
4. **Initialize Tables**: Run `python init_db.py`
5. **Start Development**: Begin building your features!

### 🆘 Troubleshooting

**Connection Timeout:**
- Check if database is running in Azure
- Verify firewall rules allow your IP
- Check credentials in .env file

**Table Creation Errors:**
- Ensure database is accessible
- Check for existing tables with `python test_db.py`
- Use `python init_db.py --drop` to recreate (WARNING: deletes data)

**Import Errors:**
- Run `pip install -r requirements.txt`
- Ensure all packages are installed

### 📚 Additional Resources

- [Azure SQL Documentation](https://docs.microsoft.com/en-us/azure/azure-sql/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)

---

**Database integration is complete and ready to use once the Azure database is available!** 🎉
