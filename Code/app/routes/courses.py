from flask import Blueprint, render_template, request
from app.models.db_models import Course
from sqlalchemy import or_, and_, func

bp = Blueprint('courses', __name__, url_prefix='/courses')


@bp.route('/')
def browse():
    """Browse all courses"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    level = request.args.get('level', '')
    provider = request.args.get('provider', '')

    # Build query
    query = Course.query

    if search:
        # Search in course name, organization, and skills
        search_filter = or_(
            Course.course_name.ilike(f'%{search}%'),
            Course.organization.ilike(f'%{search}%'),
            Course.skills.ilike(f'%{search}%')
        )
        query = query.filter(search_filter)

    if level:
        query = query.filter_by(level=level)

    if provider:
        query = query.filter_by(provider=provider)

    # Paginate results - order by URL (primary key) for MSSQL compatibility
    per_page = 12
    # MSSQL requires ORDER BY when using OFFSET/LIMIT, so we order by the primary key
    courses_pagination = query.order_by(Course.url).paginate(
        page=page, per_page=per_page, error_out=False
    )

    courses = courses_pagination.items
    total_pages = courses_pagination.pages

    # Get unique providers for filter dropdown
    providers = Course.query.with_entities(Course.provider).distinct().filter(
        Course.provider.isnot(None)
    ).limit(20).all()
    providers = [p[0] for p in providers if p[0]]

    return render_template('courses/browse.html',
                          courses=courses,
                          page=page,
                          total_pages=total_pages,
                          search=search,
                          level=level,
                          provider=provider,
                          providers=providers)
