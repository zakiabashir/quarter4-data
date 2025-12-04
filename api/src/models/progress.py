from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, Float, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import uuid

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # Overall progress
    total_chapters_completed = Column(Integer, default=0)
    total_time_spent = Column(Integer, default=0)  # in minutes
    current_streak = Column(Integer, default=0)  # consecutive days
    last_activity_date = Column(DateTime(timezone=True))

    # Learning paths and goals
    learning_paths = Column(JSON, default=list)
    current_goal = Column(Text)
    achievements = Column(JSON, default=list)

    # Preferences
    preferred_difficulty = Column(String(20), default="intermediate")
    interests = Column(JSON, default=list)
    custom_goals = Column(JSON, default=list)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="progress")
    chapter_progress = relationship("ChapterProgress", back_populates="user_progress", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    achievements_rel = relationship("Achievement", back_populates="user", cascade="all, delete-orphan")

    def calculate_completion_percentage(self):
        """Calculate overall completion percentage"""
        if self.total_chapters_completed == 0:
            return 0.0
        # Assuming there are 9 total chapters
        return round((self.total_chapters_completed / 9) * 100, 2)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_chapters_completed': self.total_chapters_completed,
            'total_time_spent': self.total_time_spent,
            'current_streak': self.current_streak,
            'last_activity_date': self.last_activity_date.isoformat() if self.last_activity_date else None,
            'learning_paths': self.learning_paths or [],
            'current_goal': self.current_goal,
            'achievements': self.achievements or [],
            'preferred_difficulty': self.preferred_difficulty,
            'interests': self.interests or [],
            'custom_goals': self.custom_goals or [],
            'completion_percentage': self.calculate_completion_percentage(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ChapterProgress(Base):
    __tablename__ = "chapter_progress"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    chapter_id = Column(String, ForeignKey("chapters.id"), nullable=False, index=True)

    # Progress status
    status = Column(String(20), default="not_started")  # not_started, in_progress, completed
    completion_percentage = Column(Float, default=0.0)
    sections_completed = Column(JSON, default=list)  # List of section IDs
    total_sections = Column(Integer, default=0)

    # Time tracking
    time_spent = Column(Integer, default=0)  # in minutes
    first_accessed = Column(DateTime(timezone=True))
    last_accessed = Column(DateTime(timezone=True))
    completion_date = Column(DateTime(timezone=True))

    # Performance metrics
    quiz_attempts = Column(Integer, default=0)
    best_quiz_score = Column(Float, default=0.0)
    quiz_scores = Column(JSON, default=list)  # List of score objects
    lab_attempts = Column(Integer, default=0)
    labs_completed = Column(JSON, default=list)  # List of completed lab IDs
    notes_count = Column(Integer, default=0)

    # Learning analytics
    learning_path_taken = Column(JSON, default=list)  # Sections order
    difficulty_preference = Column(String(20))
    engagement_score = Column(Float, default=0.0)  # 0-1 scale

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user_progress = relationship("UserProgress", back_populates="chapter_progress")
    user = relationship("User", back_populates="chapter_progress")
    chapter = relationship("Chapter", back_populates="user_progress")
    bookmarks = relationship("Bookmark", back_populates="user", foreign_keys="bookmarks.user_id")
    notes = relationship("Note", back_populates="user", foreign_keys="notes.user_id")

    def update_progress(self, completed_sections, total_sections, time_spent_delta=0):
        """Update chapter progress"""
        self.sections_completed = completed_sections or []
        self.total_sections = total_sections or 0

        if len(completed_sections or []) > 0:
            self.status = "in_progress"

        if total_sections > 0:
            self.completion_percentage = round((len(self.sections_completed) / total_sections) * 100, 2)

            if self.completion_percentage >= 100:
                self.status = "completed"
                if not self.completion_date:
                    self.completion_date = func.now()
            elif self.status == "completed":
                self.status = "in_progress"
                self.completion_date = None

        self.time_spent += time_spent_delta
        self.last_accessed = func.now()

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'chapter_id': self.chapter_id,
            'status': self.status,
            'completion_percentage': self.completion_percentage,
            'sections_completed': self.sections_completed or [],
            'total_sections': self.total_sections,
            'time_spent': self.time_spent,
            'first_accessed': self.first_accessed.isoformat() if self.first_accessed else None,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'quiz_attempts': self.quiz_attempts,
            'best_quiz_score': self.best_quiz_score,
            'quiz_scores': self.quiz_scores or [],
            'lab_attempts': self.lab_attempts,
            'labs_completed': self.labs_completed or [],
            'notes_count': self.notes_count,
            'learning_path_taken': self.learning_path_taken or [],
            'difficulty_preference': self.difficulty_preference,
            'engagement_score': self.engagement_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    chapter_id = Column(String, ForeignKey("chapters.id"), nullable=False, index=True)

    # Bookmark details
    content_type = Column(String(50))  # section, code_example, diagram, etc.
    content_id = Column(String)  # ID of the specific content
    title = Column(String(255), nullable=False)
    description = Column(Text)
    note = Column(Text)  # User's personal note
    tags = Column(JSON, default=list)

    # Position data
    position = Column(JSON)  # Scroll position or other position data
    context = Column(JSON)  # Additional context when bookmarked

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="bookmarks")

class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    chapter_id = Column(String, ForeignKey("chapters.id"), nullable=False, index=True)

    # Note content
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    is_private = Column(Boolean, default=True)
    tags = Column(JSON, default=list)

    # Highlight data (if applicable)
    highlighted_text = Column(Text)
    highlight_start = Column(Integer)
    highlight_end = Column(Integer)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="notes")

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # Achievement details
    title = Column(String(255), nullable=False)
    description = Column(Text)
    icon = Column(String(100))  # Icon identifier
    category = Column(String(50))  # milestone, skill, time-based, etc.
    points = Column(Integer, default=0)

    # Achievement data
    achievement_metadata = Column(JSON, default=dict)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="achievements_rel")