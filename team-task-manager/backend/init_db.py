"""
Database Initialization Script
Run once to create all database tables
"""
import sys
sys.path.insert(0, '.')

from app import create_app
from app.models import db

def init_db():
    """Initialize database tables"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        print("\nYou can now run seed_data.py to add test data")

if __name__ == '__main__':
    init_db()
