#!/usr/bin/env python
"""
Setup college_collages table with legacy fields and add sample data
"""

import os
import sys
from dotenv import load_dotenv
import json

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.models.db_models import College
from app.database import db
from sqlalchemy import text

def setup_college_collages():
    """Add legacy fields to college_collages and insert sample data"""
    print("=" * 60)
    print("Setting up college_collages table")
    print("=" * 60)

    app = create_app('development')

    with app.app_context():
        try:
            # Check and add legacy fields if they don't exist
            print("\nChecking for legacy fields...")

            legacy_fields = {
                'user_id': 'INT',
                'college_logo_url': 'VARCHAR(500)',
                'college_images': 'VARCHAR(MAX)',
                'motivation_text': 'VARCHAR(MAX)',
                'why_this_college': 'VARCHAR(MAX)',
                'target_year': 'INT',
                'display_order': 'INT DEFAULT 0',
                'is_primary': 'BIT DEFAULT 0'
            }

            for field_name, field_type in legacy_fields.items():
                # Check if field exists
                result = db.session.execute(text(
                    f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'college_collages' AND COLUMN_NAME = '{field_name}'"
                ))
                exists = result.fetchone()[0]

                if not exists:
                    print(f"  Adding column: {field_name}")
                    db.session.execute(text(f"ALTER TABLE college_collages ADD {field_name} {field_type}"))
                else:
                    print(f"  ✓ Column exists: {field_name}")

            db.session.commit()

            # Drop old colleges table if it exists
            result = db.session.execute(text(
                "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'colleges'"
            ))
            if result.fetchone()[0]:
                print("\nDropping old colleges table...")
                db.session.execute(text("DROP TABLE colleges"))
                db.session.commit()
                print("✓ Dropped colleges table")

            # Check if there's already data
            existing_count = College.query.count()
            if existing_count > 0:
                print(f"\n✓ Database already has {existing_count} colleges")
                return True

            # Add sample data
            print("\nAdding sample colleges...")

            colleges_data = [
                {
                    'college_name': 'Indian Institute of Technology Delhi',
                    'stream': 'Engineering',
                    'state': 'Delhi',
                    'city': 'New Delhi',
                    'entrance_exams': 'JEE Main, JEE Advanced',
                    'eligibility_criteria': '12th pass with 75% in PCM. JEE Advanced rank required.',
                    'required_skills': 'Mathematics, Physics, Chemistry, Problem Solving',
                    'typical_exam_cutoffs': 'JEE Advanced: Rank under 500',
                    'fee_structure': 1000000,  # 10 lakhs total
                    'seat_intake': 1200,
                    'college_type': 'Government',
                    'tier_rank': 1,
                    'website_url': 'https://home.iitd.ac.in/',
                    'placement_average_salary': 18,
                    'located_in_campus': 'Yes',
                    'year_established': 1961,
                    'accreditation': 'NAAC A++',
                    'gender_ratio': '85:15 (M:F)'
                },
                {
                    'college_name': 'Indian Institute of Technology Bombay',
                    'stream': 'Engineering',
                    'state': 'Maharashtra',
                    'city': 'Mumbai',
                    'entrance_exams': 'JEE Main, JEE Advanced',
                    'eligibility_criteria': '12th pass with 75% in PCM. JEE Advanced rank required.',
                    'required_skills': 'Mathematics, Physics, Chemistry, Programming',
                    'typical_exam_cutoffs': 'JEE Advanced: Rank under 300',
                    'fee_structure': 920000,
                    'seat_intake': 1100,
                    'college_type': 'Government',
                    'tier_rank': 1,
                    'website_url': 'https://www.iitb.ac.in/',
                    'placement_average_salary': 20,
                    'located_in_campus': 'Yes',
                    'year_established': 1958,
                    'accreditation': 'NAAC A++',
                    'gender_ratio': '83:17 (M:F)'
                },
                {
                    'college_name': 'All India Institute of Medical Sciences',
                    'stream': 'Medical',
                    'state': 'Delhi',
                    'city': 'New Delhi',
                    'entrance_exams': 'NEET UG',
                    'eligibility_criteria': '12th pass with Physics, Chemistry, Biology. NEET UG rank required.',
                    'required_skills': 'Biology, Chemistry, Physics, Medical Knowledge',
                    'typical_exam_cutoffs': 'NEET UG: Rank under 100',
                    'fee_structure': 25000,
                    'seat_intake': 125,
                    'college_type': 'Government',
                    'tier_rank': 1,
                    'website_url': 'https://www.aiims.edu/',
                    'placement_average_salary': 15,
                    'located_in_campus': 'Yes',
                    'year_established': 1956,
                    'accreditation': 'NAAC A++',
                    'gender_ratio': '60:40 (M:F)'
                },
                {
                    'college_name': 'BITS Pilani',
                    'stream': 'Engineering',
                    'state': 'Rajasthan',
                    'city': 'Pilani',
                    'entrance_exams': 'BITSAT',
                    'eligibility_criteria': '12th pass with 75% in PCM. BITSAT score required.',
                    'required_skills': 'Mathematics, Physics, Chemistry, Logical Reasoning',
                    'typical_exam_cutoffs': 'BITSAT: Score 300+',
                    'fee_structure': 1800000,
                    'seat_intake': 800,
                    'college_type': 'Deemed',
                    'tier_rank': 1,
                    'website_url': 'https://www.bits-pilani.ac.in/',
                    'placement_average_salary': 16,
                    'located_in_campus': 'Yes',
                    'year_established': 1964,
                    'accreditation': 'NAAC A',
                    'gender_ratio': '80:20 (M:F)'
                },
                {
                    'college_name': 'NIT Trichy',
                    'stream': 'Engineering',
                    'state': 'Tamil Nadu',
                    'city': 'Tiruchirappalli',
                    'entrance_exams': 'JEE Main',
                    'eligibility_criteria': '12th pass with 75% in PCM. JEE Main rank required.',
                    'required_skills': 'Mathematics, Physics, Chemistry, Computer Science',
                    'typical_exam_cutoffs': 'JEE Main: 98 percentile',
                    'fee_structure': 600000,
                    'seat_intake': 900,
                    'college_type': 'Government',
                    'tier_rank': 1,
                    'website_url': 'https://www.nitt.edu/',
                    'placement_average_salary': 14,
                    'located_in_campus': 'Yes',
                    'year_established': 1964,
                    'accreditation': 'NAAC A++',
                    'gender_ratio': '78:22 (M:F)'
                }
            ]

            for college_data in colleges_data:
                college = College(**college_data)
                db.session.add(college)
                print(f"  ✓ Added: {college_data['college_name']}")

            db.session.commit()

            total = College.query.count()
            print(f"\n✓ Successfully added {len(colleges_data)} colleges")
            print(f"✓ Total colleges in database: {total}")

            return True

        except Exception as e:
            print(f"\n✗ Setup failed!")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = setup_college_collages()
    sys.exit(0 if success else 1)
