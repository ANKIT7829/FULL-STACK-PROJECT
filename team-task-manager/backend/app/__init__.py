"""
Main Flask Application Factory
Initializes and configures the Flask app
"""
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import get_config
from app.models import db
from app.auth import init_auth_blueprint
from app.projects import init_projects_blueprint
from app.tasks import init_tasks_blueprint
from app.dashboard import init_dashboard_blueprint


def create_app():
    """
    Application factory function
    Creates and configures Flask app with all extensions
    """
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(get_config())
    
    # Enable CORS for frontend communication
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    init_auth_blueprint(app)
    init_projects_blueprint(app)
    init_tasks_blueprint(app)
    init_dashboard_blueprint(app)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({'status': 'OK', 'message': 'API is running'}), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return jsonify({'error': 'Internal server error'}), 500
    
    # JWT error handlers
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        """Customize JWT identity"""
        return user
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        """Add claims to JWT"""
        return {}
    
    # Create tables with app context
    with app.app_context():
        db.create_all()
    
    return app
