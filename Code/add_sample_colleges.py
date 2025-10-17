#!/usr/bin/env python
"""
Add sample college data to the database
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

def add_sample_colleges():
    """Add sample college data"""
    print("=" * 60)
    print("Adding Sample College Data")
    print("=" * 60)

    app = create_app('development')

    with app.app_context():
        try:
            # Check if colleges already exist
            existing_count = College.query.count()
            if existing_count > 0:
                print(f"\n✓ Database already has {existing_count} colleges")
                return True

            print("\nAdding sample colleges...")

            # Sample colleges data
            colleges_data = [
                {
                    'college_name': 'Indian Institute of Technology Delhi',
                    'stream': 'Engineering',
                    'state': 'Delhi',
                    'city': 'New Delhi',
                    'entrance_exams': json.dumps(["JEE Main", "JEE Advanced"]),
                    'eligibility_criteria': '12th pass with 75% in PCM. JEE Advanced rank required.',
                    'required_skills': json.dumps(["Mathematics", "Physics", "Chemistry", "Problem Solving", "Analytical Thinking"]),
                    'typical_exam_cutoffs': json.dumps({"JEE Advanced": "Rank under 500", "JEE Main": "99 percentile"}),
                    'fee_structure': json.dumps({"Year 1": "₹2,50,000", "Year 2": "₹2,50,000", "Year 3": "₹2,50,000", "Year 4": "₹2,50,000", "Total": "₹10,00,000"}),
                    'seat_intake': 1200,
                    'college_type': 'Government',
                    'tier_rank': 'Tier 1',
                    'website_url': 'https://home.iitd.ac.in/',
                    'placement_average_salary': 18.5,
                    'located_in_campus': True,
                    'year_established': 1961,
                    'accreditation': 'NAAC A++',
                    'gender_ratio': '85:15 (M:F)'
                },
                {
                    'college_name': 'Indian Institute of Technology Bombay',
                    'stream': 'Engineering',
                    'state': 'Maharashtra',
                    'city': 'Mumbai',
                    'entrance_exams': json.dumps(["JEE Main", "JEE Advanced"]),
                    'eligibility_criteria': '12th pass with 75% in PCM. JEE Advanced rank required.',
                    'required_skills': json.dumps(["Mathematics", "Physics", "Chemistry", "Programming", "Critical Thinking"]),
                    'typical_exam_cutoffs': json.dumps({"JEE Advanced": "Rank under 300", "JEE Main": "99.5 percentile"}),
                    'fee_structure': json.dumps({"Year 1": "₹2,30,000", "Year 2": "₹2,30,000", "Year 3": "₹2,30,000", "Year 4": "₹2,30,000", "Total": "₹9,20,000"}),
                    'seat_intake': 1100,
                    'college_type': 'Government',
                    'tier_rank': 'Tier 1',
                    'website_url': 'https://www.iitb.ac.in/',
                    'placement_average_salary': 20.0,
                    'located_in_campus': True,
                    'year_established': 1958,
                    'accreditation': 'NAAC A++',
                    'gender_ratio': '83:17 (M:F)'
                },
                {
                    'college_name': 'All India Institute of Medical Sciences',
                    'stream': 'Medical',
                    'state': 'Delhi',
                    'city': 'New Delhi',
                    'entrance_exams': json.dumps(["NEET UG"]),
                    'eligibility_criteria': '12th pass with Physics, Chemistry, Biology. NEET UG rank required.',
                    'required_skills': json.dumps(["Biology", "Chemistry", "Physics", "Medical Knowledge", "Communication Skills"]),
                    'typical_exam_cutoffs': json.dumps({"NEET UG": "Rank under 100"}),
                    'fee_structure': json.dumps({"Year 1": "₹5,000", "Year 2": "₹5,000", "Year 3": "₹5,000", "Year 4": "₹5,000", "Year 5": "₹5,000", "Total": "₹25,000"}),
                    'seat_intake': 125,
                    'college_type': 'Government',
                    'tier_rank': 'Tier 1',
                    'website_url': 'https://www.aiims.edu/',
                    'placement_average_salary': 15.0,
                    'located_in_campus': True,
                    'year_established': 1956,
                    'accreditation': 'NAAC A++',
                    'gender_ratio': '60:40 (M:F)'
                },
                {
                    'college_name': 'Delhi University - St. Stephens College',
                    'stream': 'Arts & Science',
                    'state': 'Delhi',
                    'city': 'New Delhi',
                    'entrance_exams': json.dumps(["CUET", "College Interview"]),
                    'eligibility_criteria': '12th pass with 85%+ marks. CUET score and interview required.',
                    'required_skills': json.dumps(["Critical Thinking", "Communication", "Research", "Writing"]),
                    'typical_exam_cutoffs': json.dumps({"CUET": "95 percentile", "12th Marks": "95%"}),
                    'fee_structure': json.dumps({"Year 1": "₹45,000", "Year 2": "₹45,000", "Year 3": "₹45,000", "Total": "₹1,35,000"}),
                    'seat_intake': 450,
                    'college_type': 'Government',
                    'tier_rank': 'Tier 1',
                    'website_url': 'https://www.ststephens.edu/',
                    'placement_average_salary': 8.5,
                    'located_in_campus': True,
                    'year_established': 1881,
                    'accreditation': 'NAAC A++',
                    'gender_ratio': '55:45 (M:F)'
                },
                {
                    'college_name': 'Birla Institute of Technology and Science, Pilani',
                    'stream': 'Engineering',
                    'state': 'Rajasthan',
                    'city': 'Pilani',
                    'entrance_exams': json.dumps(["BITSAT"]),
                    'eligibility_criteria': '12th pass with 75% in PCM. BITSAT score required.',
                    'required_skills': json.dumps(["Mathematics", "Physics", "Chemistry", "Logical Reasoning"]),
                    'typical_exam_cutoffs': json.dumps({"BITSAT": "Score 300+"}),
                    'fee_structure': json.dumps({"Year 1": "₹4,50,000", "Year 2": "₹4,50,000", "Year 3": "₹4,50,000", "Year 4": "₹4,50,000", "Total": "₹18,00,000"}),
                    'seat_intake': 800,
                    'college_type': 'Deemed',
                    'tier_rank': 'Tier 1',
                    'website_url': 'https://www.bits-pilani.ac.in/',
                    'placement_average_salary': 16.5,
                    'located_in_campus': True,
                    'year_established': 1964,
                    'accreditation': 'NAAC A',
                    'gender_ratio': '80:20 (M:F)'
                },
                {
                    'college_name': 'National Institute of Technology Trichy',
                    'stream': 'Engineering',
                    'state': 'Tamil Nadu',
                    'city': 'Tiruchirappalli',
                    'entrance_exams': json.dumps(["JEE Main"]),
                    'eligibility_criteria': '12th pass with 75% in PCM. JEE Main rank required.',
                    'required_skills': json.dumps(["Mathematics", "Physics", "Chemistry", "Computer Science"]),
                    'typical_exam_cutoffs': json.dumps({"JEE Main": "98 percentile"}),
                    'fee_structure': json.dumps({"Year 1": "₹1,50,000", "Year 2": "₹1,50,000", "Year 3": "₹1,50,000", "Year 4": "₹1,50,000", "Total": "₹6,00,000"}),
                    'seat_intake': 900,
                    'college_type': 'Government',
                    'tier_rank': 'Tier 1',
                    'website_url': 'https://www.nitt.edu/',
                    'placement_average_salary': 14.0,
                    'located_in_campus': True,
                    'year_established': 1964,
                    'accreditation': 'NAAC A++',
                    'gender_ratio': '78:22 (M:F)'
                },
                {
                    'college_name': 'Manipal Institute of Technology',
                    'stream': 'Engineering',
                    'state': 'Karnataka',
                    'city': 'Manipal',
                    'entrance_exams': json.dumps(["MET", "JEE Main"]),
                    'eligibility_criteria': '12th pass with 60% in PCM. MET or JEE Main score required.',
                    'required_skills': json.dumps(["Mathematics", "Physics", "Chemistry", "Programming"]),
                    'typical_exam_cutoffs': json.dumps({"MET": "Rank under 5000", "JEE Main": "85 percentile"}),
                    'fee_structure': json.dumps({"Year 1": "₹3,50,000", "Year 2": "₹3,50,000", "Year 3": "₹3,50,000", "Year 4": "₹3,50,000", "Total": "₹14,00,000"}),
                    'seat_intake': 1500,
                    'college_type': 'Private',
                    'tier_rank': 'Tier 2',
                    'website_url': 'https://manipal.edu/mit.html',
                    'placement_average_salary': 8.0,
                    'located_in_campus': True,
                    'year_established': 1957,
                    'accreditation': 'NAAC A',
                    'gender_ratio': '75:25 (M:F)'
                },
                {
                    'college_name': 'Christ University',
                    'stream': 'Commerce & Management',
                    'state': 'Karnataka',
                    'city': 'Bangalore',
                    'entrance_exams': json.dumps(["CUET", "Christ Entrance Test"]),
                    'eligibility_criteria': '12th pass with 50%+ marks. Entrance test and interview required.',
                    'required_skills': json.dumps(["Business Acumen", "Communication", "Leadership", "Analytical Skills"]),
                    'typical_exam_cutoffs': json.dumps({"Christ Entrance Test": "70%", "12th Marks": "80%"}),
                    'fee_structure': json.dumps({"Year 1": "₹1,80,000", "Year 2": "₹1,80,000", "Year 3": "₹1,80,000", "Total": "₹5,40,000"}),
                    'seat_intake': 600,
                    'college_type': 'Deemed',
                    'tier_rank': 'Tier 2',
                    'website_url': 'https://christuniversity.in/',
                    'placement_average_salary': 6.5,
                    'located_in_campus': True,
                    'year_established': 1969,
                    'accreditation': 'NAAC A+',
                    'gender_ratio': '50:50 (M:F)'
                }
            ]

            # Add colleges to database
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
            print(f"\n✗ Failed to add colleges!")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = add_sample_colleges()
    sys.exit(0 if success else 1)
