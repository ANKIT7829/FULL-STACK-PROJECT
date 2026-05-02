"""
Tasks Routes
Handles task CRUD operations
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Task, Project, ProjectMember, User
from app.tasks.schemas import TaskSchema, TaskUpdateSchema
from marshmallow import ValidationError
from datetime import datetime

# Create Blueprint for tasks routes
tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


@tasks_bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    """
    Create a new task in a project
    Expects: { "title": "Task", "description": "Desc", "project_id": 1, "assigned_to": 2, "due_date": "2024-12-31" }
    Returns: Created task object
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        schema = TaskSchema()
        data = schema.load(request.get_json())
        
        # Get project
        project = Project.query.get(data['project_id'])
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Check if user is admin or project member
        if user.role != 'admin':
            is_member = ProjectMember.query.filter_by(
                project_id=data['project_id'],
                user_id=current_user_id
            ).first()
            if not is_member:
                return jsonify({'error': 'Unauthorized to create tasks in this project'}), 403
        
        # Validate assigned_to user is project member
        if data.get('assigned_to'):
            assigned_user = User.query.get(data['assigned_to'])
            if not assigned_user:
                return jsonify({'error': 'Assigned user not found'}), 404
            
            # Check if assigned user is project member
            is_member = ProjectMember.query.filter_by(
                project_id=data['project_id'],
                user_id=data['assigned_to']
            ).first()
            if not is_member:
                return jsonify({'error': 'Assigned user is not a project member'}), 400
        
        # Create task
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            status='todo',
            project_id=data['project_id'],
            assigned_to=data.get('assigned_to'),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'message': 'Task created successfully',
            'task': task.to_dict()
        }), 201
        
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@tasks_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    """
    Get tasks filtered by project and status
    Query params: project_id (required), status (optional)
    Returns: List of tasks
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        project_id = request.args.get('project_id', type=int)
        status = request.args.get('status')
        
        if not project_id:
            return jsonify({'error': 'project_id is required'}), 400
        
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Check access
        if user.role != 'admin':
            is_member = ProjectMember.query.filter_by(
                project_id=project_id,
                user_id=current_user_id
            ).first()
            if not is_member:
                return jsonify({'error': 'Unauthorized'}), 403
        
        # Build query
        query = Task.query.filter_by(project_id=project_id)
        
        if status:
            query = query.filter_by(status=status)
        
        tasks = query.all()
        
        return jsonify({
            'tasks': [task.to_dict() for task in tasks]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """
    Get a specific task by ID
    Returns: Task object
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        # Check access
        if user.role != 'admin':
            is_member = ProjectMember.query.filter_by(
                project_id=task.project_id,
                user_id=current_user_id
            ).first()
            if not is_member:
                return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify(task.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """
    Update a task
    Members can only update their assigned tasks
    Expects: { "title": "New Title", "status": "in_progress", "due_date": "2024-12-31" }
    Returns: Updated task object
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        # Check permission: admin or assigned user
        if user.role != 'admin' and task.assigned_to != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        schema = TaskUpdateSchema()
        data = schema.load(request.get_json())
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        if 'due_date' in data:
            task.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
        if 'assigned_to' in data and user.role == 'admin':
            task.assigned_to = data['assigned_to']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Task updated successfully',
            'task': task.to_dict()
        }), 200
        
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """
    Delete a task (Admin only)
    Returns: Success message
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'message': 'Task deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
