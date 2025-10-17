#!/usr/bin/env python
"""
Add application_url column to jobs table
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.database import db
from sqlalchemy import text

def add_application_url_column():
    """Add application_url column to jobs table"""
    print("=" * 60)
    print("Adding application_url column to jobs table")
    print("=" * 60)

    app = create_app('development')

    with app.app_context():
        try:
            print("\nChecking if column already exists...")

            # Check if column exists
            result = db.session.execute(text(
                "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'jobs' AND COLUMN_NAME = 'application_url'"
            ))
            exists = result.fetchone()[0]

            if exists:
                print("✓ Column 'application_url' already exists in jobs table")
                return True

            print("Adding application_url column...")

            # Add the column
            db.session.execute(text("ALTER TABLE jobs ADD application_url NVARCHAR(500)"))
            db.session.commit()

            print("✓ Successfully added application_url column to jobs table")

            return True

        except Exception as e:
            print(f"\n✗ Failed to add column!")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = add_application_url_column()
    sys.exit(0 if success else 1)
