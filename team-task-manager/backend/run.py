"""
Application Entry Point
Run this file to start the Flask development server
"""
from app import create_app

# Create Flask app
app = create_app()

if __name__ == '__main__':
    """
    Run development server
    Access the app at http://localhost:5000
    """
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
