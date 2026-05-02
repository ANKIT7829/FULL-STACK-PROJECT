# Backend Setup - Quick Reference

## Quickstart (5 minutes)

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Up Database
```bash
# Create PostgreSQL database
createdb team_task_manager

# Update .env
cp .env.example .env
# Edit .env with your database URL
```

### 3. Seed Test Data
```bash
python seed_data.py
```

### 4. Run Server
```bash
python run.py
```

Server runs at: http://localhost:5000

---

## Test Credentials
- **Admin:** admin@example.com / admin123
- **Member:** john@example.com / member123

---

## API Health Check
```bash
curl http://localhost:5000/api/health
```

---

## Database Schema

**Users:** id, name, email, password_hash, role (admin/member)
**Projects:** id, title, description, created_by
**ProjectMembers:** id, project_id, user_id (many-to-many)
**Tasks:** id, title, description, status, due_date, project_id, assigned_to

---

## Key Features
- ✅ JWT Authentication
- ✅ Role-Based Access Control (Admin/Member)
- ✅ Project Management (Admin only)
- ✅ Task Management
- ✅ Dashboard with Statistics
- ✅ Input Validation (Marshmallow)
- ✅ Error Handling
