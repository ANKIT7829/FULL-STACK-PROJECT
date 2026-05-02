# PostgreSQL Database Setup Guide

## Prerequisites
- PostgreSQL 12+ installed and running
- psql command-line tool available

## Setup Steps

### 1. Create Database User (Optional)
If you want a dedicated database user:

```sql
-- Connect to PostgreSQL as superuser
sudo -u postgres psql

-- Create new user
CREATE USER task_manager WITH PASSWORD 'your_password';

-- Grant privileges
ALTER USER task_manager CREATEDB;
```

### 2. Create Database

```sql
-- Using default postgres user
createdb -U postgres team_task_manager

-- Or if using dedicated user
createdb -U task_manager team_task_manager
```

### 3. Configure Database Connection

Create a `.env` file in the backend directory:

```bash
cd backend
cp .env.example .env
```

Edit `.env` and update:

```
# Default PostgreSQL connection (user: postgres)
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/team_task_manager

# Or with dedicated user
DATABASE_URL=postgresql://task_manager:your_password@localhost:5432/team_task_manager

# Other settings
FLASK_ENV=development
SECRET_KEY=your-secret-key-generate-random-value
JWT_SECRET_KEY=your-jwt-secret-key-generate-random-value
DEBUG=True
```

### 4. Verify Connection

```bash
# Test connection with psql
psql -U postgres -h localhost -d team_task_manager

# Inside psql, verify connection:
\l                    # List databases
\du                   # List users
\dt                   # List tables
\q                    # Quit
```

### 5. Troubleshooting

#### PostgreSQL Connection Error
```bash
# Make sure PostgreSQL is running
sudo service postgresql status     # Linux
brew services list                  # macOS
net start PostgreSQL               # Windows
```

#### Permission Denied
```bash
# Change PostgreSQL password
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD 'new_password';
```

#### Port Already in Use
PostgreSQL default port is 5432. If in use:
```
DATABASE_URL=postgresql://postgres:password@localhost:5433/team_task_manager
```

---

## Database Tables

The application automatically creates these tables on first run:

### users
- id (primary key)
- name (string)
- email (unique string)
- password_hash (hashed password)
- role (admin/member)
- created_at (timestamp)
- updated_at (timestamp)

### projects
- id (primary key)
- title (string)
- description (text)
- created_by (foreign key to users)
- created_at (timestamp)
- updated_at (timestamp)

### project_members
- id (primary key)
- project_id (foreign key to projects)
- user_id (foreign key to users)
- added_at (timestamp)
- unique constraint: (project_id, user_id)

### tasks
- id (primary key)
- title (string)
- description (text)
- status (todo/in_progress/done)
- due_date (timestamp, nullable)
- project_id (foreign key to projects)
- assigned_to (foreign key to users, nullable)
- created_at (timestamp)
- updated_at (timestamp)

---

## Reset Database

To clear and recreate all tables:

```bash
# Using Python script (from backend directory)
python
```

```python
from app import create_app
from app.models import db

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
```

Or directly with psql:

```sql
DROP DATABASE team_task_manager;
CREATE DATABASE team_task_manager;
```

---

## Backup Database

```bash
# Backup
pg_dump -U postgres team_task_manager > backup.sql

# Restore
psql -U postgres team_task_manager < backup.sql
```

---

## Production Notes

For production deployment:

1. Use strong, random passwords
2. Enable SSL connections
3. Configure firewall rules
4. Use connection pooling (PgBouncer)
5. Enable backup schedules
6. Monitor database logs
7. Use managed database service (AWS RDS, Heroku, etc.)

Example production connection string:
```
DATABASE_URL=postgresql://user:password@db.example.com:5432/team_task_manager?sslmode=require
```
