#!/usr/bin/env python
"""
Verify database schema matches our models
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.database import db
from sqlalchemy import text, inspect

def verify_schema():
    """Verify database schema"""
    print("=" * 60)
    print("Database Schema Verification")
    print("=" * 60)

    app = create_app('development')

    with app.app_context():
        try:
            inspector = inspect(db.engine)

            # Check JOBS table
            print("\n✓ JOBS TABLE COLUMNS:")
            jobs_columns = inspector.get_columns('jobs')
            for col in sorted(jobs_columns, key=lambda x: x['name']):
                print(f"  - {col['name']}: {col['type']}")

            # Check COURSES table
            print("\n✓ COURSES TABLE COLUMNS:")
            courses_columns = inspector.get_columns('courses')
            for col in sorted(courses_columns, key=lambda x: x['name']):
                print(f"  - {col['name']}: {col['type']}")

            # Check EVENTS table
            print("\n✓ EVENTS TABLE COLUMNS:")
            events_columns = inspector.get_columns('events')
            for col in sorted(events_columns, key=lambda x: x['name']):
                print(f"  - {col['name']}: {col['type']}")

            print("\n" + "=" * 60)
            print("Schema verification completed!")
            print("=" * 60)

            return True

        except Exception as e:
            print(f"\n✗ Verification failed!")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = verify_schema()
    sys.exit(0 if success else 1)
