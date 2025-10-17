#!/usr/bin/env python
"""
Database initialization script
Creates all tables in the Azure SQL database
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.database import db, create_tables, drop_tables
from app.models import db_models  # Import to register models


def init_database(drop_existing=False):
    """Initialize database tables"""
    print("=" * 60)
    print("Database Initialization Script")
    print("=" * 60)

    # Create Flask app
    print("\n1. Creating Flask application...")
    app = create_app('development')

    with app.app_context():
        print("✓ Flask app created successfully\n")

        # Test connection
        print("2. Testing database connection...")
        try:
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            print("✓ Database connection successful\n")
        except Exception as e:
            print(f"✗ Database connection failed: {str(e)}")
            return False

        # Drop existing tables if requested
        if drop_existing:
            print("3. Dropping existing tables...")
            try:
                drop_tables()
                print("✓ Existing tables dropped\n")
            except Exception as e:
                print(f"⚠ Warning: Could not drop tables: {str(e)}\n")

        # Create tables
        print("4. Creating database tables...")
        try:
            create_tables()
            print("✓ All tables created successfully\n")

            # List created tables
            print("5. Created tables:")
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            for table in tables:
                print(f"   - {table}")

            print(f"\n✓ Total tables: {len(tables)}")
            print("\n" + "=" * 60)
            print("Database initialization completed successfully!")
            print("=" * 60)
            return True

        except Exception as e:
            print(f"✗ Error creating tables: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def show_database_info():
    """Display database connection information"""
    print("\nDatabase Configuration:")
    print(f"  Server: {os.getenv('DB_SERVER')}")
    print(f"  Database: {os.getenv('DB_NAME')}")
    print(f"  Username: {os.getenv('DB_USERNAME')}")
    print(f"  Port: {os.getenv('DB_PORT')}")
    print(f"  Driver: {os.getenv('DB_DRIVER')}")
    print()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Initialize database tables')
    parser.add_argument('--drop', action='store_true',
                       help='Drop existing tables before creating new ones')
    parser.add_argument('--info', action='store_true',
                       help='Show database connection information')

    args = parser.parse_args()

    if args.info:
        show_database_info()
    else:
        if args.drop:
            confirm = input("⚠️  This will DROP all existing tables. Are you sure? (yes/no): ")
            if confirm.lower() != 'yes':
                print("Aborted.")
                sys.exit(0)

        success = init_database(drop_existing=args.drop)
        sys.exit(0 if success else 1)
