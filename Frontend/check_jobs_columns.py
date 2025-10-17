#!/usr/bin/env python
"""
Check actual jobs table columns
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.database import db
from sqlalchemy import inspect

def check_jobs_columns():
    """Check jobs table columns"""
    print("=" * 60)
    print("Jobs Table Column Check")
    print("=" * 60)

    app = create_app('development')

    with app.app_context():
        try:
            inspector = inspect(db.engine)

            # Check JOBS table
            print("\n✓ JOBS TABLE - ALL COLUMNS:")
            jobs_columns = inspector.get_columns('jobs')

            print(f"\nTotal columns: {len(jobs_columns)}\n")

            for col in jobs_columns:
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                print(f"  {col['name']:30} {str(col['type']):30} {nullable}")

            # Check primary keys
            print("\n✓ PRIMARY KEYS:")
            pk = inspector.get_pk_constraint('jobs')
            print(f"  {pk}")

            return True

        except Exception as e:
            print(f"\n✗ Check failed!")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = check_jobs_columns()
    sys.exit(0 if success else 1)
