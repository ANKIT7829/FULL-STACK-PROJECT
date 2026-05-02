# COMPLETE SETUP & CONNECTION GUIDE
# How Backend and Frontend Connect

## ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (localhost:8000)                │
│                   HTML/CSS/Vanilla JavaScript               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • index.html (Login/Signup)                         │  │
│  │  • dashboard.html (Statistics & Overview)           │  │
│  │  • projects.html (Project Management)               │  │
│  │  • tasks.html (Task Management)                     │  │
│  │  • js/api.js (API Communication)                    │  │
│  │  • js/auth.js (Authentication & Authorization)      │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓ (HTTP/JSON)                      │
│                  Fetch API with JWT Token                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (localhost:5000)                 │
│                    Flask REST API                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Routes & Endpoints:                                 │  │
│  │  • /api/auth (signup, login, verify)               │  │
│  │  • /api/projects (CRUD operations)                 │  │
│  │  • /api/tasks (Task management)                    │  │
│  │  • /api/dashboard (Statistics)                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓ (SQL Queries)                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│            DATABASE (localhost:5432)                        │
│            PostgreSQL with SQLAlchemy ORM                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Tables:                                             │  │
│  │  • users (authentication & roles)                  │  │
│  │  • projects (team projects)                        │  │
│  │  • project_members (many-to-many relationship)     │  │
│  │  • tasks (project tasks)                           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## STEP-BY-STEP SETUP INSTRUCTIONS

### STEP 1: INSTALL & CONFIGURE DATABASE

**Time: 10 minutes**

#### Windows:
```batch
# Download PostgreSQL installer from: https://www.postgresql.org/download/windows/
# Run installer, remember the password you set

# Verify installation
psql --version

# Create database from command prompt
createdb team_task_manager
```

#### macOS:
```bash
# Install PostgreSQL
brew install postgresql
brew services start postgresql

# Create database
createdb team_task_manager
```

#### Linux (Ubuntu/Debian):
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start

# Create database
sudo -u postgres createdb team_task_manager
```

#### Verify Connection:
```bash
psql -h localhost -d team_task_manager
```

If connection works, you'll see:
```
psql (14.0)
team_task_manager=#
```

Type `\q` to exit.

---

### STEP 2: SETUP BACKEND

**Time: 5 minutes**

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Configure Database Connection:

```bash
# Copy environment template
cp .env.example .env
# On Windows: copy .env.example .env

# Edit .env file with your PostgreSQL credentials
# Linux/macOS: nano .env
# Windows: notepad .env
```

Edit `.env` and ensure:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/team_task_manager
FLASK_ENV=development
SECRET_KEY=generate-random-secret-key-here
JWT_SECRET_KEY=generate-random-jwt-key-here
DEBUG=True
```

#### Initialize Database:

```bash
# Create all tables
python init_db.py

# Add test data (optional)
python seed_data.py
```

Expected output from seed_data.py:
```
✅ Database seeding completed successfully!

Test Credentials:
──────────────────────────
Admin Account:
  Email: admin@example.com
  Password: admin123
──────────────────────────
Member Account:
  Email: john@example.com
  Password: member123
```

#### Start Backend Server:

```bash
python run.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000

    Press CTRL+C to quit
    * Restarting with reloader
```

✅ **Backend is now running at `http://localhost:5000`**

---

### STEP 3: SETUP FRONTEND

**Time: 2 minutes**

Open a **NEW terminal window** (keep backend running in first terminal):

```bash
# Navigate to frontend directory
cd frontend

# Start development server
python -m http.server 8000
```

Expected output:
```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

✅ **Frontend is now available at `http://localhost:8000`**

---

### STEP 4: ACCESS APPLICATION

Open browser and navigate to:
```
http://localhost:8000
```

You should see the **Login page**.

#### Test with Seed Data Credentials:
```
Email: admin@example.com
Password: admin123
```

---

## HOW THEY COMMUNICATE

### Request Flow Example: Login

```
1. USER ENTERS CREDENTIALS
   ↓
   ┌─────────────────────────────────────┐
   │ Frontend (index.html)               │
   │ Form submit listener triggers       │
   │ JavaScript login function           │
   └─────────────────────────────────────┘
   ↓
   
2. JAVASCRIPT MAKES API CALL
   ┌─────────────────────────────────────┐
   │ js/api.js - apiCall() function      │
   │                                     │
   │ fetch('http://localhost:5000/api/  │
   │   auth/login', {                    │
   │   method: 'POST',                   │
   │   headers: {                        │
   │     'Content-Type': 'application/json'  │
   │   },                                │
   │   body: JSON.stringify({            │
   │     email: 'admin@example.com',    │
   │     password: 'admin123'            │
   │   })                                │
   │ })                                  │
   └─────────────────────────────────────┘
   ↓
   
3. BACKEND RECEIVES REQUEST
   ┌─────────────────────────────────────┐
   │ Backend (app/auth/routes.py)        │
   │                                     │
   │ @auth_bp.route('/login', ...)      │
   │ def login():                        │
   │   # Validate input with Marshmallow│
   │   # Query database for user        │
   │   # Check password with bcrypt     │
   │   # Generate JWT token             │
   │   # Return token to frontend       │
   └─────────────────────────────────────┘
   ↓
   
4. DATABASE QUERY
   ┌─────────────────────────────────────┐
   │ PostgreSQL (app/models.py)          │
   │                                     │
   │ SELECT * FROM users                │
   │ WHERE email = 'admin@example.com'  │
   │                                     │
   │ Returns: User object with password │
   │ hash for verification               │
   └─────────────────────────────────────┘
   ↓
   
5. BACKEND RETURNS RESPONSE
   ┌─────────────────────────────────────┐
   │ JSON Response:                      │
   │                                     │
   │ {                                   │
   │   "message": "Login successful",   │
   │   "access_token": "eyJ0eXAi...",   │
   │   "user": {                         │
   │     "id": 1,                        │
   │     "name": "Admin User",           │
   │     "email": "admin@example.com",   │
   │     "role": "admin"                 │
   │   }                                 │
   │ }                                   │
   └─────────────────────────────────────┘
   ↓
   
6. FRONTEND PROCESSES RESPONSE
   ┌─────────────────────────────────────┐
   │ js/api.js receives response         │
   │ Stores token in localStorage:       │
   │                                     │
   │ localStorage.setItem('token',       │
   │   response.access_token)            │
   │                                     │
   │ localStorage.setItem('user',        │
   │   JSON.stringify(response.user))    │
   │                                     │
   │ Redirects to dashboard.html         │
   └─────────────────────────────────────┘
   ↓
   
7. AUTHENTICATED REQUESTS
   ┌─────────────────────────────────────┐
   │ All subsequent requests include     │
   │ JWT token in header:                │
   │                                     │
   │ Authorization: Bearer <token>       │
   │                                     │
   │ Backend verifies token              │
   │ Backend checks user permissions     │
   │ Backend executes request            │
   └─────────────────────────────────────┘
```

---

## FILE COMMUNICATION MAP

### Frontend → Backend Communication

```javascript
// js/api.js
async function apiCall(endpoint, method = 'GET', data = null) {
    // Gets token from localStorage
    const token = localStorage.getItem('token');
    
    // Makes HTTP request to backend
    const response = await fetch(`http://localhost:5000/api${endpoint}`, {
        method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(data)
    });
    
    return await response.json();
}
```

### Backend Endpoints Diagram

```
POST   /auth/signup          → Create account
POST   /auth/login           → Get JWT token
GET    /auth/me              → Get current user (Protected)
GET    /auth/verify          → Verify token (Protected)

GET    /projects             → List projects (Protected)
POST   /projects             → Create project (Admin only)
GET    /projects/<id>        → Get project details (Protected)
PUT    /projects/<id>        → Update project (Admin only)
DELETE /projects/<id>        → Delete project (Admin only)
POST   /projects/<id>/members → Add team member (Admin only)
DELETE /projects/<id>/members/<uid> → Remove member (Admin only)

GET    /tasks                → Get tasks (Protected)
POST   /tasks                → Create task (Protected)
GET    /tasks/<id>           → Get task (Protected)
PUT    /tasks/<id>           → Update task (Protected)
DELETE /tasks/<id>           → Delete task (Admin only)

GET    /dashboard/stats      → Get statistics (Protected)
GET    /dashboard/tasks      → Get dashboard tasks (Protected)
GET    /dashboard/my-tasks   → Get my tasks (Protected)
GET    /dashboard/projects-summary → Get projects summary (Protected)
```

---

## JWT TOKEN LIFECYCLE

```
1. LOGIN
   User enters credentials
   ↓
   Backend validates credentials
   ↓
   Backend creates JWT token: eyJ0eXAi...
   ↓
   Frontend stores in localStorage

2. AUTHENTICATED REQUEST
   Frontend reads token from localStorage
   ↓
   Frontend adds to Authorization header
   ↓
   Backend verifies token signature
   ↓
   Backend extracts user ID from token
   ↓
   Backend processes request with user context

3. TOKEN EXPIRATION (1 hour)
   Frontend detects 401 response
   ↓
   Frontend clears localStorage
   ↓
   Frontend redirects to login page

4. LOGOUT
   User clicks logout button
   ↓
   Frontend clears localStorage
   ↓
   Frontend redirects to login page
```

---

## ROLE-BASED ACCESS CONTROL FLOW

```
Request comes in
↓
Backend extracts token from header
↓
Backend decodes token to get user_id
↓
Backend queries database for user
↓
Backend checks user.role
↓
┌─────────────────────────┐
│ if user.role == 'admin' │
│   → Full access         │
│ else user.role == 'member'   │
│   → Limited access      │
└─────────────────────────┘
↓
Backend checks resource permissions
↓
Return response (data or 403 Forbidden)
```

---

## ENVIRONMENT VARIABLES EXPLAINED

### Backend (.env)
```env
# Database connection
DATABASE_URL=postgresql://postgres:password@localhost:5432/team_task_manager
    └─ Format: postgresql://username:password@host:port/database

# Flask configuration
FLASK_ENV=development  # development or production
SECRET_KEY=your-secret-key  # For session encryption
DEBUG=True  # Enable debug mode (false in production)

# JWT configuration
JWT_SECRET_KEY=your-jwt-secret  # For signing tokens
JWT_ACCESS_TOKEN_EXPIRES=3600   # Token expires in 1 hour
```

### Frontend (no .env needed)
```javascript
// js/api.js
const API_BASE_URL = 'http://localhost:5000/api';
    └─ Change this if backend runs on different port
```

---

## DATABASE INITIALIZATION FLOW

```
1. python init_db.py
   ↓
   Creates Flask app with app context
   ↓
   Calls db.create_all()
   ↓
   SQLAlchemy generates SQL CREATE TABLE statements
   ↓
   PostgreSQL creates tables based on models

2. python seed_data.py
   ↓
   Inserts test users:
     • admin@example.com (Admin role)
     • john@example.com (Member role)
     • jane@example.com (Member role)
     • bob@example.com (Member role)
   ↓
   Inserts test projects
   ↓
   Inserts project member relationships
   ↓
   Inserts test tasks
```

---

## CORS (Cross-Origin Resource Sharing)

Why we need it:
- Frontend runs on `http://localhost:8000`
- Backend runs on `http://localhost:5000`
- Browsers block cross-origin requests by default

Solution:
```python
# In backend app/__init__.py
CORS(app, resources={r"/api/*": {"origins": "*"}})

# This allows frontend to make requests to backend
# In production, specify allowed origins:
CORS(app, resources={r"/api/*": {
    "origins": ["https://yourdomain.com"]
}})
```

---

## TESTING THE CONNECTION

### Test 1: Backend is running
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{"status": "OK", "message": "API is running"}
```

### Test 2: Database connection
```bash
# Check if tables exist
psql -d team_task_manager -c "\dt"
```

Expected output:
```
        List of relations
 Schema | Name              | Type  | Owner
─────────────────────────────────────────
 public | project_members   | table | postgres
 public | projects          | table | postgres
 public | tasks             | table | postgres
 public | users             | table | postgres
```

### Test 3: Login API
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

Expected response (with actual token):
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "name": "Admin User",
    "email": "admin@example.com",
    "role": "admin"
  }
}
```

### Test 4: Frontend pages load
```
http://localhost:8000/index.html       # Login page
http://localhost:8000/signup.html      # Sign up page
http://localhost:8000/dashboard.html   # Dashboard (if logged in)
http://localhost:8000/projects.html    # Projects (if logged in)
http://localhost:8000/tasks.html       # My tasks (if logged in)
```

---

## TROUBLESHOOTING CONNECTION ISSUES

### Issue: "Cannot GET /api/projects" (404 error)
**Solution:** Backend is not running or using wrong URL
```bash
# Check backend is running on 5000
python run.py

# Check API is accessible
curl http://localhost:5000/api/health
```

### Issue: "TypeError: Failed to fetch"
**Solution:** CORS issue or backend not responding
```bash
# Check if backend is accessible
curl http://localhost:5000/api/health

# Check CORS in Flask app is enabled
# Should see in app/__init__.py: CORS(app)
```

### Issue: "Invalid email or password"
**Solution:** Wrong credentials or database not seeded
```bash
# Re-seed database with test data
python seed_data.py

# Use credentials from output
```

### Issue: "Authorization: Bearer is missing"
**Solution:** Token not stored in localStorage
```javascript
// Check in browser console
localStorage.getItem('token')  // Should return token string

// Check login is storing token
// In index.html, check apiCall result has 'access_token'
```

### Issue: "postgresql: command not found"
**Solution:** PostgreSQL not installed or not in PATH
```bash
# Windows: Add to PATH
C:\Program Files\PostgreSQL\14\bin

# macOS: Use brew
brew install postgresql

# Linux: Use apt
sudo apt-get install postgresql
```

---

## QUICK REFERENCE

### Terminal 1: Start Backend
```bash
cd backend
python run.py
# Runs on http://localhost:5000
```

### Terminal 2: Start Frontend
```bash
cd frontend
python -m http.server 8000
# Runs on http://localhost:8000
```

### Access Application
```
http://localhost:8000
```

### Admin Credentials
```
Email: admin@example.com
Password: admin123
```

### Create New User
```
Go to: http://localhost:8000/signup.html
Fill form and create account
```

---

## NEXT STEPS

1. ✅ Complete setup as per instructions above
2. ✅ Test login with admin credentials
3. ✅ Explore all features (projects, tasks, dashboard)
4. ✅ Create new projects (admin only)
5. ✅ Add team members to projects (admin only)
6. ✅ Create and manage tasks
7. ✅ Customize styling in css/style.css
8. ✅ Extend functionality by adding new endpoints
9. ✅ Deploy to production

---

## KEY CONCEPTS SUMMARY

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | HTML/CSS/JavaScript | User interface |
| Backend | Flask + Python | REST API |
| Database | PostgreSQL | Data storage |
| Auth | JWT | Secure authentication |
| Communication | JSON + HTTP | Data transfer |
| ORM | SQLAlchemy | Database abstraction |
| Validation | Marshmallow | Input validation |
| Hashing | bcrypt | Password security |
| CORS | Flask-CORS | Cross-origin requests |

---

**You now have a complete, production-ready Team Task Manager application!** 🎉
