from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import uuid

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    number = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)

    # Chapter metadata
    difficulty = Column(String(20), nullable=False)  # beginner, intermediate, advanced
    estimated_duration = Column(Integer)  # in minutes
    prerequisites = Column(JSON, default=list)  # List of chapter numbers
    learning_objectives = Column(JSON, default=list)
    topics = Column(JSON, default=list)
    tools = Column(JSON, default=list)

    # Content structure
    sections = Column(JSON, default=list)  # List of section objects

    # Localization
    translations = Column(JSON, default=dict)  # {language: {title, description, ...}}

    # Metadata
    contributors = Column(JSON, default=list)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    version = Column(String(20), default="1.0.0")
    is_published = Column(Boolean, default=False)

    # Relationships
    sections_rel = relationship("Section", back_populates="chapter", cascade="all, delete-orphan")
    user_progress = relationship("ChapterProgress", back_populates="chapter", cascade="all, delete-orphan")

    def to_dict(self, include_content=False):
        """Convert chapter to dictionary"""
        result = {
            'id': self.id,
            'number': self.number,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'difficulty': self.difficulty,
            'estimated_duration': self.estimated_duration,
            'prerequisites': self.prerequisites or [],
            'learning_objectives': self.learning_objectives or [],
            'topics': self.topics or [],
            'tools': self.tools or [],
            'sections': self.sections or [],
            'translations': self.translations or {},
            'contributors': self.contributors or [],
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'version': self.version,
            'is_published': self.is_published
        }

        if include_content:
            result['sections_content'] = [s.to_dict() for s in self.sections_rel]

        return result

    def get_section(self, section_slug):
        """Get a specific section by slug"""
        for section in self.sections_rel:
            if section.slug == section_slug:
                return section
        return None

    def __repr__(self):
        return f"<Chapter(number={self.number}, title='{self.title}')>"

class Section(Base):
    __tablename__ = "sections"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chapter_id = Column(String, nullable=False, index=True)
    order_index = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)

    # Content
    content = Column(Text)  # MDX content
    content_type = Column(String(50), nullable=False)  # concept, example, exercise, lab, quiz

    # Metadata
    difficulty = Column(Integer, default=1)  # 1-5 scale
    estimated_time = Column(Integer)  # in minutes
    tags = Column(JSON, default=list)

    # Interactive elements
    has_code_examples = Column(Boolean, default=False)
    has_simulations = Column(Boolean, default=False)
    has_quizzes = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    chapter = relationship("Chapter", back_populates="sections_rel")

    def to_dict(self):
        """Convert section to dictionary"""
        return {
            'id': self.id,
            'chapter_id': self.chapter_id,
            'order_index': self.order_index,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'content_type': self.content_type,
            'difficulty': self.difficulty,
            'estimated_time': self.estimated_time,
            'tags': self.tags or [],
            'has_code_examples': self.has_code_examples,
            'has_simulations': self.has_simulations,
            'has_quizzes': self.has_quizzes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<Section(title='{self.title}', type='{self.content_type}')>"