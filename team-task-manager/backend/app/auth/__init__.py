"""Auth Blueprint Initialization"""
from flask import Blueprint

def init_auth_blueprint(app):
    """Initialize authentication blueprint"""
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)
