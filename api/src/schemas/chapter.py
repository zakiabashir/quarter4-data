from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ChapterDifficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class SectionType(str, Enum):
    CONCEPT = "concept"
    EXAMPLE = "example"
    EXERCISE = "exercise"
    LAB = "lab"
    QUIZ = "quiz"

class ChapterBase(BaseModel):
    number: int = Field(..., ge=1, le=20)
    title: str = Field(..., min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    difficulty: ChapterDifficulty = ChapterDifficulty.INTERMEDIATE
    estimated_duration: Optional[int] = Field(None, ge=1, le=1000)  # minutes
    prerequisites: List[int] = Field(default_factory=list)
    learning_objectives: List[str] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    is_published: bool = False

class ChapterCreate(ChapterBase):
    sections: Optional[List[Dict[str, Any]] = Field(default_factory=list)
    translations: Optional[Dict[str, Dict[str, str]]] = Field(default_factory=dict)

    @validator('slug')
    def validate_slug(cls, v, values):
        if not v and 'title' in values:
            # Auto-generate slug from title
            v = values['title'].lower()
            v = v.replace(' ', '-')
            v = ''.join(c for c in v if c.isalnum() or c == '-')
        return v

class ChapterUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    difficulty: Optional[ChapterDifficulty] = None
    estimated_duration: Optional[int] = Field(None, ge=1, le=1000)
    prerequisites: Optional[List[int]] = None
    learning_objectives: Optional[List[str]] = None
    topics: Optional[List[str]] = None
    tools: Optional[List[str]] = None
    sections: Optional[List[Dict[str, Any]]] = None
    translations: Optional[Dict[str, Dict[str, str]]] = None
    is_published: Optional[bool] = None

class ChapterResponse(BaseModel):
    id: str
    number: int
    title: str
    slug: str
    description: Optional[str]
    difficulty: ChapterDifficulty
    estimated_duration: Optional[int]
    prerequisites: List[int]
    learning_objectives: List[str]
    topics: List[str]
    tools: List[str]
    sections: List[Dict[str, Any]]
    translations: Dict[str, Dict[str, str]]
    contributors: List[str]
    last_updated: datetime
    version: str
    is_published: bool

    class Config:
        from_attributes = True

class ChapterMetadata(BaseModel):
    id: str
    number: int
    title: str
    slug: str
    difficulty: ChapterDifficulty
    estimated_duration: Optional[int]
    total_sections: int
    total_estimated_time: int
    has_code_examples: bool
    has_quizzes: bool
    has_labs: bool
    completion_rate: Optional[float] = None  # For user progress

class SectionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    content: str
    content_type: SectionType = SectionType.CONCEPT
    difficulty: int = Field(default=1, ge=1, le=5)
    estimated_time: Optional[int] = Field(None, ge=1, le=180)  # minutes
    tags: List[str] = Field(default_factory=list)

class SectionCreate(SectionBase):
    order_index: int = Field(..., ge=0)

class SectionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    content_type: Optional[SectionType] = None
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    estimated_time: Optional[int] = Field(None, ge=1, le=180)
    tags: Optional[List[str]] = None

class SectionResponse(BaseModel):
    id: str
    chapter_id: str
    order_index: int
    title: str
    slug: str
    content: str
    content_type: SectionType
    difficulty: int
    estimated_time: Optional[int]
    tags: List[str]
    has_code_examples: bool = False
    has_simulations: bool = False
    has_quizzes: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChapterSearchResult(BaseModel):
    query: str
    total: int
    results: List[SectionResponse]

class ChapterList(BaseModel):
    chapters: List[ChapterMetadata]
    total: int
    page: int
    size: int

class ChapterProgress(BaseModel):
    chapter_id: str
    sections_completed: List[str]
    total_sections: int
    completion_percentage: float
    time_spent: int  # minutes
    last_accessed: datetime
    quiz_scores: List[Dict[str, Any]] = Field(default_factory=list)
    lab_completions: List[str] = Field(default_factory=list)