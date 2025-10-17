"""
Migration script to add registration_url column to events table
Run this once to update your existing database
"""
from app import create_app
from app.database import db
from sqlalchemy import text

def migrate():
    app = create_app()

    with app.app_context():
        try:
            # Check if column already exists
            result = db.session.execute(text("""
                SELECT COUNT(*)
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'events'
                AND COLUMN_NAME = 'registration_url'
            """))

            count = result.scalar()

            if count == 0:
                # Add the column
                db.session.execute(text("""
                    ALTER TABLE events
                    ADD registration_url VARCHAR(500) NULL
                """))
                db.session.commit()
                print("✓ Successfully added registration_url column to events table!")
            else:
                print("✓ registration_url column already exists in events table")

        except Exception as e:
            print(f"✗ Error during migration: {e}")
            db.session.rollback()

if __name__ == '__main__':
    migrate()
