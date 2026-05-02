"""Tasks Blueprint Initialization"""
from flask import Blueprint

def init_tasks_blueprint(app):
    """Initialize tasks blueprint"""
    from app.tasks.routes import tasks_bp
    app.register_blueprint(tasks_bp)
