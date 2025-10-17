Lakshya - Portfolio, Skill Building & AI Job Matching Platform

A modern web application built with Flask that helps high schoolers and adults build portfolios, discover events/courses, and find jobs using AI-powered matching.

## Features

### 📊 Dashboard & Analytics
- **Overview Stats**: Courses completed, events attended, portfolio projects, job applications
- **Goals Tracking**: Set and track dream colleges, companies, and personal goals
- **Achievements & Badges**: Earn badges and unlock milestones
- **Skill Progress**: Visualize your learning journey with progress charts
- **Activity Feed**: Track your recent activities and accomplishments
- **Personalized Recommendations**: Get course and event suggestions based on your interests

### 🎨 User Profiles & Portfolio
- Personal portfolio pages with customizable sections
- Add projects, skills, and achievements
- Public/Private profile toggle
- GitHub, LinkedIn, and social media integration
- Beautiful, responsive portfolio layouts

### 📚 Events & Courses (Skill Building Hub)
- Browse and search for workshops, courses, and events
- Filter by category, level, and type
- Enroll in events and bookmark for later
- Creator mode to host and manage your own events
- Real-time enrollment tracking

### 🤖 AI Job Finder
- **Passive Mode**: Browse AI-matched job listings based on your skills
- **Aggressive Mode**: TikTok/Reels-style endless scrolling job feed
- Real-time job market data integration
- Skill-based matching algorithm
- Save and apply to jobs directly

### 💬 Messaging System
- Direct messaging (one-to-one)
- Group chats and collaboration channels
- Real-time messaging with WebSockets (Flask-SocketIO)
- Public and private group options
- Typing indicators and read receipts

### 🎯 Dual Experience Modes
- **Kid Mode**: Simplified UI, colorful design, learning-focused
- **Adult Mode**: Professional UI, full-featured, networking-focused
- Easy toggle between modes

## Tech Stack

**Frontend:**
- Flask with Jinja2 templating
- Tailwind CSS for styling
- Alpine.js for interactive components
- htmx for dynamic content loading
- Font Awesome for icons

**Backend & Real-time:**
- Flask (Python web framework)
- Flask-Login (authentication)
- Flask-WTF (form handling)
- Flask-SocketIO (real-time messaging)
- Python requests (API integration)

**Architecture:**
- Modular Blueprint structure
- RESTful API integration
- WebSocket support for real-time features
- Responsive, mobile-first design

## Project Structure

```
Chirec/
├── app/
│   ├── __init__.py              # App factory and configuration
│   ├── models/                  # Data models
│   │   ├── user.py
│   │   └── __init__.py
│   ├── routes/                  # Blueprint routes
│   │   ├── auth.py             # Authentication routes
│   │   ├── dashboard.py        # Dashboard & analytics routes
│   │   ├── profile.py          # Portfolio/profile routes
│   │   ├── events.py           # Events & courses routes
│   │   ├── jobs.py             # Job finder routes
│   │   ├── messaging.py        # Messaging routes
│   │   └── main.py             # Main/homepage routes
│   ├── forms/                   # WTForms
│   │   ├── auth.py
│   │   ├── profile.py
│   │   ├── events.py
│   │   └── messaging.py
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html
│   │   ├── components/
│   │   │   ├── navigation.html
│   │   │   └── footer.html
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── profile/
│   │   ├── events/
│   │   ├── jobs/
│   │   ├── messaging/
│   │   └── main/
│   ├── static/                  # Static assets
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── img/
│   └── utils/                   # Utility modules
│       ├── api_client.py       # API integration client
│       └── __init__.py
├── app.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Chirec
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and set your configuration values
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
API_BASE_URL=http://localhost:5001/api
```

- `SECRET_KEY`: A secure random string for session management
- `API_BASE_URL`: Backend API endpoint URL (to be provided by backend team)

## Backend API Integration

This frontend application is designed to work with a backend API. The `APIClient` class in `app/utils/api_client.py` handles all API communications.

### Expected API Endpoints

**Authentication:**
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration

**Users & Profiles:**
- `GET /api/users/{id}` - Get user profile
- `PUT /api/users/{id}` - Update user profile
- `POST /api/users/{id}/projects` - Add project
- `GET /api/projects/{id}` - Get project details

**Dashboard:**
- `GET /api/users/{id}/dashboard` - Get dashboard data
- `GET /api/users/{id}/goals` - Get user goals
- `POST /api/users/{id}/goals` - Create new goal
- `PUT /api/goals/{id}` - Update goal
- `DELETE /api/goals/{id}` - Delete goal
- `GET /api/users/{id}/achievements` - Get achievements
- `GET /api/users/{id}/stats` - Get detailed statistics

**Events:**
- `GET /api/events` - List events
- `GET /api/events/{id}` - Event details
- `POST /api/events` - Create event
- `POST /api/events/{id}/enroll` - Enroll in event

**Jobs:**
- `GET /api/jobs` - List jobs
- `GET /api/jobs/feed` - Job feed for scroller
- `GET /api/jobs/{id}` - Job details
- `POST /api/jobs/{id}/save` - Save job

**Messaging:**
- `GET /api/users/{id}/conversations` - List conversations
- `GET /api/conversations/{id}/messages` - Get messages
- `POST /api/conversations/{id}/messages` - Send message

## Key Features Implementation

### Dashboard
- Located at `/dashboard`
- Comprehensive overview of user progress
- Goal tracking with progress bars
- Achievement badges (12+ different badges)
- Skill progress visualization
- Recent activity timeline
- Upcoming events and recommendations

### Job Scroller (TikTok-style)
- Located at `/jobs/scroller`
- Infinite scroll with lazy loading
- Full-screen card-based UI
- Swipe/scroll to navigate
- Real-time job matching scores

### Real-time Messaging
- WebSocket connection via Socket.IO
- Real-time message delivery
- Typing indicators
- Room-based group chats
- Persistent message history via API

### Portfolio Builder
- Drag-and-drop project cards (planned)
- Rich text editing for descriptions
- Image uploads for projects
- Public/private visibility toggle
- Share on social platforms

### Kid vs Adult Mode
- Toggle in user dropdown menu
- Different UI themes and layouts
- Simplified navigation for kid mode
- Full professional features in adult mode
- Persisted user preference

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python app.py
```

The application will run with:
- Debug mode enabled
- Auto-reload on code changes
- Detailed error pages
- Port 5000 by default

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Comment complex logic
- Keep routes thin, move logic to utility functions

## Deployment

### Production Considerations

1. **Set production environment variables**
   ```env
   FLASK_ENV=production
   SECRET_KEY=<secure-random-key>
   API_BASE_URL=<production-api-url>
   ```

2. **Use a production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
   ```

3. **Enable HTTPS** for secure communication

4. **Set up reverse proxy** (nginx/Apache)

5. **Configure CORS** for API communication

## API Integration Notes

- All API calls go through `APIClient` in `app/utils/api_client.py`
- Errors are handled gracefully with user-friendly messages
- Timeout set to 10 seconds for all requests
- Authentication tokens (if needed) should be passed in headers

## Future Enhancements

- [ ] Resume builder and PDF export
- [ ] Advanced search and filters
- [ ] Integration with external job boards (LinkedIn, Indeed)
- [ ] Video chat for networking
- [ ] Achievement badges and gamification
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced analytics dashboard
- [ ] Import portfolios from GitHub, Behance, etc.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Built with ❤️ for learners and job seekers**
