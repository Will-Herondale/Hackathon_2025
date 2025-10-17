#!/usr/bin/env python
"""
Database Migration Script - Add new fields to existing tables
This script alters existing tables to add new columns without dropping data
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.database import db
from sqlalchemy import text

def migrate_database():
    """Add new fields to existing tables"""
    print("=" * 60)
    print("Database Schema Migration")
    print("=" * 60)

    app = create_app('development')

    with app.app_context():
        try:
            print("\n1. Testing database connection...")
            result = db.session.execute(text('SELECT 1'))
            result.fetchone()
            print("✓ Connected to database successfully")

            # Migration for JOBS table
            print("\n2. Migrating JOBS table - Adding new fields...")

            jobs_migrations = [
                "ALTER TABLE jobs ADD jobId NVARCHAR(255)",
                "ALTER TABLE jobs ADD currency NVARCHAR(10)",
                "ALTER TABLE jobs ADD jobUploaded DATETIME",
                "ALTER TABLE jobs ADD companyName NVARCHAR(255)",
                "ALTER TABLE jobs ADD tagsAndSkills NVARCHAR(MAX)",
                "ALTER TABLE jobs ADD experience NVARCHAR(100)",
                "ALTER TABLE jobs ADD companyId NVARCHAR(255)",
                "ALTER TABLE jobs ADD ReviewsCount INT DEFAULT 0",
                "ALTER TABLE jobs ADD AggregateRating FLOAT",
                "ALTER TABLE jobs ADD jobDescription NVARCHAR(MAX)",
                "ALTER TABLE jobs ADD minimumSalary INT",
                "ALTER TABLE jobs ADD maximumSalary INT",
                "ALTER TABLE jobs ADD minimumExperience INT",
                "ALTER TABLE jobs ADD maximumExperience INT",
            ]

            for migration_sql in jobs_migrations:
                try:
                    db.session.execute(text(migration_sql))
                    db.session.commit()
                    column_name = migration_sql.split('ADD')[1].split()[0]
                    print(f"  ✓ Added column: {column_name}")
                except Exception as e:
                    if "already exists" in str(e) or "duplicate" in str(e).lower():
                        column_name = migration_sql.split('ADD')[1].split()[0]
                        print(f"  ⊙ Column already exists: {column_name}")
                        db.session.rollback()
                    else:
                        print(f"  ✗ Error: {str(e)}")
                        db.session.rollback()

            # Copy old data to new fields if needed
            print("\n3. Migrating existing data...")
            try:
                # Copy 'company' to 'companyName' if companyName is NULL
                db.session.execute(text(
                    "UPDATE jobs SET companyName = company WHERE companyName IS NULL AND company IS NOT NULL"
                ))
                # Copy 'description' to 'jobDescription' if jobDescription is NULL
                db.session.execute(text(
                    "UPDATE jobs SET jobDescription = description WHERE jobDescription IS NULL AND description IS NOT NULL"
                ))
                # Copy 'skills' to 'tagsAndSkills' if tagsAndSkills is NULL
                db.session.execute(text(
                    "UPDATE jobs SET tagsAndSkills = skills WHERE tagsAndSkills IS NULL AND skills IS NOT NULL"
                ))
                db.session.commit()
                print("  ✓ Migrated existing job data to new fields")
            except Exception as e:
                print(f"  ⚠ Warning during data migration: {str(e)}")
                db.session.rollback()

            # Note: COURSES table already exists based on test_db.py output
            # Check if it needs any schema updates
            print("\n4. Checking COURSES table...")
            try:
                result = db.session.execute(text(
                    "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'courses'"
                ))
                count = result.fetchone()[0]
                print(f"  ✓ Courses table exists with {count} columns")
            except Exception as e:
                print(f"  ℹ Courses table info: {str(e)}")

            # Check EVENTS table for registration_url
            print("\n5. Checking EVENTS table...")
            try:
                result = db.session.execute(text(
                    "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'events' AND COLUMN_NAME = 'registration_url'"
                ))
                has_field = result.fetchone()[0]
                if has_field:
                    print("  ✓ Events table already has registration_url field")
                else:
                    db.session.execute(text("ALTER TABLE events ADD registration_url NVARCHAR(500)"))
                    db.session.commit()
                    print("  ✓ Added registration_url to events table")
            except Exception as e:
                print(f"  ⚠ Events table check: {str(e)}")
                db.session.rollback()

            print("\n" + "=" * 60)
            print("Migration completed successfully!")
            print("=" * 60)
            print("\nNext steps:")
            print("  1. Review the changes above")
            print("  2. Test your application with: python app.py")
            print("  3. Check that data displays correctly")
            print("=" * 60)

            return True

        except Exception as e:
            print(f"\n✗ Migration failed!")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = migrate_database()
    sys.exit(0 if success else 1)
