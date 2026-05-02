# Team Task Manager - Complete Setup & Run Guide

A production-ready full-stack web application for team task management with role-based access control.

## Technology Stack

### Backend
- **Framework:** Flask 2.3.2
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Authentication:** JWT (Flask-JWT-Extended)
- **Validation:** Marshmallow
- **Password Hashing:** bcrypt

### Frontend
- **HTML5**, **CSS3**, **Vanilla JavaScript**
- **Responsive Design** with Flexbox/Grid
- **Fetch API** for HTTP requests
- **localStorage** for JWT token management

### Database
- **PostgreSQL** with proper indexing
- **Relationships:** One-to-Many, Many-to-Many
- **Constraints:** Unique, Foreign Keys

## Project Structure

```
team-task-manager/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── config.py            # Configuration management
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── auth/                # Authentication module
│   │   │   ├── __init__.py
│   │   │   ├── routes.py        # Auth endpoints
│   │   │   └── schemas.py       # Input validation
│   │   ├── projects/            # Projects module
│   │   │   ├── __init__.py
│   │   │   ├── routes.py        # Project endpoints
│   │   │   └── schemas.py
│   │   ├── tasks/               # Tasks module
│   │   │   ├── __init__.py
│   │   │   ├── routes.py        # Task endpoints
│   │   │   └── schemas.py
│   │   └── dashboard/           # Dashboard module
│   │       ├── __init__.py
│   │       └── routes.py        # Dashboard endpoints
│   ├── run.py                   # Entry point
│   ├── seed_data.py             # Test data seeding
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment template
│   └── .gitignore               # Git ignore file
├── frontend/
│   ├── index.html               # Login page
│   ├── signup.html              # Registration page
│   ├── dashboard.html           # Dashboard page
│   ├── projects.html            # Projects page
│   ├── tasks.html               # My Tasks page
│   ├── css/
│   │   └── style.css            # Main stylesheet
│   └── js/
│       ├── api.js               # API helper functions
│       ├── auth.js              # Auth helper functions
│       ├── dashboard.js         # Dashboard logic
│       ├── projects.js          # Projects logic
│       └── tasks.js             # Tasks logic
├── DATABASE_SETUP.md            # Database setup guide
├── API_DOCUMENTATION.md         # API reference
└── README.md                    # This file
```

---

## Prerequisites

### System Requirements
- **Python 3.8+**
- **PostgreSQL 12+**
- **Node.js** (optional, for file serving)
- **Git**

### Install PostgreSQL

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

**Windows:**
Download from [postgresql.org](https://www.postgresql.org/download/windows/) and run installer

---

## Backend Setup

### Step 1: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL connection details:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/team_task_manager
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DEBUG=True
```

### Step 3: Create PostgreSQL Database

Follow the [DATABASE_SETUP.md](DATABASE_SETUP.md) guide to:
1. Create database user
2. Create database
3. Test connection

### Step 4: Seed Test Data (Optional)

```bash
python seed_data.py
```

This creates:
- 1 Admin user (admin@example.com / admin123)
- 3 Member users (john@example.com / member123, etc.)
- 3 Sample projects
- 9 Sample tasks with various statuses

### Step 5: Run Backend Server

```bash
python run.py
```

Backend will run at: `http://localhost:5000`

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

---

## Frontend Setup

### Option 1: Simple HTTP Server (Recommended for Development)

**Python 3:**
```bash
cd frontend
python -m http.server 8000
```

**Then visit:** `http://localhost:8000`

### Option 2: Node.js HTTP Server

```bash
npm install -g http-server
cd frontend
http-server
```

### Option 3: Live Server Extension

If using VS Code, install "Live Server" extension and right-click on `index.html` → "Open with Live Server"

---

## Running the Application

### Terminal 1: Start Backend
```bash
cd backend
python run.py
```

### Terminal 2: Start Frontend
```bash
cd frontend
python -m http.server 8000
```

### Access Application
Open browser: `http://localhost:8000`

---

## Login Credentials

### Admin Account
- **Email:** admin@example.com
- **Password:** admin123

### Member Account (for testing)
- **Email:** john@example.com
- **Password:** member123

### Other Member Accounts
- jane@example.com / member123
- bob@example.com / member123

---

## API Endpoints Reference

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference.

### Quick Examples

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

**Get Projects:**
```bash
curl -X GET http://localhost:5000/api/projects \
  -H "Authorization: Bearer <your_token>"
```

---

## Features

### User Management
- ✅ Sign up with email validation
- ✅ Secure login with JWT tokens
- ✅ Password hashing with bcrypt
- ✅ Token expiration (1 hour)
- ✅ Protected routes

### Role-Based Access Control
- ✅ Admin: Full access to all resources
- ✅ Member: Limited access based on project assignment

### Project Management
- ✅ Create projects (Admin only)
- ✅ Update project details (Admin only)
- ✅ Delete projects (Admin only)
- ✅ Add/remove team members (Admin only)
- ✅ View assigned projects (Members)

### Task Management
- ✅ Create tasks within projects
- ✅ Assign tasks to team members
- ✅ Update task status (Todo, In Progress, Done)
- ✅ Set due dates
- ✅ Members can update only their assigned tasks

### Dashboard
- ✅ View task statistics
- ✅ Filter tasks by project and status
- ✅ View project summary with progress
- ✅ Track overdue tasks
- ✅ Monitor completed vs pending tasks

### UI/UX
- ✅ Responsive design (Mobile, Tablet, Desktop)
- ✅ Clean, modern interface
- ✅ Intuitive navigation
- ✅ Status badges and visual indicators
- ✅ Modal dialogs for forms

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'member',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Projects Table
```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    created_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### ProjectMembers Table (Many-to-Many)
```sql
CREATE TABLE project_members (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, user_id)
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'todo',
    due_date TIMESTAMP,
    project_id INTEGER NOT NULL REFERENCES projects(id),
    assigned_to INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Common Issues & Troubleshooting

### PostgreSQL Connection Error
```bash
# Check if PostgreSQL is running
pg_isready -h localhost

# View PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql.log
```

### Token Expired
- Frontend automatically handles 401 responses
- User is redirected to login page
- Clear localStorage: `localStorage.clear()`

### CORS Errors
- Backend includes CORS configuration
- Frontend requests from `http://localhost:8000`
- Backend runs on `http://localhost:5000`
- Both are enabled in CORS settings

### Port Already in Use
```bash
# Change backend port in run.py
app.run(port=5001)

# Change frontend port
python -m http.server 8001
```

---

## Development Workflow

### Adding New Features

1. **Create API endpoint** in backend (e.g., `/app/features/routes.py`)
2. **Add validation** in `schemas.py`
3. **Create frontend page** (e.g., `features.html`)
4. **Add JavaScript logic** in `js/features.js`
5. **Test API** with curl or Postman
6. **Test UI** in browser

### Testing

```bash
# Backend: Add to app/__init__.py
TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Run tests
python -m pytest
```

---

## Deployment Guide

### Environment Variables for Production

```env
FLASK_ENV=production
DEBUG=False
DATABASE_URL=postgresql://user:pass@prod-db:5432/db
SECRET_KEY=<strong-random-key>
JWT_SECRET_KEY=<strong-random-key>
```

### Deploy to Heroku

```bash
# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c 'import os; print(os.urandom(32))')

# Deploy
git push heroku main
```

### Deploy to AWS/DigitalOcean

See deployment documentation for:
- Gunicorn/WSGI server setup
- Nginx reverse proxy configuration
- SSL certificate setup
- Database backup strategy

---

## Performance Optimization

### Backend
- ✅ Database query optimization with indexes
- ✅ Connection pooling for database
- ✅ CORS configuration for static assets
- ✅ Gzip compression support

### Frontend
- ✅ CSS minification
- ✅ JavaScript bundling (optional)
- ✅ Image optimization
- ✅ Caching strategies

---

## Security Considerations

### Implemented
- ✅ Password hashing with bcrypt (10 rounds)
- ✅ JWT token-based authentication
- ✅ CORS protection
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Role-based access control
- ✅ Input validation with Marshmallow

### Additional Recommendations
- Enable HTTPS in production
- Use environment variables for secrets
- Implement rate limiting
- Add request logging
- Regular security audits
- Keep dependencies updated

---

## File Structure Summary

```
team-task-manager/
├── backend/                    # Flask backend
│   ├── app/models.py          # Database models
│   ├── run.py                 # Start server
│   ├── seed_data.py           # Test data
│   └── requirements.txt       # Dependencies
│
├── frontend/                   # Web UI
│   ├── index.html             # Login page
│   ├── dashboard.html         # Dashboard
│   ├── projects.html          # Projects
│   ├── tasks.html             # My Tasks
│   ├── css/style.css          # Styling
│   └── js/                    # JavaScript logic
│
├── DATABASE_SETUP.md          # Database guide
├── API_DOCUMENTATION.md       # API reference
└── README.md                  # This file
```

---

## Support & Documentation

- **Backend Framework:** [Flask Documentation](https://flask.palletsprojects.com/)
- **Database ORM:** [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- **Authentication:** [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- **Database:** [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## License

This project is provided as-is for educational purposes.

---

## Next Steps

1. ✅ Clone/extract the project
2. ✅ Set up PostgreSQL database
3. ✅ Install backend dependencies
4. ✅ Configure `.env` file
5. ✅ Run seed_data.py (optional)
6. ✅ Start backend and frontend servers
7. ✅ Login with test credentials
8. ✅ Explore features and customize as needed

**Happy Task Managing! 🚀**
