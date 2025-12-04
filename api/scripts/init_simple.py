#!/usr/bin/env python3
"""
Simple database initialization for testing
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from src.database import DATABASE_URL, Base
from src.models.user import User
from src.core.security import get_password_hash


def create_sample_users():
    """Create sample users for testing"""
    engine = create_engine(DATABASE_URL)

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

    sample_users = [
        {
            "email": "student@example.com",
            "username": "student_user",
            "full_name": "Student User",
            "hashed_password": get_password_hash("password123"),
            "role": "student",
            "is_active": True,
        },
        {
            "email": "instructor@example.com",
            "username": "instructor_user",
            "full_name": "Instructor User",
            "hashed_password": get_password_hash("password123"),
            "role": "instructor",
            "is_active": True,
        },
        {
            "email": "admin@example.com",
            "username": "admin_user",
            "full_name": "Admin User",
            "hashed_password": get_password_hash("password123"),
            "role": "admin",
            "is_active": True,
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
                        INSERT INTO users (email, username, full_name, hashed_password, role, is_active, created_at)
                        VALUES (:email, :username, :full_name, :hashed_password, :role, :is_active, datetime('now'))
                    """),
                    user_data
                )
                print(f"✅ Created user: {user_data['email']}")
            else:
                print(f"ℹ️  User already exists: {user_data['email']}")
        conn.commit()


def main():
    """Main initialization function"""
    print("🚀 Initializing AI Physical AI Textbook database...")

    try:
        create_sample_users()
        print("\n✅ Database initialization completed successfully!")
        print("\n📋 Sample User Credentials:")
        print("  ┌─────────────────────┬────────────────┐")
        print("  │ Role            │ Email            │")
        print("  ├─────────────────────┼────────────────┤")
        print("  │ Student         │ student@example.com │")
        print("  │ Instructor      │ instructor@example.com │")
        print("  │ Admin           │ admin@example.com   │")
        print("  └─────────────────────┴────────────────┘")
        print("\n🔑 Password for all users: password123")
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        return 1

    return 0


if __name__ == "__main__":
    main()