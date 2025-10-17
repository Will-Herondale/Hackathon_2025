#!/usr/bin/env python
"""
Create colleges table in the database
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.database import db
from sqlalchemy import text

def create_colleges_table():
    """Create colleges table with all required columns"""
    print("=" * 60)
    print("Creating colleges table")
    print("=" * 60)

    app = create_app('development')

    with app.app_context():
        try:
            print("\nChecking if table already exists...")

            # Check if table exists
            result = db.session.execute(text(
                "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'colleges'"
            ))
            exists = result.fetchone()[0]

            if exists:
                print("✓ Table 'colleges' already exists")
                return True

            print("Creating colleges table...")

            # Create the table
            create_table_sql = """
            CREATE TABLE colleges (
                id INT IDENTITY(1,1) PRIMARY KEY,
                college_name NVARCHAR(500) NOT NULL,
                stream NVARCHAR(255),
                state NVARCHAR(255),
                city NVARCHAR(255),
                entrance_exams NVARCHAR(MAX),
                eligibility_criteria NVARCHAR(MAX),
                required_skills NVARCHAR(MAX),
                typical_exam_cutoffs NVARCHAR(MAX),
                fee_structure NVARCHAR(MAX),
                seat_intake INT,
                college_type NVARCHAR(100),
                tier_rank NVARCHAR(50),
                website_url NVARCHAR(500),
                placement_average_salary FLOAT,
                located_in_campus BIT DEFAULT 1,
                year_established INT,
                accreditation NVARCHAR(255),
                gender_ratio NVARCHAR(50),
                created_at DATETIME2 DEFAULT GETDATE(),
                updated_at DATETIME2 DEFAULT GETDATE()
            )
            """

            db.session.execute(text(create_table_sql))
            db.session.commit()

            print("✓ Successfully created colleges table")

            # Create indexes
            print("\nCreating indexes...")

            indexes = [
                "CREATE INDEX idx_college_state_city ON colleges(state, city)",
                "CREATE INDEX idx_college_stream ON colleges(stream)",
                "CREATE INDEX idx_college_type ON colleges(college_type)"
            ]

            for idx_sql in indexes:
                db.session.execute(text(idx_sql))

            db.session.commit()
            print("✓ Successfully created indexes")

            return True

        except Exception as e:
            print(f"\n✗ Failed to create table!")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = create_colleges_table()
    sys.exit(0 if success else 1)
