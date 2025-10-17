from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_required, current_user
from app.models.db_models import Job, Profile, User as DBUser
from app.database import db
import json
from functools import wraps
import re

bp = Blueprint('jobs', __name__, url_prefix='/jobs')


def strip_html(text):
    """Remove HTML tags from text"""
    if not text:
        return ''
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', ' ', text)
    # Replace multiple spaces with single space
    clean = re.sub(r'\s+', ' ', clean)
    # Strip leading/trailing whitespace
    return clean.strip()


def adult_only(f):
    """Decorator to restrict access to adult users only"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.user_type != 'adult':
            flash('Jobs are only available for adult users.', 'warning')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
@bp.route('/browse')
@adult_only
def browse():
    """Browse jobs (passive mode)"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    location = request.args.get('location', '')
    search = request.args.get('search', '')  # General search term

    # Build query (no 'active' field in database)
    query = Job.query

    # Location filter
    if location:
        # Case-insensitive search for location
        query = query.filter(Job.location.ilike(f'%{location}%'))

    # General search (searches title, company, description, skills)
    if search:
        # Expand common tech abbreviations for better matching
        search_lower = search.lower()

        # Map common abbreviations to full terms
        expansions = {
            'ai': ['artificial intelligence', 'ai/ml', 'ai engineer', 'ai scientist'],
            'ml': ['machine learning', 'ml engineer', 'ml scientist'],
            'nlp': ['natural language processing', 'nlp engineer'],
            'cv': ['computer vision'],
            'dl': ['deep learning'],
        }

        # Check if search matches an abbreviation and expand it
        if search_lower in expansions:
            search_terms = expansions[search_lower]
        else:
            search_terms = [search]

        # Build OR conditions - prioritize title and skills matches
        conditions = []
        for term in search_terms:
            conditions.extend([
                Job.title.ilike(f'%{term}%'),
                Job.companyName.ilike(f'%{term}%'),
                Job.tagsAndSkills.ilike(f'%{term}%'),
                Job.jobDescription.ilike(f'%{term}%'),
            ])

        search_filter = db.or_(*conditions)
        query = query.filter(search_filter)

    # Paginate results (order by jobId since there's no id or posted_at)
    per_page = 20
    jobs_pagination = query.order_by(Job.jobId.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    jobs = jobs_pagination.items
    total_pages = jobs_pagination.pages

    return render_template('jobs/browse.html',
                          jobs=jobs,
                          page=page,
                          total_pages=total_pages,
                          category=category,
                          location=location,
                          search=search)


@bp.route('/scroller')
@adult_only
def scroller():
    """Aggressive mode - TikTok-style job scroller"""
    return render_template('jobs/scroller.html')


@bp.route('/feed')
@adult_only
def feed():
    """API endpoint for job feed (used by scroller)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Get user's skills for matching
    db_user = DBUser.query.get(current_user.id)
    user_skills = []
    if db_user.profile and db_user.profile.skills:
        try:
            user_skills = json.loads(db_user.profile.skills)
        except:
            user_skills = []

    # Fetch jobs in random order for variety (no 'active' or 'posted_at' fields in database, no 'id' column!)
    # Use NEWID() for SQL Server random ordering
    from sqlalchemy import func
    jobs_pagination = Job.query.order_by(
        func.newid()  # SQL Server random function
    ).paginate(page=page, per_page=per_page, error_out=False)

    jobs_data = []
    for job in jobs_pagination.items:
        # Parse job skills (using new tagsAndSkills field)
        job_skills = []
        try:
            job_skills = json.loads(job.tagsAndSkills) if job.tagsAndSkills else []
        except:
            job_skills = []

        # Calculate match score
        match_score = 0
        if user_skills and job_skills:
            matching_skills = set(user_skills).intersection(set(job_skills))
            match_score = int((len(matching_skills) / len(job_skills)) * 100) if job_skills else 0

        jobs_data.append({
            'id': job.jobId,  # Using jobId as id since there's no id column
            'title': job.title,
            'jobId': job.jobId,
            'company': job.companyName,
            'companyId': job.companyId,
            'description': strip_html(job.jobDescription),  # Strip HTML tags
            'location': job.location,
            'experience': job.experience,
            'salary': job.salary,
            'minimumSalary': job.minimumSalary,
            'maximumSalary': job.maximumSalary,
            'minimumExperience': job.minimumExperience,
            'maximumExperience': job.maximumExperience,
            'currency': job.currency,
            'skills': job_skills,
            'ReviewsCount': job.ReviewsCount,
            'AggregateRating': job.AggregateRating,
            'match_score': match_score,
            'jobUploaded': job.jobUploaded
        })

    return jsonify({
        'jobs': jobs_data,
        'page': page,
        'total_pages': jobs_pagination.pages,
        'has_more': jobs_pagination.has_next
    })


@bp.route('/<int:job_id>')
def detail(job_id):
    """Job detail page"""
    job = Job.query.get_or_404(job_id)

    # Parse skills (using new tagsAndSkills field)
    skills = []
    try:
        skills = json.loads(job.tagsAndSkills) if job.tagsAndSkills else []
    except:
        skills = []

    return render_template('jobs/detail.html', job=job, skills=skills)


@bp.route('/<int:job_id>/apply')
@adult_only
def apply(job_id):
    """Find and redirect to external job application URL"""
    job = Job.query.get_or_404(job_id)

    # Check if we already have a cached application URL
    if job.application_url:
        return redirect(job.application_url)

    # Try to find the application URL
    application_url = find_job_application_url(job)

    if application_url:
        # Save the URL to the database for future use
        try:
            job.application_url = application_url
            db.session.commit()
        except Exception as e:
            # If saving fails, just log it and continue
            print(f"Failed to save application URL: {e}")
            db.session.rollback()

        # Redirect to the application page
        return redirect(application_url)
    else:
        flash('Could not find application URL for this job. Please search for it manually.', 'warning')
        return redirect(url_for('jobs.detail', job_id=job_id))


def find_job_application_url(job):
    """
    Find job application URL using web search or construct it
    Returns the application URL or None
    """
    import re
    from urllib.parse import quote_plus

    # Check if we have a company website or known job board pattern
    company_name = job.companyName
    job_title = job.title
    location = job.location or ''

    if not company_name or not job_title:
        return None

    # Clean up location - extract city/country
    location_clean = location.strip()

    # Detect location for job board URLs
    location_param = ''
    if location_clean:
        # Extract main location (before comma if multiple parts)
        location_parts = location_clean.split(',')
        main_location = location_parts[0].strip()
        location_param = quote_plus(main_location)

    # Build search query with location
    full_search_query = f"{job_title} {company_name}"
    if location_clean:
        full_search_query += f" {location_clean}"

    # Common job board patterns with location
    job_boards = {
        'linkedin': f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(job_title + ' ' + company_name)}&location={location_param}" if location_param else f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(job_title + ' ' + company_name)}",
        'indeed': f"https://www.indeed.com/jobs?q={quote_plus(job_title + ' ' + company_name)}&l={location_param}" if location_param else f"https://www.indeed.com/jobs?q={quote_plus(job_title + ' ' + company_name)}",
        'google': f"https://www.google.com/search?q={quote_plus(full_search_query + ' job application')}",
    }

    # Try to detect which job board this might be from based on company patterns
    company_lower = company_name.lower()

    # Check for major tech companies with direct career pages
    major_companies = {
        'google': 'https://careers.google.com/jobs/results/',
        'microsoft': 'https://careers.microsoft.com/professionals/us/en/search-results',
        'amazon': 'https://www.amazon.jobs/en/search',
        'meta': 'https://www.metacareers.com/jobs',
        'facebook': 'https://www.metacareers.com/jobs',
        'apple': 'https://jobs.apple.com/en-us/search',
        'netflix': 'https://jobs.netflix.com/search',
        'tesla': 'https://www.tesla.com/careers/search',
        'ibm': 'https://www.ibm.com/employment/',
        'oracle': 'https://careers.oracle.com/jobs/',
        'nvidia': 'https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite',
        'intel': 'https://jobs.intel.com/en/search-jobs',
        'salesforce': 'https://www.salesforce.com/company/careers/',
        'adobe': 'https://careers.adobe.com/us/en/search-results',
    }

    for company_key, career_url in major_companies.items():
        if company_key in company_lower:
            return career_url

    # Default to Google search (most comprehensive)
    # This allows users to find the exact job posting
    return job_boards['google']


@bp.route('/<int:job_id>/save', methods=['POST'])
@adult_only
def save(job_id):
    """Save/bookmark job"""
    # TODO: Implement saved jobs functionality (requires separate saved_jobs table)
    return jsonify({'success': True})


@bp.route('/saved')
@adult_only
def saved():
    """View saved jobs"""
    # TODO: Implement saved jobs functionality (requires separate saved_jobs table)
    jobs = []
    return render_template('jobs/saved.html', jobs=jobs)
