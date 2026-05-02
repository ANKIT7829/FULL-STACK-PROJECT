"""Projects Blueprint Initialization"""
from flask import Blueprint

def init_projects_blueprint(app):
    """Initialize projects blueprint"""
    from app.projects.routes import projects_bp
    app.register_blueprint(projects_bp)
