from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.forms.profile import ProfileEditForm, ProjectForm
from app.models.db_models import User as DBUser, Profile, Project
from app.database import db
import json

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/<int:user_id>')
def view(user_id):
    """View user profile/portfolio"""
    # Fetch user from database
    user = DBUser.query.get(user_id)

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('main.index'))

    is_own_profile = current_user.is_authenticated and current_user.id == user_id

    # Check if profile is public or if it's the user's own profile
    if not user.profile_public and not is_own_profile:
        flash('This profile is private.', 'warning')
        return redirect(url_for('main.index'))

    # Get user's profile
    profile = user.profile

    # Get user's projects
    projects = Project.query.filter_by(user_id=user_id).order_by(Project.featured.desc(), Project.created_at.desc()).all()

    return render_template('profile/view.html', user=user, profile=profile, projects=projects, is_own_profile=is_own_profile)


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """Edit user profile"""
    # For now, redirect to profile view with a message
    # TODO: Create profile/edit.html template
    flash('Profile editing is currently under development. Please check back later.', 'info')
    return redirect(url_for('profile.view', user_id=current_user.id))


@bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
def add_project():
    """Add new project to portfolio"""
    # For now, redirect to profile view with a message
    # TODO: Create profile/add_project.html template
    flash('Project management is currently under development. Please check back later.', 'info')
    return redirect(url_for('profile.view', user_id=current_user.id))


@bp.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """Edit existing project"""
    project = Project.query.get_or_404(project_id)

    # Ensure user owns this project
    if project.user_id != current_user.id:
        flash('You do not have permission to edit this project.', 'danger')
        return redirect(url_for('main.index'))

    # For now, redirect to profile view with a message
    # TODO: Create profile/edit_project.html template
    flash('Project editing is currently under development. Please check back later.', 'info')
    return redirect(url_for('profile.view', user_id=current_user.id))


@bp.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    """Delete project"""
    project = Project.query.get_or_404(project_id)

    # Ensure user owns this project
    if project.user_id != current_user.id:
        flash('You do not have permission to delete this project.', 'danger')
        return redirect(url_for('main.index'))

    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully.', 'success')

    return redirect(url_for('profile.view', user_id=current_user.id))


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """User settings page"""
    # For now, redirect to dashboard with a message
    # TODO: Create profile/settings.html template
    flash('Settings page is currently under development. Please check back later.', 'info')
    return redirect(url_for('dashboard.index'))


@bp.route('/toggle-visibility', methods=['POST'])
@login_required
def toggle_visibility():
    """Toggle profile visibility (public/private)"""
    db_user = DBUser.query.get(current_user.id)
    db_user.profile_public = not db_user.profile_public
    db.session.commit()

    return jsonify({'success': True, 'public': db_user.profile_public})
