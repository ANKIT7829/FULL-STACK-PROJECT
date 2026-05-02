"""
Dashboard Routes
Handles dashboard statistics and task analytics
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Task, Project, ProjectMember, User
from datetime import datetime

# Create Blueprint for dashboard routes
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """
    Get dashboard statistics for current user
    Returns: Total, completed, pending, and overdue tasks
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        project_id = request.args.get('project_id', type=int)
        
        # Build base query
        if project_id:
            # Get stats for specific project
            tasks_query = Task.query.filter_by(project_id=project_id)
            
            # Check access
            if user.role != 'admin':
                is_member = ProjectMember.query.filter_by(
                    project_id=project_id,
                    user_id=current_user_id
                ).first()
                if not is_member:
                    return jsonify({'error': 'Unauthorized'}), 403
        else:
            # Get stats for all accessible projects
            if user.role == 'admin':
                tasks_query = Task.query
            else:
                # Get all tasks from projects user is a member of
                project_ids = db.session.query(ProjectMember.project_id).filter(
                    ProjectMember.user_id == current_user_id
                ).all()
                project_ids = [p[0] for p in project_ids]
                
                if not project_ids:
                    return jsonify({
                        'total_tasks': 0,
                        'completed_tasks': 0,
                        'pending_tasks': 0,
                        'overdue_tasks': 0
                    }), 200
                
                tasks_query = Task.query.filter(Task.project_id.in_(project_ids))
        
        # Get all tasks
        all_tasks = tasks_query.all()
        
        # Calculate stats
        total_tasks = len(all_tasks)
        completed_tasks = len([t for t in all_tasks if t.status == 'done'])
        pending_tasks = len([t for t in all_tasks if t.status != 'done'])
        
        # Calculate overdue tasks (due_date < today and status != done)
        now = datetime.utcnow()
        overdue_tasks = len([
            t for t in all_tasks 
            if t.due_date and t.due_date < now and t.status != 'done'
        ])
        
        return jsonify({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'overdue_tasks': overdue_tasks
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dashboard_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_dashboard_tasks():
    """
    Get tasks for dashboard with filtering
    Query params: project_id (optional), status (optional), assigned_to (optional)
    Returns: List of tasks
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        project_id = request.args.get('project_id', type=int)
        status = request.args.get('status')
        assigned_to = request.args.get('assigned_to', type=int)
        
        # Build base query
        query = Task.query
        
        # Filter by project if specified
        if project_id:
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
            
            query = query.filter_by(project_id=project_id)
        else:
            # If no project specified, get tasks from accessible projects
            if user.role != 'admin':
                project_ids = db.session.query(ProjectMember.project_id).filter(
                    ProjectMember.user_id == current_user_id
                ).all()
                project_ids = [p[0] for p in project_ids]
                
                if not project_ids:
                    return jsonify({'tasks': []}), 200
                
                query = query.filter(Task.project_id.in_(project_ids))
        
        # Filter by status
        if status:
            query = query.filter_by(status=status)
        
        # Filter by assigned user
        if assigned_to:
            query = query.filter_by(assigned_to=assigned_to)
        
        tasks = query.all()
        
        return jsonify({
            'tasks': [task.to_dict() for task in tasks]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dashboard_bp.route('/my-tasks', methods=['GET'])
@jwt_required()
def get_my_tasks():
    """
    Get all tasks assigned to current user
    Query params: status (optional), project_id (optional)
    Returns: List of tasks assigned to current user
    """
    try:
        current_user_id = get_jwt_identity()
        
        status = request.args.get('status')
        project_id = request.args.get('project_id', type=int)
        
        query = Task.query.filter_by(assigned_to=current_user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        if project_id:
            query = query.filter_by(project_id=project_id)
        
        tasks = query.all()
        
        return jsonify({
            'tasks': [task.to_dict() for task in tasks]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dashboard_bp.route('/projects-summary', methods=['GET'])
@jwt_required()
def get_projects_summary():
    """
    Get summary of all accessible projects with task counts
    Returns: List of projects with task statistics
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        # Get accessible projects
        if user.role == 'admin':
            projects = Project.query.all()
        else:
            projects = db.session.query(Project).join(
                ProjectMember, Project.id == ProjectMember.project_id
            ).filter(ProjectMember.user_id == current_user_id).all()
        
        # Build summary for each project
        summary = []
        for project in projects:
            all_tasks = Task.query.filter_by(project_id=project.id).all()
            completed = len([t for t in all_tasks if t.status == 'done'])
            
            summary.append({
                'project': project.to_dict(),
                'total_tasks': len(all_tasks),
                'completed_tasks': completed,
                'pending_tasks': len(all_tasks) - completed
            })
        
        return jsonify({'projects': summary}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
