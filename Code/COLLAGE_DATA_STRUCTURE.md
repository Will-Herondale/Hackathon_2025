# Kids Mode College Collage - Data Structure Documentation

## Overview
This document describes the data structure for the Kids Mode College Collage feature. This feature allows young users to create a visual vision board of their dream colleges with motivational content.

---

## Database Table: `college_collages`

### Table Schema

| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Unique identifier for each collage entry |
| `user_id` | INTEGER | FOREIGN KEY (users.id), NOT NULL | References the user who owns this collage |
| `college_name` | VARCHAR(255) | NOT NULL | Name of the dream college (e.g., "MIT", "Stanford") |
| `college_logo_url` | VARCHAR(500) | NULLABLE | URL to the college logo image |
| `college_images` | TEXT | NULLABLE | JSON array of image URLs for inspiration board |
| `motivation_text` | TEXT | NULLABLE | Student's personal motivation quote/text |
| `why_this_college` | TEXT | NULLABLE | Reason why the student chose this college |
| `target_year` | INTEGER | NULLABLE | Target year for admission (e.g., 2028) |
| `display_order` | INTEGER | DEFAULT 0 | Order in which to display collages |
| `is_primary` | BOOLEAN | DEFAULT FALSE | Marks if this is the student's top choice |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | When the collage was created |
| `updated_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP, ON UPDATE | When the collage was last updated |

### Indexes
- `idx_user_collages` on `user_id` for efficient querying of user's collages

---

## JSON Data Format

### `college_images` Field
This field stores an array of image URLs as a JSON string.

**Format:**
```json
[
  "https://example.com/image1.jpg",
  "https://example.com/image2.jpg",
  "https://example.com/image3.jpg",
  "https://example.com/image4.jpg"
]
```

**Example:**
```json
[
  "https://cdn.mit.edu/campus.jpg",
  "https://cdn.mit.edu/dome.jpg",
  "https://cdn.mit.edu/students.jpg"
]
```

---

## API Endpoints

### 1. GET `/dashboard/collage`
**Description:** Display all college collages for the current user

**Response:** Renders HTML template with collage data

---

### 2. POST `/dashboard/collage/add`
**Description:** Add a new college to the user's collage

**Request Body (Form Data):**
```
college_name: string (required)
college_logo_url: string (optional)
motivation_text: text (optional)
why_this_college: text (optional)
target_year: integer (optional)
college_images[]: array of strings (optional, multiple URLs)
```

**Example cURL:**
```bash
curl -X POST http://localhost:5000/dashboard/collage/add \
  -H "Content-Type: multipart/form-data" \
  -F "college_name=Massachusetts Institute of Technology" \
  -F "college_logo_url=https://cdn.mit.edu/logo.png" \
  -F "motivation_text=I want to change the world through technology!" \
  -F "why_this_college=MIT has the best robotics program" \
  -F "target_year=2028" \
  -F "college_images[]=https://cdn.mit.edu/campus1.jpg" \
  -F "college_images[]=https://cdn.mit.edu/campus2.jpg"
```

**Response:**
```json
{
  "success": true,
  "collage": {
    "id": 1,
    "college_name": "Massachusetts Institute of Technology",
    "logo_url": "https://cdn.mit.edu/logo.png"
  }
}
```

---

### 3. POST `/dashboard/collage/<int:collage_id>/update`
**Description:** Update an existing collage entry

**Request Body (Form Data):**
```
college_name: string (optional)
college_logo_url: string (optional)
motivation_text: text (optional)
why_this_college: text (optional)
target_year: integer (optional)
is_primary: string "true"/"false" (optional)
college_images[]: array of strings (optional)
```

**Example cURL:**
```bash
curl -X POST http://localhost:5000/dashboard/collage/1/update \
  -F "motivation_text=Updated motivation text" \
  -F "is_primary=true"
```

**Response:**
```json
{
  "success": true
}
```

---

### 4. POST `/dashboard/collage/<int:collage_id>/delete`
**Description:** Delete a collage entry

**Response:**
```json
{
  "success": true
}
```

---

## Database Relationships

```
users (1) ─────< (many) college_collages
```

Each user can have multiple college collages, but each collage belongs to only one user.

---

## Sample Data for Testing

### Sample 1: MIT Entry
```json
{
  "user_id": 1,
  "college_name": "Massachusetts Institute of Technology",
  "college_logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/1200px-MIT_logo.svg.png",
  "college_images": "[\"https://news.mit.edu/sites/default/files/styles/news_article__image_gallery/public/images/202009/MIT-Campus-Aerial-01_0.jpg\", \"https://news.mit.edu/sites/default/files/styles/news_article__image_gallery/public/images/202009/MIT-Campus-02_0.jpg\"]",
  "motivation_text": "I want to become an engineer and change the world!",
  "why_this_college": "MIT has the best engineering programs and I love their hands-on approach to learning.",
  "target_year": 2028,
  "display_order": 0,
  "is_primary": true
}
```

### Sample 2: Stanford Entry
```json
{
  "user_id": 1,
  "college_name": "Stanford University",
  "college_logo_url": "https://identity.stanford.edu/wp-content/uploads/sites/3/2020/07/block-s-right.png",
  "college_images": "[\"https://www.stanford.edu/wp-content/uploads/2020/09/stanford-campus.jpg\"]",
  "motivation_text": "Innovation and entrepreneurship drive me forward!",
  "why_this_college": "Stanford is in Silicon Valley and has amazing startup programs.",
  "target_year": 2028,
  "display_order": 1,
  "is_primary": false
}
```

### Sample 3: Harvard Entry
```json
{
  "user_id": 1,
  "college_name": "Harvard University",
  "college_logo_url": "https://1000logos.net/wp-content/uploads/2017/02/Harvard-Logo.png",
  "college_images": "[\"https://www.harvard.edu/wp-content/uploads/2021/02/091520_Stock_KS_025.jpeg\", \"https://www.harvard.edu/wp-content/uploads/2021/02/091520_Stock_KS_045.jpeg\", \"https://www.harvard.edu/wp-content/uploads/2021/02/091520_Stock_KS_067.jpeg\"]",
  "motivation_text": "Excellence in everything I do!",
  "why_this_college": "Harvard has an amazing history and the best library system in the world.",
  "target_year": 2029,
  "display_order": 2,
  "is_primary": false
}
```

---

## Python Code Examples

### Adding Data Programmatically
```python
from app.models.db_models import CollegeCollage
from app.database import db
import json

# Create a new collage entry
collage = CollegeCollage(
    user_id=1,
    college_name="Massachusetts Institute of Technology",
    college_logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/1200px-MIT_logo.svg.png",
    college_images=json.dumps([
        "https://news.mit.edu/sites/default/files/images/MIT-Campus-Aerial.jpg",
        "https://news.mit.edu/sites/default/files/images/MIT-Dome.jpg"
    ]),
    motivation_text="I want to become an engineer and change the world!",
    why_this_college="MIT has the best engineering programs.",
    target_year=2028,
    is_primary=True,
    display_order=0
)

db.session.add(collage)
db.session.commit()
```

### Querying Data
```python
from app.models.db_models import CollegeCollage
import json

# Get all collages for a user
user_collages = CollegeCollage.query.filter_by(user_id=1).all()

# Get primary collage
primary_collage = CollegeCollage.query.filter_by(
    user_id=1,
    is_primary=True
).first()

# Parse images
for collage in user_collages:
    images = json.loads(collage.college_images) if collage.college_images else []
    print(f"{collage.college_name}: {len(images)} images")
```

---

## Migration Command

To create the database table, run:

```bash
# Create migration
flask db migrate -m "Add college_collages table for kids mode"

# Apply migration
flask db upgrade
```

Or if you're using the init_db.py script:

```bash
python init_db.py
```

---

## Notes for Backend Team

1. **JSON Handling**: Always use `json.dumps()` when storing arrays in `college_images` and `json.loads()` when reading them.

2. **Image URLs**: No file upload functionality yet - users provide image URLs. Future enhancement could add file upload support.

3. **Primary Collage**: Only one collage per user should have `is_primary=True`. When setting a new primary, unset the old one:
   ```python
   # Unset all primary collages for user
   CollegeCollage.query.filter_by(user_id=user_id, is_primary=True).update({'is_primary': False})
   # Set new primary
   new_primary.is_primary = True
   db.session.commit()
   ```

4. **Display Order**: Use this for custom sorting. Lower numbers appear first.

5. **Target Year**: Should be validated to be reasonable (between current year and 20 years in future).

6. **User Type Check**: Consider checking `user.user_type == 'kid'` before showing collage features in production.

---

## Future Enhancements

- [ ] Add file upload for images instead of URLs
- [ ] Add drag-and-drop reordering of collages
- [ ] Add achievement badges for adding collages
- [ ] Add sharing functionality to share collages with friends/family
- [ ] Add progress tracking toward college goals
- [ ] Add college statistics/facts integration
- [ ] Add collaborative collages (parent/teacher can add notes)
