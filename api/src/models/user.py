from sqlalchemy import Column, String, DateTime, Boolean, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default='student')  # student, instructor, admin
    avatar = Column(String(500))
    bio = Column(Text)
    institution = Column(String(255))

    # Preferences stored as JSON
    preferences = Column(JSON, default=dict)

    # Profile data
    expertise = Column(JSON, default=list)  # List of expertise areas
    learning_goals = Column(JSON, default=list)  # Learning objectives

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    # Relationships
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    achievements_rel = relationship("Achievement", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    chapter_progress = relationship("ChapterProgress", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'avatar': self.avatar,
            'bio': self.bio,
            'institution': self.institution,
            'preferences': self.preferences or {},
            'expertise': self.expertise or [],
            'learning_goals': self.learning_goals or [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

    def __repr__(self):
        return f"<User(email='{self.email}', role='{self.role}')>"