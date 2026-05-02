# Frontend Setup - Quick Reference

## Quickstart (1 minute)

### Start Development Server
```bash
cd frontend
python -m http.server 8000
```

Or using Node.js:
```bash
http-server
```

### Access Application
Open: http://localhost:8000

---

## File Structure
```
frontend/
├── index.html          # Login page
├── signup.html         # Registration
├── dashboard.html      # Main dashboard
├── projects.html       # Projects list
├── tasks.html          # My tasks
├── css/
│   └── style.css       # All styling
└── js/
    ├── api.js          # API calls
    ├── auth.js         # Auth helpers
    ├── dashboard.js    # Dashboard logic
    ├── projects.js     # Projects logic
    └── tasks.js        # Tasks logic
```

---

## Pages Overview

| Page | Route | Purpose |
|------|-------|---------|
| Login | /index.html | User authentication |
| Sign Up | /signup.html | New account creation |
| Dashboard | /dashboard.html | Overview & statistics |
| Projects | /projects.html | Project management |
| My Tasks | /tasks.html | Personal task list |

---

## API Configuration
Set API base URL in `js/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

---

## Features
- ✅ Responsive Design (Mobile/Tablet/Desktop)
- ✅ JWT Token Management
- ✅ Modal Forms
- ✅ Real-time Filtering
- ✅ Status Badges
- ✅ Progress Bars
