# Team Task Manager - API Documentation

## Overview
Complete REST API for the Team Task Manager application with JWT authentication, role-based access control, and full project/task management functionality.

---

## Base URL
```
http://localhost:5000/api
```

---

## Authentication

### JWT Token
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## Endpoints

### 1. Authentication

#### Signup
- **POST** `/auth/signup`
- **Request Body:**
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }
  ```
- **Response:** `201 Created`
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "role": "member",
      "created_at": "2024-01-01T12:00:00",
      "updated_at": "2024-01-01T12:00:00"
    }
  }
  ```

#### Login
- **POST** `/auth/login`
- **Request Body:**
  ```json
  {
    "email": "john@example.com",
    "password": "password123"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "message": "Login successful",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "role": "member",
      "created_at": "2024-01-01T12:00:00",
      "updated_at": "2024-01-01T12:00:00"
    }
  }
  ```

#### Get Current User
- **GET** `/auth/me` (Protected)
- **Response:** `200 OK` - User object

#### Verify Token
- **GET** `/auth/verify` (Protected)
- **Response:** `200 OK`
  ```json
  {
    "message": "Token is valid",
    "user_id": 1
  }
  ```

---

### 2. Projects (Admin: Full CRUD, Members: View Only)

#### Create Project (Admin Only)
- **POST** `/projects` (Protected, Admin)
- **Request Body:**
  ```json
  {
    "title": "Website Redesign",
    "description": "Complete redesign of company website"
  }
  ```
- **Response:** `201 Created`

#### Get All Projects
- **GET** `/projects` (Protected)
- **Response:** `200 OK`
  ```json
  {
    "projects": [
      {
        "id": 1,
        "title": "Website Redesign",
        "description": "...",
        "created_by": 1,
        "creator": { "id": 1, "name": "Admin User", ... },
        "members": [...],
        "created_at": "2024-01-01T12:00:00",
        "updated_at": "2024-01-01T12:00:00"
      }
    ]
  }
  ```

#### Get Project Details
- **GET** `/projects/<project_id>` (Protected)
- **Response:** `200 OK` - Project object with members and tasks

#### Update Project (Admin Only)
- **PUT** `/projects/<project_id>` (Protected, Admin)
- **Request Body:**
  ```json
  {
    "title": "New Title",
    "description": "New description"
  }
  ```
- **Response:** `200 OK`

#### Delete Project (Admin Only)
- **DELETE** `/projects/<project_id>` (Protected, Admin)
- **Response:** `200 OK`

#### Add Project Member (Admin Only)
- **POST** `/projects/<project_id>/members` (Protected, Admin)
- **Request Body:**
  ```json
  {
    "user_id": 2
  }
  ```
- **Response:** `201 Created`

#### Remove Project Member (Admin Only)
- **DELETE** `/projects/<project_id>/members/<user_id>` (Protected, Admin)
- **Response:** `200 OK`

---

### 3. Tasks

#### Create Task
- **POST** `/tasks` (Protected)
- **Request Body:**
  ```json
  {
    "title": "Design Homepage",
    "description": "Create homepage design",
    "project_id": 1,
    "assigned_to": 2,
    "due_date": "2024-12-31"
  }
  ```
- **Response:** `201 Created`

#### Get Tasks
- **GET** `/tasks?project_id=1&status=todo` (Protected)
- **Query Parameters:**
  - `project_id` (required)
  - `status` (optional): todo, in_progress, done
- **Response:** `200 OK`
  ```json
  {
    "tasks": [
      {
        "id": 1,
        "title": "Design Homepage",
        "description": "...",
        "status": "todo",
        "due_date": "2024-12-31T00:00:00",
        "project_id": 1,
        "assigned_to": 2,
        "assigned_user": { ... },
        "created_at": "2024-01-01T12:00:00",
        "updated_at": "2024-01-01T12:00:00"
      }
    ]
  }
  ```

#### Get Task Details
- **GET** `/tasks/<task_id>` (Protected)
- **Response:** `200 OK` - Task object

#### Update Task
- **PUT** `/tasks/<task_id>` (Protected)
- **Request Body:**
  ```json
  {
    "title": "New Title",
    "description": "Updated description",
    "status": "in_progress",
    "due_date": "2024-12-31"
  }
  ```
- **Permissions:**
  - Admin: Can update any task
  - Member: Can only update their assigned tasks
- **Response:** `200 OK`

#### Delete Task (Admin Only)
- **DELETE** `/tasks/<task_id>` (Protected, Admin)
- **Response:** `200 OK`

---

### 4. Dashboard

#### Get Dashboard Statistics
- **GET** `/dashboard/stats?project_id=1` (Protected)
- **Query Parameters:**
  - `project_id` (optional): Get stats for specific project or all if omitted
- **Response:** `200 OK`
  ```json
  {
    "total_tasks": 10,
    "completed_tasks": 3,
    "pending_tasks": 7,
    "overdue_tasks": 1
  }
  ```

#### Get Dashboard Tasks
- **GET** `/dashboard/tasks?project_id=1&status=todo` (Protected)
- **Query Parameters:**
  - `project_id` (optional)
  - `status` (optional): todo, in_progress, done
  - `assigned_to` (optional)
- **Response:** `200 OK` - List of tasks

#### Get My Tasks
- **GET** `/dashboard/my-tasks?status=todo` (Protected)
- **Query Parameters:**
  - `status` (optional)
  - `project_id` (optional)
- **Response:** `200 OK` - List of tasks assigned to current user

#### Get Projects Summary
- **GET** `/dashboard/projects-summary` (Protected)
- **Response:** `200 OK`
  ```json
  {
    "projects": [
      {
        "project": { ... },
        "total_tasks": 10,
        "completed_tasks": 3,
        "pending_tasks": 7
      }
    ]
  }
  ```

---

## Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Error Response Format

```json
{
  "error": "Error message describing what went wrong"
}
```

---

## Role-Based Access Control

### Admin Role
- Create, update, delete projects
- Add/remove project members
- Perform CRUD operations on any task
- View all projects and tasks

### Member Role
- View only projects they are assigned to
- View and create tasks in assigned projects
- Update only their assigned tasks
- Cannot delete tasks

---

## Authentication Flow

1. User signs up → Create account
2. User logs in → Receive JWT token
3. Store token in localStorage
4. Include token in Authorization header for all protected requests
5. Token expires after 1 hour (configurable)
6. User logs out → Remove token from storage

---

## Example Request

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'

# Get projects with token
curl -X GET http://localhost:5000/api/projects \
  -H "Authorization: Bearer <your_token>"
```
