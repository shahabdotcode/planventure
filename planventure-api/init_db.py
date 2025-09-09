"""
Database initialization script.
Run this script to create or recreate all the database tables.
"""
from models import db
from app import app
from models.user import User
from models.trip import Trip

def init_db():
    """Initialize the database by dropping and recreating all tables."""
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables with the updated schema
        db.create_all()
        
        print("Database tables have been recreated!")

if __name__ == "__main__":
    init_db()