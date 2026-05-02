"""
Authentication Routes
Handles user signup, login, and token verification
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, User
from app.auth.schemas import UserRegistrationSchema, UserLoginSchema
from marshmallow import ValidationError

# Create Blueprint for auth routes
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    User signup endpoint
    Expects: { "name": "John", "email": "john@example.com", "password": "password123" }
    Returns: User object with success message
    """
    try:
        # Validate request data
        schema = UserRegistrationSchema()
        data = schema.load(request.get_json())
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user with default role 'member'
        user = User(
            name=data['name'],
            email=data['email'],
            role='member'
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    Expects: { "email": "john@example.com", "password": "password123" }
    Returns: JWT access token and user information
    """
    try:
        # Validate request data
        schema = UserLoginSchema()
        data = schema.load(request.get_json())
        
        # Find user by email
        user = User.query.filter_by(email=data['email']).first()
        
        # Check if user exists and password is correct
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create JWT token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current logged-in user information
    Requires: Valid JWT token
    Returns: Current user object
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """
    Verify JWT token validity
    Requires: Valid JWT token
    Returns: Success message with user id
    """
    try:
        current_user_id = get_jwt_identity()
        return jsonify({
            'message': 'Token is valid',
            'user_id': current_user_id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401
