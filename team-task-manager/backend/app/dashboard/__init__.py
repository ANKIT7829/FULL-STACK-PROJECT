"""Dashboard Blueprint Initialization"""
from flask import Blueprint

def init_dashboard_blueprint(app):
    """Initialize dashboard blueprint"""
    from app.dashboard.routes import dashboard_bp
    app.register_blueprint(dashboard_bp)
