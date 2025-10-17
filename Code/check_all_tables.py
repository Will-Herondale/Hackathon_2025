#!/usr/bin/env python
"""
Check all table structures (jobs, courses, events)
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.database import db
from sqlalchemy import inspect

def check_all_tables():
    """Check all table columns"""
    print("=" * 80)
    print("ALL TABLES STRUCTURE CHECK")
    print("=" * 80)

    app = create_app('development')

    with app.app_context():
        try:
            inspector = inspect(db.engine)

            # Check all tables
            for table_name in ['jobs', 'courses', 'events']:
                print(f"\n{'='*80}")
                print(f"TABLE: {table_name.upper()}")
                print(f"{'='*80}")

                columns = inspector.get_columns(table_name)
                print(f"\nTotal columns: {len(columns)}\n")

                for col in columns:
                    nullable = "NULL" if col['nullable'] else "NOT NULL"
                    print(f"  {col['name']:35} {str(col['type']):35} {nullable}")

                # Check primary keys
                pk = inspector.get_pk_constraint(table_name)
                if pk and pk.get('constrained_columns'):
                    print(f"\n  PRIMARY KEY: {pk['constrained_columns']}")
                else:
                    print(f"\n  PRIMARY KEY: None (WARNING!)")

            return True

        except Exception as e:
            print(f"\n✗ Check failed!")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = check_all_tables()
    sys.exit(0 if success else 1)
