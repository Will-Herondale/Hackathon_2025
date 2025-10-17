from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.db_models import College
from app.database import db
import json

bp = Blueprint('colleges', __name__, url_prefix='/colleges')


@bp.route('/')
@bp.route('/browse')
def browse():
    """Browse colleges"""
    page = request.args.get('page', 1, type=int)
    stream = request.args.get('stream', '')
    state = request.args.get('state', '')
    city = request.args.get('city', '')
    college_type = request.args.get('college_type', '')
    search = request.args.get('search', '')

    # Build query
    query = College.query

    # Stream filter
    if stream:
        query = query.filter(College.stream.ilike(f'%{stream}%'))

    # State filter
    if state:
        query = query.filter(College.state.ilike(f'%{state}%'))

    # City filter
    if city:
        query = query.filter(College.city.ilike(f'%{city}%'))

    # College type filter
    if college_type:
        query = query.filter(College.college_type.ilike(f'%{college_type}%'))

    # General search (searches name, city, state)
    if search:
        search_filter = db.or_(
            College.college_name.ilike(f'%{search}%'),
            College.city.ilike(f'%{search}%'),
            College.state.ilike(f'%{search}%'),
            College.stream.ilike(f'%{search}%')
        )
        query = query.filter(search_filter)

    # Paginate results
    per_page = 20
    colleges_pagination = query.order_by(College.tier_rank, College.college_name).paginate(
        page=page, per_page=per_page, error_out=False
    )

    colleges = colleges_pagination.items
    total_pages = colleges_pagination.pages

    return render_template('colleges/browse.html',
                          colleges=colleges,
                          page=page,
                          total_pages=total_pages,
                          stream=stream,
                          state=state,
                          city=city,
                          college_type=college_type,
                          search=search)


@bp.route('/<int:college_id>')
def detail(college_id):
    """College detail page"""
    college = College.query.get_or_404(college_id)

    # Parse JSON fields
    entrance_exams = []
    required_skills = []
    typical_exam_cutoffs = {}
    fee_structure = {}

    try:
        entrance_exams = json.loads(college.entrance_exams) if college.entrance_exams else []
    except:
        entrance_exams = []

    try:
        required_skills = json.loads(college.required_skills) if college.required_skills else []
    except:
        required_skills = []

    try:
        typical_exam_cutoffs = json.loads(college.typical_exam_cutoffs) if college.typical_exam_cutoffs else {}
    except:
        typical_exam_cutoffs = {}

    try:
        fee_structure = json.loads(college.fee_structure) if college.fee_structure else {}
    except:
        fee_structure = {}

    return render_template('colleges/detail.html',
                          college=college,
                          entrance_exams=entrance_exams,
                          required_skills=required_skills,
                          typical_exam_cutoffs=typical_exam_cutoffs,
                          fee_structure=fee_structure)


@bp.route('/api/filters')
def api_filters():
    """Get filter options for colleges"""
    # Get unique values for filters
    streams = db.session.query(College.stream).distinct().filter(College.stream.isnot(None)).all()
    states = db.session.query(College.state).distinct().filter(College.state.isnot(None)).all()
    college_types = db.session.query(College.college_type).distinct().filter(College.college_type.isnot(None)).all()

    return jsonify({
        'streams': [s[0] for s in streams],
        'states': [s[0] for s in states],
        'college_types': [c[0] for c in college_types]
    })
