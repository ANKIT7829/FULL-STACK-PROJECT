"""
Flask-CORS Configuration
Add this to handle Cross-Origin requests properly
"""
from flask_cors import CORS

# In app/__init__.py, after creating the Flask app:
# CORS(app, resources={r"/api/*": {"origins": "*"}})

# The backend is already configured for CORS in app/__init__.py
