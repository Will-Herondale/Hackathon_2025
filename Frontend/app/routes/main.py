from flask import Blueprint, render_template
from flask_login import current_user

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Homepage"""
    return render_template('main/index.html')


@bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')


@bp.route('/career-advisor')
def career_advisor():
    """AI Career Advisor chatbot"""
    return render_template('main/career_advisor.html')


@bp.route('/api/toggle-mode', methods=['POST'])
def toggle_mode():
    """Toggle between kid and adult mode"""
    if current_user.is_authenticated:
        from app.models.db_models import User as DBUser
        from app.database import db

        # Update user mode in database
        db_user = DBUser.query.get(current_user.id)
        new_mode = 'kid' if db_user.user_type == 'adult' else 'adult'
        db_user.user_type = new_mode
        db.session.commit()

        # Update current_user object
        current_user.user_type = new_mode

        return {'success': True, 'mode': new_mode}
    return {'error': 'Not authenticated'}, 401


@bp.route('/api/user-context')
def user_context():
    """Get user context (goals, skills, interests) for AI advisor"""
    if not current_user.is_authenticated:
        return {'error': 'Not authenticated'}, 401

    from app.models.db_models import User as DBUser, Goal
    from flask import jsonify
    import json

    db_user = DBUser.query.get(current_user.id)

    # Get active goals
    goals = Goal.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).order_by(Goal.created_at.desc()).all()

    goals_data = []
    for goal in goals:
        goals_data.append({
            'id': goal.id,
            'title': goal.title,
            'description': goal.description,
            'category': goal.category,
            'progress': goal.progress,
            'target_date': goal.target_date.isoformat() if goal.target_date else None
        })

    # Get profile data
    profile_data = db_user.profile_data
    skills = profile_data.get('skills', [])
    interests = profile_data.get('interests', [])

    return jsonify({
        'goals': goals_data,
        'profile': {
            'skills': skills,
            'interests': interests,
            'title': profile_data.get('title', ''),
            'bio': profile_data.get('bio', '')
        }
    })


@bp.route('/api/ai-chat', methods=['POST'])
def ai_chat():
    """Proxy endpoint for AI chat to avoid CORS issues"""
    from flask import request, jsonify
    import requests
    from urllib.parse import quote
    import json as json_module

    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        # Call the AI API from the backend
        api_url = f"https://gptapi-ghd5dghhdvbvaqg3.centralindia-01.azurewebsites.net/aimn?prompt={quote(prompt)}"

        print(f"Calling API: {api_url}")

        # Make the request with a timeout
        response = requests.get(api_url, timeout=30)

        print(f"API Status: {response.status_code}")
        print(f"API Response Text: {response.text[:500]}")  # First 500 chars

        # Try to parse response as JSON first
        try:
            json_response = response.json()
            print(f"Parsed JSON: {json_response}")

            # Check if there's an error in the JSON response
            if isinstance(json_response, dict):
                if 'error' in json_response:
                    # API returned an error message
                    error_msg = json_response.get('error', 'Unknown error')
                    details = json_response.get('details', '')
                    return jsonify({
                        'error': error_msg,
                        'details': details
                    }), 200  # Return 200 so frontend can display the error nicely

                # Check for common response keys
                if 'response' in json_response:
                    return jsonify({'response': json_response['response']})
                elif 'message' in json_response:
                    return jsonify({'response': json_response['message']})
                elif 'text' in json_response:
                    return jsonify({'response': json_response['text']})
                else:
                    # Return the whole JSON object as response
                    return jsonify({'response': json_module.dumps(json_response, indent=2)})
            else:
                # JSON is not a dict, return as-is
                return jsonify({'response': str(json_response)})

        except json_module.JSONDecodeError:
            # Not JSON, treat as plain text
            print("Response is plain text, not JSON")
            if response.status_code == 200:
                return jsonify({'response': response.text})
            else:
                return jsonify({
                    'error': f'API returned status {response.status_code}',
                    'details': response.text
                }), 200  # Return 200 so frontend displays error nicely

    except requests.exceptions.Timeout:
        return jsonify({'error': 'API request timed out. Please try again.'}), 200
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Could not connect to AI service. Please check your internet connection.'}), 200
    except Exception as e:
        print(f"Exception: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 200
