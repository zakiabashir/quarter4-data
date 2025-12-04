#!/usr/bin/env python3
"""
Simple database initialization for testing - Creates sample users without passwords
"""

import sys
from pathlib import Path
import uuid

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from src.database import DATABASE_URL, Base
from src.models.user import User

def create_sample_users():
    """Create sample users for testing"""
    engine = create_engine(DATABASE_URL)

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

    sample_users = [
        {
            "id": str(uuid.uuid4()),
            "email": "student@example.com",
            "name": "Student User",
            "role": "student",
        },
        {
            "id": str(uuid.uuid4()),
            "email": "instructor@example.com",
            "name": "Instructor User",
            "role": "instructor",
        },
        {
            "id": str(uuid.uuid4()),
            "email": "admin@example.com",
            "name": "Admin User",
            "role": "admin",
        },
    ]

    with engine.connect() as conn:
        for user_data in sample_users:
            # Check if user already exists
            result = conn.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {"email": user_data["email"]}
            ).fetchone()

            if not result:
                conn.execute(
                    text("""
                        INSERT INTO users (id, email, name, role, created_at)
                        VALUES (:id, :email, :name, :role, datetime('now'))
                    """),
                    user_data
                )
                print(f"Created user: {user_data['email']}")
            else:
                print(f"User already exists: {user_data['email']}")
        conn.commit()


def main():
    """Main initialization function"""
    print("Initializing AI Physical AI Textbook database...")

    try:
        create_sample_users()
        print("\nDatabase initialization completed successfully!")
        print("\nSample User Credentials:")
        print("  Student         -> student@example.com")
        print("  Instructor      -> instructor@example.com")
        print("  Admin           -> admin@example.com")
        print("\nNote: Password authentication not configured yet")
    except Exception as e:
        print(f"\nError during initialization: {e}")
        return 1

    return 0


if __name__ == "__main__":
    main()