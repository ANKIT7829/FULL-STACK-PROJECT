"""
Seed Data for Team Task Manager
Run this script to populate the database with test data
Usage: python seed_data.py
"""
import sys
sys.path.insert(0, '.')

from app import create_app
from app.models import db, User, Project, ProjectMember, Task
from datetime import datetime, timedelta

# Create app context
app = create_app()

def seed_database():
    """Populate database with seed data"""
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create users
        print("Creating users...")
        admin_user = User(
            name="Admin User",
            email="admin@example.com",
            role="admin"
        )
        admin_user.set_password("admin123")
        
        member1 = User(
            name="John Doe",
            email="john@example.com",
            role="member"
        )
        member1.set_password("member123")
        
        member2 = User(
            name="Jane Smith",
            email="jane@example.com",
            role="member"
        )
        member2.set_password("member123")
        
        member3 = User(
            name="Bob Johnson",
            email="bob@example.com",
            role="member"
        )
        member3.set_password("member123")
        
        db.session.add_all([admin_user, member1, member2, member3])
        db.session.commit()
        print(f"✓ Created 4 users")
        
        # Create projects
        print("Creating projects...")
        project1 = Project(
            title="Website Redesign",
            description="Complete redesign of company website with modern UI/UX",
            created_by=admin_user.id
        )
        
        project2 = Project(
            title="Mobile App Development",
            description="Develop new iOS and Android app for customer engagement",
            created_by=admin_user.id
        )
        
        project3 = Project(
            title="Database Migration",
            description="Migrate legacy database to cloud-based solution",
            created_by=admin_user.id
        )
        
        db.session.add_all([project1, project2, project3])
        db.session.commit()
        print(f"✓ Created 3 projects")
        
        # Add project members
        print("Adding project members...")
        members_data = [
            (project1.id, member1.id),
            (project1.id, member2.id),
            (project2.id, member2.id),
            (project2.id, member3.id),
            (project3.id, member1.id),
            (project3.id, member3.id),
        ]
        
        for project_id, user_id in members_data:
            member = ProjectMember(project_id=project_id, user_id=user_id)
            db.session.add(member)
        db.session.commit()
        print(f"✓ Added team members to projects")
        
        # Create tasks
        print("Creating tasks...")
        now = datetime.utcnow()
        
        # Website Redesign tasks
        tasks = [
            Task(
                title="Design mockups",
                description="Create high-fidelity mockups for all pages",
                status="done",
                project_id=project1.id,
                assigned_to=member1.id,
                due_date=now - timedelta(days=5)
            ),
            Task(
                title="Frontend development",
                description="Implement responsive frontend using HTML/CSS/JS",
                status="in_progress",
                project_id=project1.id,
                assigned_to=member2.id,
                due_date=now + timedelta(days=10)
            ),
            Task(
                title="API integration",
                description="Integrate backend APIs with frontend",
                status="todo",
                project_id=project1.id,
                assigned_to=member1.id,
                due_date=now + timedelta(days=20)
            ),
            
            # Mobile App tasks
            Task(
                title="Requirements gathering",
                description="Collect all requirements from stakeholders",
                status="done",
                project_id=project2.id,
                assigned_to=member2.id,
                due_date=now - timedelta(days=10)
            ),
            Task(
                title="Architecture design",
                description="Design app architecture and database schema",
                status="in_progress",
                project_id=project2.id,
                assigned_to=member3.id,
                due_date=now + timedelta(days=5)
            ),
            Task(
                title="iOS development",
                description="Develop iOS app using Swift",
                status="todo",
                project_id=project2.id,
                assigned_to=member2.id,
                due_date=now + timedelta(days=30)
            ),
            
            # Database Migration tasks
            Task(
                title="Backup current database",
                description="Create complete backup before migration",
                status="done",
                project_id=project3.id,
                assigned_to=member1.id,
                due_date=now - timedelta(days=3)
            ),
            Task(
                title="Data mapping",
                description="Map old database schema to new schema",
                status="in_progress",
                project_id=project3.id,
                assigned_to=member3.id,
                due_date=now + timedelta(days=7)
            ),
            Task(
                title="Testing",
                description="Test data integrity after migration",
                status="todo",
                project_id=project3.id,
                assigned_to=member1.id,
                due_date=now + timedelta(days=14)
            ),
        ]
        
        for task in tasks:
            db.session.add(task)
        db.session.commit()
        print(f"✓ Created {len(tasks)} tasks")
        
        print("\n✅ Database seeding completed successfully!")
        print("\nTest Credentials:")
        print("─" * 40)
        print("Admin Account:")
        print("  Email: admin@example.com")
        print("  Password: admin123")
        print("─" * 40)
        print("Member Account:")
        print("  Email: john@example.com")
        print("  Password: member123")
        print("─" * 40)
        print("\nYou can now login with these credentials!")

if __name__ == '__main__':
    seed_database()
