from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, Boolean, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import uuid

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # Conversation details
    title = Column(String(255), nullable=False)
    context_type = Column(String(20), default="general")  # general, chapter, section, quiz
    context_ids = Column(JSON, default=list)  # Related chapter/section IDs
    is_archived = Column(Boolean, default=False)

    # Metadata
    message_count = Column(Integer, default=0)
    last_message_at = Column(DateTime(timezone=True))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("ChatMessage", back_populates="conversation", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'context_type': self.context_type,
            'context_ids': self.context_ids or [],
            'is_archived': self.is_archived,
            'message_count': self.message_count,
            'last_message_at': self.last_message_at.isoformat() if self.last_message_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    parent_message_id = Column(String, ForeignKey("chat_messages.id"), nullable=True)

    # Message content
    content = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system
    message_type = Column(String(20), default="text")  # text, code, image, reference, quiz, exercise

    # Context information
    context_chapter_ids = Column(JSON, default=list)
    context_section_ids = Column(JSON, default=list)
    references = Column(JSON, default=list)  # Referenced content

    # AI/ML data
    embedding_id = Column(String)  # Reference to vector storage
    message_metadata = Column(JSON, default=dict)  # Additional metadata
    token_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    user = relationship("User", back_populates="chat_messages")
    parent_message = relationship("ChatMessage", remote_side=[id])

    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'user_id': self.user_id,
            'parent_message_id': self.parent_message_id,
            'content': self.content,
            'role': self.role,
            'message_type': self.message_type,
            'context_chapter_ids': self.context_chapter_ids or [],
            'context_section_ids': self.context_section_ids or [],
            'references': self.references or [],
            'embedding_id': self.embedding_id,
            'metadata': self.message_metadata or {},
            'token_count': self.token_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ChatUsage(Base):
    __tablename__ = "chat_usage"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False, index=True)
    message_id = Column(String, ForeignKey("chat_messages.id"), nullable=False)

    # Usage metrics
    prompt_tokens: int = Column(Integer, default=0)
    completion_tokens: int = Column(Integer, default=0)
    total_tokens: int = Column(Integer, default=0)
    model_used = Column(String(100))
    response_time_ms: int = Column(Integer, default=0)
    search_time_ms: int = Column(Integer, default=0)

    # Cost tracking (if applicable)
    cost_usd = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    conversation = relationship("Conversation")
    message = relationship("ChatMessage")

class ChatFeedback(Base):
    __tablename__ = "chat_feedback"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    message_id = Column(String, ForeignKey("chat_messages.id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # Feedback
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text)
    helpful = Column(Boolean)  # True/False/None

    # Feedback categories
    issue_types = Column(JSON, default=list)  # ["inaccurate", "unclear", "incomplete", etc.]

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    message = relationship("ChatMessage")
    user = relationship("User")