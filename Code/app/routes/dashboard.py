from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.db_models import (
    User as DBUser, Event, EventEnrollment, Goal, Achievement,
    Project, Activity, CollegeCollage
)
from app.database import db
from datetime import datetime, timedelta
from sqlalchemy import func
import json

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('/')
@login_required
def index():
    """Main dashboard page with overview stats"""
    db_user = DBUser.query.get(current_user.id)

    # Calculate stats
    completed_courses = EventEnrollment.query.filter_by(
        user_id=current_user.id,
        status='completed'
    ).count()

    in_progress_courses = EventEnrollment.query.filter_by(
        user_id=current_user.id,
        status='enrolled'
    ).count()

    portfolio_projects = Project.query.filter_by(
        user_id=current_user.id
    ).count()

    active_goals = Goal.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).count()

    # Get recent achievements
    recent_achievements = Achievement.query.filter_by(
        user_id=current_user.id
    ).order_by(Achievement.earned_at.desc()).limit(5).all()

    # Get active goals
    user_goals = Goal.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).order_by(Goal.created_at.desc()).limit(5).all()

    # Get recent activity
    recent_activity = Activity.query.filter_by(
        user_id=current_user.id
    ).order_by(Activity.created_at.desc()).limit(10).all()

    # Get upcoming events
    upcoming_events = Event.query.join(EventEnrollment).filter(
        EventEnrollment.user_id == current_user.id,
        EventEnrollment.status == 'enrolled',
        Event.start_date >= datetime.utcnow()
    ).order_by(Event.start_date.asc()).limit(5).all()

    dashboard_data = {
        'stats': {
            'courses_completed': completed_courses,
            'courses_in_progress': in_progress_courses,
            'events_attended': completed_courses,
            'upcoming_events': len(upcoming_events),
            'portfolio_projects': portfolio_projects,
            'job_applications': 0,  # TODO: Implement job applications tracking
            'profile_views': 0,  # TODO: Implement profile views tracking
            'connections': 0  # TODO: Implement connections tracking
        },
        'recent_achievements': recent_achievements,
        'active_goals': user_goals,
        'recent_activity': recent_activity,
        'upcoming_events': upcoming_events,
    }

    return render_template('dashboard/index.html', data=dashboard_data)


@bp.route('/goals')
@login_required
def goals():
    """Goals tracking page"""
    user_goals = Goal.query.filter_by(
        user_id=current_user.id
    ).order_by(Goal.status.asc(), Goal.created_at.desc()).all()

    return render_template('dashboard/goals.html', goals=user_goals)


@bp.route('/goals/add', methods=['POST'])
@login_required
def add_goal():
    """Add a new goal"""
    title = request.form.get('title')
    category = request.form.get('category')
    description = request.form.get('description')
    target_date = request.form.get('target_date')

    if not title or not category:
        return jsonify({'success': False, 'message': 'Title and category are required'}), 400

    # Create new goal
    goal = Goal(
        user_id=current_user.id,
        category=category,
        title=title,
        description=description,
        progress=0,
        status='active'
    )

    if target_date:
        try:
            goal.target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        except:
            pass

    db.session.add(goal)
    db.session.commit()

    return jsonify({
        'success': True,
        'goal': {
            'id': goal.id,
            'title': goal.title,
            'category': goal.category,
            'progress': goal.progress
        }
    })


@bp.route('/goals/<int:goal_id>/update', methods=['POST'])
@login_required
def update_goal(goal_id):
    """Update goal progress"""
    goal = Goal.query.get_or_404(goal_id)

    # Verify ownership
    if goal.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    progress = request.form.get('progress', type=int)
    status = request.form.get('status')
    notes = request.form.get('notes')

    if progress is not None:
        goal.progress = max(0, min(100, progress))

        # Auto-complete if progress reaches 100
        if goal.progress == 100 and goal.status == 'active':
            goal.status = 'completed'
            goal.completed_at = datetime.utcnow()

    if status:
        goal.status = status
        if status == 'completed' and not goal.completed_at:
            goal.completed_at = datetime.utcnow()

    db.session.commit()

    return jsonify({'success': True})


@bp.route('/goals/<int:goal_id>/delete', methods=['POST'])
@login_required
def delete_goal(goal_id):
    """Delete a goal"""
    goal = Goal.query.get_or_404(goal_id)

    # Verify ownership
    if goal.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    db.session.delete(goal)
    db.session.commit()

    return jsonify({'success': True})


@bp.route('/achievements')
@login_required
def achievements():
    """Achievements and badges page"""
    user_achievements = Achievement.query.filter_by(
        user_id=current_user.id
    ).order_by(Achievement.earned_at.desc()).all()

    # Define all possible badges
    all_badges = [
        {'type': 'first_course', 'title': 'First Course', 'icon': '🎓', 'description': 'Complete your first course'},
        {'type': 'bookworm', 'title': 'Bookworm', 'icon': '📚', 'description': 'Complete 10 courses'},
        {'type': 'portfolio_starter', 'title': 'Portfolio Starter', 'icon': '🎨', 'description': 'Add your first project'},
        {'type': 'networker', 'title': 'Networker', 'icon': '🤝', 'description': 'Connect with 10 people'},
        {'type': 'job_hunter', 'title': 'Job Hunter', 'icon': '💼', 'description': 'Apply to 5 jobs'},
        {'type': 'early_bird', 'title': 'Early Bird', 'icon': '🌅', 'description': 'Join within first month'},
        {'type': 'goal_setter', 'title': 'Goal Setter', 'icon': '🎯', 'description': 'Set 3 goals'},
        {'type': 'achiever', 'title': 'Achiever', 'icon': '⭐', 'description': 'Complete a goal'},
        {'type': 'social_butterfly', 'title': 'Social Butterfly', 'icon': '🦋', 'description': 'Send 50 messages'},
        {'type': 'event_creator', 'title': 'Event Creator', 'icon': '🎪', 'description': 'Create your first event'},
        {'type': 'consistent_learner', 'title': 'Consistent Learner', 'icon': '📈', 'description': '7-day learning streak'},
        {'type': 'profile_complete', 'title': 'Profile Complete', 'icon': '✨', 'description': 'Complete your profile'},
    ]

    # Mark which badges are earned
    earned_types = [a.badge_type for a in user_achievements]
    for badge in all_badges:
        badge['earned'] = badge['type'] in earned_types

    return render_template('dashboard/achievements.html',
                          achievements=user_achievements,
                          badges=all_badges)


@bp.route('/stats')
@login_required
def stats():
    """Detailed statistics page"""
    # Get comprehensive statistics
    stats_data = {
        'events': {
            'enrolled': EventEnrollment.query.filter_by(user_id=current_user.id, status='enrolled').count(),
            'completed': EventEnrollment.query.filter_by(user_id=current_user.id, status='completed').count(),
            'cancelled': EventEnrollment.query.filter_by(user_id=current_user.id, status='cancelled').count(),
        },
        'projects': {
            'total': Project.query.filter_by(user_id=current_user.id).count(),
            'featured': Project.query.filter_by(user_id=current_user.id, featured=True).count(),
        },
        'goals': {
            'active': Goal.query.filter_by(user_id=current_user.id, status='active').count(),
            'completed': Goal.query.filter_by(user_id=current_user.id, status='completed').count(),
            'abandoned': Goal.query.filter_by(user_id=current_user.id, status='abandoned').count(),
        },
        'achievements': {
            'total': Achievement.query.filter_by(user_id=current_user.id).count(),
        }
    }

    return render_template('dashboard/stats.html', stats=stats_data)


@bp.route('/activity')
@login_required
def activity():
    """Recent activity feed"""
    activities = Activity.query.filter_by(
        user_id=current_user.id
    ).order_by(Activity.created_at.desc()).limit(50).all()

    return render_template('dashboard/activity.html', activities=activities)


@bp.route('/collage')
@login_required
def collage():
    """Dream college collage for kids mode"""
    db_user = DBUser.query.get(current_user.id)

    # Get all college collages for the user
    collages = CollegeCollage.query.filter_by(
        user_id=current_user.id
    ).order_by(CollegeCollage.is_primary.desc(), CollegeCollage.display_order.asc()).all()

    # Parse JSON image arrays for each collage
    for collage in collages:
        try:
            collage.images_list = json.loads(collage.college_images) if collage.college_images else []
        except:
            collage.images_list = []

    return render_template('dashboard/collage.html', collages=collages, user=db_user)


@bp.route('/collage/add', methods=['POST'])
@login_required
def add_collage():
    """Add a new college to the collage"""
    college_name = request.form.get('college_name')
    college_logo_url = request.form.get('college_logo_url')
    motivation_text = request.form.get('motivation_text')
    why_this_college = request.form.get('why_this_college')
    target_year = request.form.get('target_year', type=int)

    # Handle multiple image URLs
    college_images = request.form.getlist('college_images[]')

    if not college_name:
        return jsonify({'success': False, 'message': 'College name is required'}), 400

    # Create new collage entry
    collage = CollegeCollage(
        user_id=current_user.id,
        college_name=college_name,
        college_logo_url=college_logo_url,
        college_images=json.dumps(college_images) if college_images else json.dumps([]),
        motivation_text=motivation_text,
        why_this_college=why_this_college,
        target_year=target_year,
        is_primary=False,
        display_order=CollegeCollage.query.filter_by(user_id=current_user.id).count()
    )

    db.session.add(collage)
    db.session.commit()

    return jsonify({
        'success': True,
        'collage': {
            'id': collage.id,
            'college_name': collage.college_name,
            'logo_url': collage.college_logo_url
        }
    })


@bp.route('/collage/<int:collage_id>/update', methods=['POST'])
@login_required
def update_collage(collage_id):
    """Update a collage entry"""
    collage = CollegeCollage.query.get_or_404(collage_id)

    # Verify ownership
    if collage.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    # Update fields if provided
    if 'college_name' in request.form:
        collage.college_name = request.form.get('college_name')
    if 'college_logo_url' in request.form:
        collage.college_logo_url = request.form.get('college_logo_url')
    if 'motivation_text' in request.form:
        collage.motivation_text = request.form.get('motivation_text')
    if 'why_this_college' in request.form:
        collage.why_this_college = request.form.get('why_this_college')
    if 'target_year' in request.form:
        collage.target_year = request.form.get('target_year', type=int)
    if 'is_primary' in request.form:
        # If setting as primary, unset other primary collages
        if request.form.get('is_primary') == 'true':
            CollegeCollage.query.filter_by(user_id=current_user.id, is_primary=True).update({'is_primary': False})
            collage.is_primary = True

    # Handle image updates
    if request.form.getlist('college_images[]'):
        college_images = request.form.getlist('college_images[]')
        collage.college_images = json.dumps(college_images)

    db.session.commit()

    return jsonify({'success': True})


@bp.route('/collage/<int:collage_id>/delete', methods=['POST'])
@login_required
def delete_collage(collage_id):
    """Delete a collage entry"""
    collage = CollegeCollage.query.get_or_404(collage_id)

    # Verify ownership
    if collage.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    db.session.delete(collage)
    db.session.commit()

    return jsonify({'success': True})
