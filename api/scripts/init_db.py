#!/usr/bin/env python3
"""
Database initialization script for the AI Physical AI Textbook application.
This script creates the database tables and populates them with sample data.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from src.models.user import User
from src.models.progress import UserProgress, Bookmark, Note, Achievement
from src.models.content import Chapter, Section, Quiz, QuizQuestion
from src.database import get_db_url, Base
from src.core.security import get_password_hash

DATABASE_URL = get_db_url()


def create_sample_users():
    """Create sample users for testing"""
    engine = create_engine(DATABASE_URL)

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
                        INSERT INTO users (email, username, full_name, hashed_password, role, is_active)
                        VALUES (:email, :username, :full_name, :hashed_password, :role, :is_active)
                    """),
                    user_data
                )
                print(f"Created user: {user_data['email']}")
        conn.commit()


def create_sample_content():
    """Create sample chapters and sections"""
    engine = create_engine(DATABASE_URL)

    sample_chapters = [
        {
            "title": "Introduction to Physical AI",
            "description": "Learn the fundamentals of Physical AI, including perception, decision-making, and actuation.",
            "order_index": 1,
            "estimated_hours": 5,
            "difficulty": "beginner",
        },
        {
            "title": "Robotics Fundamentals",
            "description": "Explore the core concepts of robotics, including kinematics, dynamics, and control systems.",
            "order_index": 2,
            "estimated_hours": 8,
            "difficulty": "intermediate",
        },
        {
            "title": "Computer Vision for Physical AI",
            "description": "Deep dive into computer vision techniques used in physical AI systems.",
            "order_index": 3,
            "estimated_hours": 10,
            "difficulty": "intermediate",
        },
    ]

    sample_sections = [
        {
            "chapter_id": 1,
            "title": "What is Physical AI?",
            "content": "Physical AI refers to artificial intelligence systems that interact with the physical world...",
            "order_index": 1,
            "type": "lesson",
        },
        {
            "chapter_id": 1,
            "title": "Sensors and Perception",
            "content": "Perception is the foundation of Physical AI systems. Common sensors include...",
            "order_index": 2,
            "type": "lesson",
        },
        {
            "chapter_id": 1,
            "title": "Decision Making Algorithms",
            "content": "Physical AI systems must make decisions based on sensory input...",
            "order_index": 3,
            "type": "lesson",
        },
        {
            "chapter_id": 1,
            "title": "Actuation Systems",
            "content": "Actuators are the muscles of Physical AI systems...",
            "order_index": 4,
            "type": "lesson",
        },
    ]

    with engine.connect() as conn:
        # Insert chapters
        for chapter in sample_chapters:
            result = conn.execute(
                text("SELECT id FROM chapters WHERE title = :title"),
                {"title": chapter["title"]}
            ).fetchone()

            if not result:
                conn.execute(
                    text("""
                        INSERT INTO chapters (title, description, order_index, estimated_hours, difficulty)
                        VALUES (:title, :description, :order_index, :estimated_hours, :difficulty)
                        RETURNING id
                    """),
                    chapter
                )
                print(f"Created chapter: {chapter['title']}")

        # Get chapter IDs
        chapter_ids = {}
        chapters = conn.execute(text("SELECT id, title FROM chapters")).fetchall()
        for chapter in chapters:
            chapter_ids[chapter.title] = chapter.id

        # Insert sections
        for section in sample_sections:
            section["chapter_id"] = chapter_ids.get("Introduction to Physical AI", 1)
            result = conn.execute(
                text("SELECT id FROM sections WHERE title = :title"),
                {"title": section["title"]}
            ).fetchone()

            if not result:
                conn.execute(
                    text("""
                        INSERT INTO sections (chapter_id, title, content, order_index, type)
                        VALUES (:chapter_id, :title, :content, :order_index, :type)
                    """),
                    section
                )
                print(f"Created section: {section['title']}")

        conn.commit()


def create_sample_quizzes():
    """Create sample quiz questions"""
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        # Get section ID for the first section
        result = conn.execute(
            text("SELECT id FROM sections WHERE title = 'What is Physical AI?' LIMIT 1")
        ).fetchone()

        if result:
            section_id = result.id

            sample_quiz = {
                "section_id": section_id,
                "title": "Introduction to Physical AI Quiz",
                "description": "Test your understanding of Physical AI fundamentals",
                "time_limit_minutes": 15,
                "passing_score": 70,
            }

            # Insert quiz
            quiz_result = conn.execute(
                text("""
                    INSERT INTO quizzes (section_id, title, description, time_limit_minutes, passing_score)
                    VALUES (:section_id, :title, :description, :time_limit_minutes, :passing_score)
                    RETURNING id
                """),
                sample_quiz
            )
            quiz_id = quiz_result.fetchone().id

            # Insert quiz questions
            sample_questions = [
                {
                    "quiz_id": quiz_id,
                    "question_text": "What is the core definition of Physical AI?",
                    "question_type": "multiple_choice",
                    "options": json.dumps([
                        "AI that exists purely in digital spaces",
                        "AI that processes large datasets",
                        "AI that interacts with and manipulates the physical world",
                        "AI that plays games"
                    ]),
                    "correct_answer": "AI that interacts with and manipulates the physical world",
                    "points": 10,
                    "order_index": 1,
                },
                {
                    "quiz_id": quiz_id,
                    "question_text": "Which of the following is NOT a component of Physical AI systems?",
                    "question_type": "multiple_choice",
                    "options": json.dumps([
                        "Perception",
                        "Decision-making",
                        "Actuation",
                        "Cloud computing"
                    ]),
                    "correct_answer": "Cloud computing",
                    "points": 10,
                    "order_index": 2,
                },
                {
                    "quiz_id": quiz_id,
                    "question_text": "Name three sensors commonly used in Physical AI systems.",
                    "question_type": "text",
                    "correct_answer": "Cameras, LiDAR, Radar, IMU, etc.",
                    "points": 15,
                    "order_index": 3,
                },
            ]

            for question in sample_questions:
                conn.execute(
                    text("""
                        INSERT INTO quiz_questions (
                            quiz_id, question_text, question_type, options,
                            correct_answer, points, order_index
                        )
                        VALUES (
                            :quiz_id, :question_text, :question_type, :options,
                            :correct_answer, :points, :order_index
                        )
                    """),
                    question
                )

            print(f"Created quiz with {len(sample_questions)} questions")

        conn.commit()


def create_sample_achievements():
    """Create sample achievements"""
    engine = create_engine(DATABASE_URL)

    sample_achievements = [
        {
            "title": "First Steps",
            "description": "Complete your first lesson",
            "badge_icon": "🎯",
            "points": 10,
            "type": "milestone",
        },
        {
            "title": "Quick Learner",
            "description": "Complete a chapter in less than 24 hours",
            "badge_icon": "⚡",
            "points": 25,
            "type": "speed",
        },
        {
            "title": "Perfectionist",
            "description": "Score 100% on a quiz",
            "badge_icon": "💯",
            "points": 50,
            "type": "performance",
        },
        {
            "title": "Code Master",
            "description": "Successfully run 10 interactive code examples",
            "badge_icon": "💻",
            "points": 30,
            "type": "practice",
        },
    ]

    with engine.connect() as conn:
        for achievement in sample_achievements:
            result = conn.execute(
                text("SELECT id FROM achievements WHERE title = :title"),
                {"title": achievement["title"]}
            ).fetchone()

            if not result:
                conn.execute(
                    text("""
                        INSERT INTO achievements (title, description, badge_icon, points, type)
                        VALUES (:title, :description, :badge_icon, :points, :type)
                    """),
                    achievement
                )
                print(f"Created achievement: {achievement['title']}")

        conn.commit()


def main():
    """Main initialization function"""
    print("Starting database initialization...")

    # Create all tables
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

    # Import json for quiz questions
    import json

    # Create sample data
    create_sample_users()
    create_sample_content()
    create_sample_quizzes()
    create_sample_achievements()

    print("\n✅ Database initialization completed successfully!")
    print("\nSample user credentials:")
    print("  Student: student@example.com / password123")
    print("  Instructor: instructor@example.com / password123")
    print("  Admin: admin@example.com / password123")


if __name__ == "__main__":
    main()