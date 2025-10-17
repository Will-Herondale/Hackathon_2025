#!/usr/bin/env python
"""
Migrate data from colleges table to college_collages and drop colleges table
"""

import os
import sys
from dotenv import load_dotenv
import json

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.database import db
from sqlalchemy import text

def migrate_colleges():
    """Migrate colleges data to college_collages table"""
    print("=" * 60)
    print("Migrating Colleges Data")
    print("=" * 60)

    app = create_app('development')

    with app.app_context():
        try:
            # Check if colleges table exists
            result = db.session.execute(text(
                "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'colleges'"
            ))
            colleges_exists = result.fetchone()[0]

            if not colleges_exists:
                print("\n✓ colleges table doesn't exist, no migration needed")
                return True

            # Get data from colleges table
            print("\nFetching data from colleges table...")
            colleges_data = db.session.execute(text("SELECT * FROM colleges")).fetchall()

            if not colleges_data:
                print("  No data to migrate")
            else:
                print(f"  Found {len(colleges_data)} colleges to migrate")

                # Get column names
                columns = db.session.execute(text(
                    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'colleges' ORDER BY ORDINAL_POSITION"
                )).fetchall()
                col_names = [col[0] for col in columns]

                # Insert into college_collages
                for row in colleges_data:
                    college_dict = dict(zip(col_names, row))

                    # Convert data types to match college_collages schema
                    insert_data = {
                        'college_name': college_dict.get('college_name'),
                        'stream': college_dict.get('stream'),
                        'state': college_dict.get('state'),
                        'city': college_dict.get('city'),
                        'entrance_exams': college_dict.get('entrance_exams'),
                        'eligibility_criteria': college_dict.get('eligibility_criteria'),
                        'required_skills': college_dict.get('required_skills'),
                        'typical_exam_cutoffs': college_dict.get('typical_exam_cutoffs'),
                        'fee_structure': int(college_dict.get('placement_average_salary', 0)) if college_dict.get('placement_average_salary') else None,
                        'seat_intake': college_dict.get('seat_intake'),
                        'college_type': college_dict.get('college_type'),
                        'tier_rank': 1 if college_dict.get('tier_rank', '').startswith('Tier 1') else 2,
                        'website_url': college_dict.get('website_url'),
                        'placement_average_salary': int(college_dict.get('placement_average_salary', 0)) if college_dict.get('placement_average_salary') else None,
                        'located_in_campus': 'Yes' if college_dict.get('located_in_campus') else 'No',
                        'year_established': college_dict.get('year_established'),
                        'accreditation': college_dict.get('accreditation'),
                        'gender_ratio': college_dict.get('gender_ratio')
                    }

                    # Insert into college_collages
                    placeholders = ', '.join([f':{k}' for k in insert_data.keys()])
                    columns_str = ', '.join(insert_data.keys())

                    db.session.execute(
                        text(f"INSERT INTO college_collages ({columns_str}) VALUES ({placeholders})"),
                        insert_data
                    )
                    print(f"  ✓ Migrated: {insert_data['college_name']}")

                db.session.commit()
                print(f"\n✓ Successfully migrated {len(colleges_data)} colleges")

            # Drop colleges table
            print("\nDropping colleges table...")
            db.session.execute(text("DROP TABLE colleges"))
            db.session.commit()
            print("✓ Successfully dropped colleges table")

            # Verify migration
            result = db.session.execute(text("SELECT COUNT(*) FROM college_collages"))
            total_count = result.fetchone()[0]
            print(f"\n✓ Total colleges in college_collages: {total_count}")

            return True

        except Exception as e:
            print(f"\n✗ Migration failed!")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = migrate_colleges()
    sys.exit(0 if success else 1)
