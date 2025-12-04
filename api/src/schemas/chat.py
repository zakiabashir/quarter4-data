from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessageType(str, Enum):
    TEXT = "text"
    CODE = "code"
    IMAGE = "image"
    REFERENCE = "reference"
    QUIZ = "quiz"
    EXERCISE = "exercise"

class ChatMessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)
    role: ChatRole
    message_type: ChatMessageType = ChatMessageType.TEXT
    metadata: Optional[Dict[str, Any]] = {}

class ChatMessageCreate(ChatMessageBase):
    conversation_id: Optional[str] = None
    parent_message_id: Optional[str] = None
    context_chapter_ids: Optional[List[str]] = []
    context_section_ids: Optional[List[str]] = []

class ChatMessageResponse(ChatMessageBase):
    id: str
    conversation_id: str
    user_id: str
    parent_message_id: Optional[str]
    context_chapter_ids: List[str]
    context_section_ids: List[str]
    references: List[Dict[str, Any]]
    embedding_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    context_type: str = Field(default="general", regex="^(general|chapter|section|quiz)$")
    context_ids: Optional[List[str]] = []

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    context_type: Optional[str] = Field(None, regex="^(general|chapter|section|quiz)$")
    context_ids: Optional[List[str]] = None
    is_archived: Optional[bool] = None

class ConversationResponse(ConversationBase):
    id: str
    user_id: str
    message_count: int
    last_message_at: Optional[datetime]
    is_archived: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = {}
    search_context: bool = True
    max_context_items: int = Field(default=5, ge=1, le=20)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=1000, ge=1, le=4000)

class ChatResponse(BaseModel):
    message: ChatMessageResponse
    conversation: ConversationResponse
    references: List[Dict[str, Any]]
    search_results: Optional[List[Dict[str, Any]]]
    usage: Dict[str, Any]

class RAGSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    context_chapter_ids: Optional[List[str]] = []
    context_section_ids: Optional[List[str]] = []
    content_types: Optional[List[str]] = []
    limit: int = Field(default=5, ge=1, le=20)
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0)

class RAGSearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total_found: int
    search_time_ms: float
    query_embedding: Optional[List[float]] = None

class ChatSummary(BaseModel):
    total_conversations: int
    total_messages: int
    active_conversations: int
    archived_conversations: int
    average_messages_per_conversation: float
    most_discussed_topics: List[Dict[str, Any]]
    activity_last_30_days: List[Dict[str, Any]]