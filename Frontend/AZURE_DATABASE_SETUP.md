# Azure Database Setup for College Collage Feature

## For Your Backend Teammate Using Azure

This document explains how to access and populate the Azure database with college collage data.

---

## Option 1: Using Azure Portal SQL Query Editor

### Step 1: Access Azure Portal
1. Go to https://portal.azure.com
2. Sign in with your Azure credentials
3. Navigate to **SQL databases**
4. Select your database (likely named something like `chirec-db`)

### Step 2: Open Query Editor
1. In the left sidebar, click **Query editor (preview)**
2. Login with your database credentials
3. You'll see a SQL query interface

### Step 3: Create the Table (If Not Created Yet)
Run this SQL to create the `college_collages` table:

```sql
CREATE TABLE college_collages (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    college_name VARCHAR(255) NOT NULL,
    college_logo_url VARCHAR(500),
    college_images TEXT,
    motivation_text TEXT,
    why_this_college TEXT,
    target_year INT,
    display_order INT DEFAULT 0,
    is_primary BIT DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_user_collages ON college_collages(user_id);
```

### Step 4: Insert Sample Data
Use these INSERT statements to add sample college data:

```sql
-- MIT Entry (Primary Dream College)
INSERT INTO college_collages (
    user_id,
    college_name,
    college_logo_url,
    college_images,
    motivation_text,
    why_this_college,
    target_year,
    is_primary,
    display_order
) VALUES (
    1, -- Change this to your test user's ID
    'Massachusetts Institute of Technology',
    'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/1200px-MIT_logo.svg.png',
    '["https://news.mit.edu/sites/default/files/styles/news_article__image_gallery/public/images/202009/MIT-Campus-Aerial-01_0.jpg", "https://news.mit.edu/sites/default/files/styles/news_article__image_gallery/public/images/202009/MIT-Dome.jpg", "https://news.mit.edu/sites/default/files/styles/news_article__image_gallery/public/images/202009/MIT-Students.jpg"]',
    'I want to become an engineer and change the world through technology!',
    'MIT has the best engineering programs in the world and I love their hands-on approach to learning. The innovation culture inspires me every day!',
    2028,
    1,
    0
);

-- Stanford Entry
INSERT INTO college_collages (
    user_id,
    college_name,
    college_logo_url,
    college_images,
    motivation_text,
    why_this_college,
    target_year,
    is_primary,
    display_order
) VALUES (
    1, -- Change this to your test user's ID
    'Stanford University',
    'https://identity.stanford.edu/wp-content/uploads/sites/3/2020/07/block-s-right.png',
    '["https://www.stanford.edu/wp-content/uploads/2020/09/stanford-campus.jpg", "https://www.stanford.edu/wp-content/uploads/2020/09/hoover-tower.jpg"]',
    'Innovation and entrepreneurship drive me forward every single day!',
    'Stanford is in Silicon Valley and has amazing startup programs. I dream of creating my own company someday!',
    2028,
    0,
    1
);

-- Harvard Entry
INSERT INTO college_collages (
    user_id,
    college_name,
    college_logo_url,
    college_images,
    motivation_text,
    why_this_college,
    target_year,
    is_primary,
    display_order
) VALUES (
    1, -- Change this to your test user's ID
    'Harvard University',
    'https://1000logos.net/wp-content/uploads/2017/02/Harvard-Logo.png',
    '["https://www.harvard.edu/wp-content/uploads/2021/02/091520_Stock_KS_025.jpeg", "https://www.harvard.edu/wp-content/uploads/2021/02/091520_Stock_KS_045.jpeg", "https://www.harvard.edu/wp-content/uploads/2021/02/091520_Stock_KS_067.jpeg", "https://www.harvard.edu/wp-content/uploads/2021/02/widener-library.jpg"]',
    'Excellence in everything I do! I want to be the best version of myself!',
    'Harvard has an amazing history and the best library system in the world. The academic environment is unmatched!',
    2029,
    0,
    2
);

-- UC Berkeley Entry
INSERT INTO college_collages (
    user_id,
    college_name,
    college_logo_url,
    college_images,
    motivation_text,
    why_this_college,
    target_year,
    is_primary,
    display_order
) VALUES (
    1, -- Change this to your test user's ID
    'UC Berkeley',
    'https://brand.berkeley.edu/wp-content/uploads/2020/10/ucbseal_139_540.png',
    '["https://www.berkeley.edu/wp-content/uploads/2021/09/campus-aerial.jpg", "https://www.berkeley.edu/wp-content/uploads/2021/09/sather-gate.jpg"]',
    'Go Bears! I want to be part of the Cal spirit!',
    'Berkeley is known for its amazing research opportunities and diverse student body. Plus, California weather is great!',
    2028,
    0,
    3
);

-- Carnegie Mellon Entry
INSERT INTO college_collages (
    user_id,
    college_name,
    college_logo_url,
    college_images,
    motivation_text,
    why_this_college,
    target_year,
    is_primary,
    display_order
) VALUES (
    1, -- Change this to your test user's ID
    'Carnegie Mellon University',
    'https://www.cmu.edu/brand/brand-guidelines/images/seal-1.png',
    '["https://www.cmu.edu/homepage/images/campus-aerial.jpg", "https://www.cmu.edu/homepage/images/gates-center.jpg", "https://www.cmu.edu/homepage/images/students-collaboration.jpg"]',
    'I love computer science and robotics - CMU is the place to be!',
    'Carnegie Mellon has the #1 computer science program and amazing AI research. I want to build intelligent robots!',
    2028,
    0,
    4
);
```

**IMPORTANT**: Change `user_id` value from `1` to match an actual user ID in your database!

---

## Option 2: Using Azure Data Studio

### Step 1: Install Azure Data Studio
1. Download from: https://docs.microsoft.com/en-us/sql/azure-data-studio/download
2. Install and launch the application

### Step 2: Connect to Azure SQL Database
1. Click **New Connection**
2. Enter your connection details:
   - **Server**: `your-server.database.windows.net`
   - **Authentication type**: SQL Login
   - **User name**: Your admin username
   - **Password**: Your admin password
   - **Database**: Select your database name
3. Click **Connect**

### Step 3: Run SQL Queries
1. Click **New Query** button
2. Copy and paste the SQL statements from Option 1 above
3. Click **Run** or press F5

---

## Option 3: Using Python Script (Recommended for Multiple Entries)

### Step 1: Install Required Package
```bash
pip install pyodbc
```

### Step 2: Create Python Script
Create a file called `populate_collages.py`:

```python
import pyodbc
import json

# Azure SQL Database connection string
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:your-server.database.windows.net,1433;"
    "Database=your-database-name;"
    "Uid=your-username;"
    "Pwd=your-password;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Sample college data
colleges = [
    {
        "user_id": 1,  # CHANGE THIS
        "college_name": "Massachusetts Institute of Technology",
        "college_logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/1200px-MIT_logo.svg.png",
        "college_images": [
            "https://news.mit.edu/sites/default/files/styles/news_article__image_gallery/public/images/202009/MIT-Campus-Aerial-01_0.jpg",
            "https://news.mit.edu/sites/default/files/styles/news_article__image_gallery/public/images/202009/MIT-Dome.jpg"
        ],
        "motivation_text": "I want to become an engineer and change the world!",
        "why_this_college": "MIT has the best engineering programs.",
        "target_year": 2028,
        "is_primary": True,
        "display_order": 0
    },
    {
        "user_id": 1,  # CHANGE THIS
        "college_name": "Stanford University",
        "college_logo_url": "https://identity.stanford.edu/wp-content/uploads/sites/3/2020/07/block-s-right.png",
        "college_images": [
            "https://www.stanford.edu/wp-content/uploads/2020/09/stanford-campus.jpg"
        ],
        "motivation_text": "Innovation drives me!",
        "why_this_college": "Stanford is in Silicon Valley!",
        "target_year": 2028,
        "is_primary": False,
        "display_order": 1
    }
]

# Connect and insert
try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    for college in colleges:
        cursor.execute("""
            INSERT INTO college_collages
            (user_id, college_name, college_logo_url, college_images,
             motivation_text, why_this_college, target_year, is_primary, display_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            college["user_id"],
            college["college_name"],
            college["college_logo_url"],
            json.dumps(college["college_images"]),
            college["motivation_text"],
            college["why_this_college"],
            college["target_year"],
            1 if college["is_primary"] else 0,
            college["display_order"]
        ))

    conn.commit()
    print(f"Successfully inserted {len(colleges)} college entries!")

except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()
```

### Step 3: Run the Script
```bash
python populate_collages.py
```

---

## Option 4: Using Flask App Directly (If App is Deployed on Azure)

### Step 1: SSH into Azure App Service
```bash
az webapp ssh --name your-app-name --resource-group your-resource-group
```

### Step 2: Open Python Shell
```bash
cd /home/site/wwwroot
python
```

### Step 3: Insert Data Using Flask ORM
```python
from app import create_app, db
from app.models.db_models import CollegeCollage
import json

app = create_app()
with app.app_context():
    # Create MIT entry
    mit = CollegeCollage(
        user_id=1,  # CHANGE THIS
        college_name="Massachusetts Institute of Technology",
        college_logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/1200px-MIT_logo.svg.png",
        college_images=json.dumps([
            "https://news.mit.edu/sites/default/files/styles/news_article__image_gallery/public/images/202009/MIT-Campus-Aerial-01_0.jpg",
            "https://news.mit.edu/sites/default/files/styles/news_article__image_gallery/public/images/202009/MIT-Dome.jpg"
        ]),
        motivation_text="I want to become an engineer and change the world!",
        why_this_college="MIT has the best engineering programs in the world!",
        target_year=2028,
        is_primary=True,
        display_order=0
    )

    db.session.add(mit)
    db.session.commit()
    print(f"Added: {mit.college_name}")
```

---

## Finding Your User ID

Before inserting data, you need to find a valid user ID:

### SQL Query to Find Users:
```sql
SELECT id, email, name, user_type FROM users;
```

Look for a user with `user_type = 'kid'` if you want to test the kids mode feature.

### Or Create a Test User:
```sql
INSERT INTO users (email, name, password_hash, user_type)
VALUES ('testkid@example.com', 'Test Kid', 'hashed_password_here', 'kid');

SELECT id FROM users WHERE email = 'testkid@example.com';
```

---

## Verifying the Data

After inserting, verify with:

```sql
-- View all collages
SELECT * FROM college_collages;

-- View collages for a specific user
SELECT
    id,
    college_name,
    target_year,
    is_primary,
    display_order
FROM college_collages
WHERE user_id = 1  -- Change to your user ID
ORDER BY is_primary DESC, display_order ASC;

-- Count collages per user
SELECT
    user_id,
    COUNT(*) as collage_count
FROM college_collages
GROUP BY user_id;
```

---

## Common Issues & Solutions

### Issue 1: "Invalid object name 'college_collages'"
**Solution**: Run the CREATE TABLE statement first (see Option 1, Step 3)

### Issue 2: "Foreign key constraint failed"
**Solution**: Make sure the `user_id` you're using exists in the `users` table

### Issue 3: "Cannot insert duplicate key"
**Solution**: The data was already inserted. Use UPDATE instead or delete existing records first

### Issue 4: "Login failed for user"
**Solution**: Check your Azure SQL firewall rules - add your IP address in Azure Portal → SQL Database → Firewalls and virtual networks

---

## Quick Reference: Connection Strings

### Azure SQL Database Connection String Format:
```
Server=tcp:your-server.database.windows.net,1433;
Database=your-database;
User ID=your-username;
Password=your-password;
Encrypt=yes;
TrustServerCertificate=no;
```

### For Flask SQLAlchemy (in your .env or config):
```
DATABASE_URL=mssql+pyodbc://username:password@your-server.database.windows.net:1433/your-database?driver=ODBC+Driver+18+for+SQL+Server
```

---

## Need Help?

If you encounter issues:
1. Check Azure Portal for database activity logs
2. Verify firewall settings allow your IP
3. Ensure the table schema matches exactly
4. Test connection with Azure Data Studio first
5. Check application logs in Azure App Service

---

## Image URL Tips

Use these reliable sources for college images:
- **Official College Websites**: Most reliable
- **Wikimedia Commons**: Free to use
- **Unsplash**: High-quality campus photos
- **College's official press/media pages**: Usually have logo downloads

Make sure images are:
- Publicly accessible (HTTPS URLs)
- Reasonable file sizes
- Appropriate for kids to view
