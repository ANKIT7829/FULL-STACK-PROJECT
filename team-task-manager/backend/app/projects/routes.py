"""
Projects Routes
Handles project CRUD operations and team member management
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Project, ProjectMember, User, Task
from app.projects.schemas import ProjectSchema, ProjectUpdateSchema
from marshmallow import ValidationError
from functools import wraps

# Create Blueprint for projects routes
projects_bp = Blueprint('projects', __name__, url_prefix='/api/projects')


def admin_required(fn):
    """Decorator to check if user is admin"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper


@projects_bp.route('', methods=['POST'])
@admin_required
def create_project():
    """
    Create a new project (Admin only)
    Expects: { "title": "Project Name", "description": "Description" }
    Returns: Created project object
    """
    try:
        current_user_id = get_jwt_identity()
        schema = ProjectSchema()
        data = schema.load(request.get_json())
        
        project = Project(
            title=data['title'],
            description=data.get('description', ''),
            created_by=current_user_id
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'message': 'Project created successfully',
            'project': project.to_dict()
        }), 201
        
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@projects_bp.route('', methods=['GET'])
@jwt_required()
def get_projects():
    """
    Get all projects for current user
    Returns: List of projects (admin sees all, members see assigned projects)
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if user.role == 'admin':
            # Admin can see all projects
            projects = Project.query.all()
        else:
            # Members see only projects they're assigned to
            projects = db.session.query(Project).join(
                ProjectMember, Project.id == ProjectMember.project_id
            ).filter(ProjectMember.user_id == current_user_id).all()
        
        return jsonify({
            'projects': [project.to_dict(include_members=True) for project in projects]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@projects_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    """
    Get a specific project by ID
    Returns: Project object with members and tasks
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        project = Project.query.get(project_id)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Check access: admin or project member
        if user.role != 'admin':
            is_member = ProjectMember.query.filter_by(
                project_id=project_id,
                user_id=current_user_id
            ).first()
            
            if not is_member:
                return jsonify({'error': 'Unauthorized'}), 403
        
        project_data = project.to_dict(include_members=True)
        project_data['tasks'] = [task.to_dict() for task in project.tasks]
        
        return jsonify(project_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@projects_bp.route('/<int:project_id>', methods=['PUT'])
@admin_required
def update_project(project_id):
    """
    Update a project (Admin only)
    Expects: { "title": "New Title", "description": "New Description" }
    Returns: Updated project object
    """
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        schema = ProjectUpdateSchema()
        data = schema.load(request.get_json())
        
        if 'title' in data:
            project.title = data['title']
        if 'description' in data:
            project.description = data['description']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Project updated successfully',
            'project': project.to_dict()
        }), 200
        
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@admin_required
def delete_project(project_id):
    """
    Delete a project (Admin only)
    Returns: Success message
    """
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({'message': 'Project deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@projects_bp.route('/<int:project_id>/members', methods=['POST'])
@admin_required
def add_project_member(project_id):
    """
    Add a team member to project (Admin only)
    Expects: { "user_id": 2 }
    Returns: Project member object
    """
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if already a member
        existing_member = ProjectMember.query.filter_by(
            project_id=project_id,
            user_id=user_id
        ).first()
        
        if existing_member:
            return jsonify({'error': 'User is already a member'}), 400
        
        member = ProjectMember(project_id=project_id, user_id=user_id)
        db.session.add(member)
        db.session.commit()
        
        return jsonify({
            'message': 'Member added successfully',
            'member': member.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@projects_bp.route('/<int:project_id>/members/<int:user_id>', methods=['DELETE'])
@admin_required
def remove_project_member(project_id, user_id):
    """
    Remove a team member from project (Admin only)
    Returns: Success message
    """
    try:
        member = ProjectMember.query.filter_by(
            project_id=project_id,
            user_id=user_id
        ).first()
        
        if not member:
            return jsonify({'error': 'Member not found'}), 404
        
        db.session.delete(member)
        db.session.commit()
        
        return jsonify({'message': 'Member removed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
