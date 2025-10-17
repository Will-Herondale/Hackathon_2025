#!/usr/bin/env python
"""
Database connection test script
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.database import db
from sqlalchemy import text


def test_connection():
    """Test database connection"""
    print("=" * 60)
    print("Database Connection Test")
    print("=" * 60)

    print(f"\nServer: {os.getenv('DB_SERVER')}")
    print(f"Database: {os.getenv('DB_NAME')}")
    print(f"Username: {os.getenv('DB_USERNAME')}")
    print(f"Port: {os.getenv('DB_PORT')}")
    print()

    print("Testing connection...")
    app = create_app('development')

    with app.app_context():
        try:
            # Test basic query
            result = db.session.execute(text('SELECT 1 as test'))
            row = result.fetchone()
            print(f"✓ Connection successful! Test query returned: {row[0]}")

            # Get database version
            result = db.session.execute(text('SELECT @@VERSION'))
            version = result.fetchone()
            print(f"\n✓ Database Version:")
            print(f"  {version[0][:100]}...")

            # List existing tables
            print(f"\n✓ Checking existing tables...")
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()

            if tables:
                print(f"  Found {len(tables)} tables:")
                for table in tables:
                    print(f"    - {table}")
            else:
                print("  No tables found. Run 'python init_db.py' to create them.")

            print("\n" + "=" * 60)
            print("Connection test completed successfully!")
            print("=" * 60)
            return True

        except Exception as e:
            print(f"\n✗ Connection failed!")
            print(f"Error: {str(e)}")
            print("\nPlease check your database credentials in .env file")
            print("=" * 60)
            return False


if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)
