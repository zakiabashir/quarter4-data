from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ProgressStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"

class UserProgressResponse(BaseModel):
    id: str
    user_id: str
    total_chapters_completed: int
    total_time_spent: int  # in minutes
    current_streak: int
    last_activity_date: Optional[datetime]
    learning_paths: List[str]
    current_goal: Optional[str]
    achievements: List[Dict[str, Any]]
    preferred_difficulty: str
    interests: List[str]
    custom_goals: List[Dict[str, Any]]
    completion_percentage: float
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ChapterProgressResponse(BaseModel):
    id: str
    user_id: str
    chapter_id: str
    status: ProgressStatus
    completion_percentage: float
    sections_completed: List[str]
    total_sections: int
    time_spent: int  # in minutes
    first_accessed: Optional[datetime]
    last_accessed: Optional[datetime]
    completion_date: Optional[datetime]
    quiz_attempts: int
    best_quiz_score: float
    quiz_scores: List[Dict[str, Any]]
    lab_attempts: int
    labs_completed: List[str]
    notes_count: int
    learning_path_taken: List[str]
    difficulty_preference: Optional[str]
    engagement_score: float
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class BookmarkCreate(BaseModel):
    chapter_id: str
    content_type: str = Field(..., min_length=1, max_length=50)
    content_id: str
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    note: Optional[str] = None
    tags: Optional[List[str]] = []
    position: Optional[Dict[str, Any]] = {}
    context: Optional[Dict[str, Any]] = {}

class BookmarkResponse(BaseModel):
    id: str
    user_id: str
    chapter_id: str
    content_type: str
    content_id: str
    title: str
    description: Optional[str]
    note: Optional[str]
    tags: List[str]
    position: Dict[str, Any]
    context: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class NoteCreate(BaseModel):
    chapter_id: str
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    is_private: bool = True
    tags: Optional[List[str]] = []
    highlighted_text: Optional[str] = None
    highlight_start: Optional[int] = None
    highlight_end: Optional[int] = None

class NoteResponse(BaseModel):
    id: str
    user_id: str
    chapter_id: str
    title: str
    content: str
    is_private: bool
    tags: List[str]
    highlighted_text: Optional[str]
    highlight_start: Optional[int]
    highlight_end: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ProgressUpdate(BaseModel):
    sections_completed: Optional[List[str]] = None
    time_spent_delta: Optional[int] = Field(None, ge=0)
    quiz_score: Optional[float] = Field(None, ge=0, le=100)
    lab_completed: Optional[str] = None

class AchievementResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str]
    icon: Optional[str]
    category: str
    points: int
    metadata: Dict[str, Any]
    earned_at: datetime

    class Config:
        from_attributes = True

class ProgressStats(BaseModel):
    total_chapters: int
    completed_chapters: int
    completion_percentage: float
    total_time_spent_hours: float
    current_streak_days: int
    engagement_score: float
    achievements_count: int
    bookmarks_count: int
    notes_count: int