from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.forms.events import EventCreateForm, EventEnrollForm
from app.models.db_models import Event, EventEnrollment, User as DBUser
from app.database import db
import json

bp = Blueprint('events', __name__, url_prefix='/events')


@bp.route('/')
def browse():
    """Browse all events/courses"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    level = request.args.get('level', '')
    event_type = request.args.get('type', '')

    # Build query
    query = Event.query

    if category:
        query = query.filter_by(category=category)
    if level:
        query = query.filter_by(level=level)
    if event_type:
        query = query.filter_by(event_type=event_type)

    # Paginate results
    per_page = 12
    events_pagination = query.order_by(Event.featured.desc(), Event.start_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    events = events_pagination.items
    total_pages = events_pagination.pages

    return render_template('events/browse.html',
                          events=events,
                          page=page,
                          total_pages=total_pages,
                          category=category,
                          level=level,
                          event_type=event_type)


@bp.route('/<int:event_id>')
def detail(event_id):
    """Event detail page"""
    event = Event.query.get_or_404(event_id)

    # Get enrollment count
    enrollment_count = EventEnrollment.query.filter_by(event_id=event_id, status='enrolled').count()

    # Check if current user is enrolled
    is_enrolled = False
    if current_user.is_authenticated:
        is_enrolled = EventEnrollment.query.filter_by(
            event_id=event_id,
            user_id=current_user.id,
            status='enrolled'
        ).first() is not None

    return render_template('events/detail.html', event=event, enrollment_count=enrollment_count, is_enrolled=is_enrolled)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new event/course"""
    form = EventCreateForm()

    if form.validate_on_submit():
        # Parse tags
        tags = [t.strip() for t in form.tags.data.split(',') if t.strip()] if form.tags.data else []

        # Create new event
        event = Event(
            creator_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            event_type=form.event_type.data,
            category=form.category.data,
            level=form.level.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            location_type=form.location_type.data,
            location=form.location.data,
            max_participants=form.max_participants.data,
            price=form.price.data if form.price.data is not None else 0,
            tags=json.dumps(tags),
            registration_url=form.registration_url.data if form.registration_url.data else None,
            featured=form.featured.data,
            age_appropriate_for_kids=form.age_appropriate_for_kids.data
        )

        db.session.add(event)
        db.session.commit()

        flash('Event created successfully!', 'success')
        return redirect(url_for('events.detail', event_id=event.id))

    return render_template('events/create.html', form=form)


@bp.route('/<int:event_id>/enroll', methods=['POST'])
@login_required
def enroll(event_id):
    """Enroll in event"""
    event = Event.query.get_or_404(event_id)

    # Check if already enrolled
    existing_enrollment = EventEnrollment.query.filter_by(
        event_id=event_id,
        user_id=current_user.id
    ).first()

    if existing_enrollment:
        if existing_enrollment.status == 'enrolled':
            return jsonify({'success': False, 'message': 'Already enrolled in this event'}), 400
        else:
            # Reactivate enrollment
            existing_enrollment.status = 'enrolled'
            db.session.commit()
            return jsonify({'success': True, 'message': 'Successfully enrolled!'})

    # Check if event is full
    if event.max_participants:
        current_enrollments = EventEnrollment.query.filter_by(
            event_id=event_id,
            status='enrolled'
        ).count()
        if current_enrollments >= event.max_participants:
            return jsonify({'success': False, 'message': 'Event is full'}), 400

    # Create new enrollment
    enrollment = EventEnrollment(
        user_id=current_user.id,
        event_id=event_id,
        status='enrolled'
    )

    db.session.add(enrollment)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Successfully enrolled!'})


@bp.route('/<int:event_id>/bookmark', methods=['POST'])
@login_required
def bookmark(event_id):
    """Bookmark event"""
    # TODO: Implement bookmark functionality (requires separate bookmark table)
    return jsonify({'success': True})


@bp.route('/my-events')
@login_required
def my_events():
    """User's enrolled events"""
    # Get user's enrollments
    enrollments = EventEnrollment.query.filter_by(
        user_id=current_user.id
    ).order_by(EventEnrollment.enrolled_at.desc()).all()

    # Get events from enrollments
    events = [enrollment.event for enrollment in enrollments]

    return render_template('events/my_events.html', events=events, enrollments=enrollments)
