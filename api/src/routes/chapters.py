from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..models.chapter import Chapter, Section
from ..models.user import User
from ..schemas.chapter import ChapterCreate, ChapterUpdate, ChapterResponse, SectionCreate, SectionResponse
from ..middleware.auth import get_current_active_user, get_optional_current_user

router = APIRouter(prefix="/chapters", tags=["Chapters"])

@router.get("/", response_model=List[ChapterResponse])
async def list_chapters(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    published_only: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """List all chapters"""
    query = db.query(Chapter)

    if published_only and (not current_user or current_user.role == "student"):
        query = query.filter(Chapter.is_published == True)

    chapters = query.offset(skip).limit(limit).all()
    return chapters

@router.get("/{chapter_id}", response_model=ChapterResponse)
async def get_chapter(
    chapter_id: str,
    include_content: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Get a specific chapter by ID"""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()

    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    # Check if user can access unpublished chapters
    if not chapter.is_published and (not current_user or current_user.role == "student"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chapter not published"
        )

    if include_content:
        return chapter
    else:
        return chapter.to_dict()

@router.get("/slug/{slug}", response_model=ChapterResponse)
async def get_chapter_by_slug(
    slug: str,
    include_content: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Get a chapter by slug"""
    chapter = db.query(Chapter).filter(Chapter.slug == slug).first()

    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    # Check if user can access unpublished chapters
    if not chapter.is_published and (not current_user or current_user.role == "student"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chapter not published"
        )

    if include_content:
        return chapter
    else:
        return chapter.to_dict()

@router.post("/", response_model=ChapterResponse)
async def create_chapter(
    chapter: ChapterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new chapter"""
    # Check if user has permission (instructor or admin)
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

    # Check if chapter number already exists
    existing_chapter = db.query(Chapter).filter(Chapter.number == chapter.number).first()
    if existing_chapter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Chapter {chapter.number} already exists"
        )

    # Check if slug already exists
    if chapter.slug:
        existing_slug = db.query(Chapter).filter(Chapter.slug == chapter.slug).first()
        if existing_slug:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Chapter with slug '{chapter.slug}' already exists"
            )

    # Create chapter
    db_chapter = Chapter(
        number=chapter.number,
        title=chapter.title,
        slug=chapter.slug,
        description=chapter.description,
        difficulty=chapter.difficulty,
        estimated_duration=chapter.estimated_duration,
        prerequisites=chapter.prerequisites,
        learning_objectives=chapter.learning_objectives,
        topics=chapter.topics,
        tools=chapter.tools,
        sections=chapter.sections or [],
        translations=chapter.translations or {},
        contributors=[current_user.email],
        is_published=chapter.is_published or False
    )

    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)

    return db_chapter

@router.put("/{chapter_id}", response_model=ChapterResponse)
async def update_chapter(
    chapter_id: str,
    chapter_update: ChapterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a chapter"""
    # Check if user has permission
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

    db_chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not db_chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    # Update fields
    update_data = chapter_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_chapter, field, value)

    # Update metadata
    db_chapter.updated_at = datetime.utcnow()
    if current_user.email not in db_chapter.contributors:
        db_chapter.contributors.append(current_user.email)

    db.commit()
    db.refresh(db_chapter)

    return db_chapter

@router.delete("/{chapter_id}")
async def delete_chapter(
    chapter_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a chapter"""
    # Only admins can delete chapters
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

    db_chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not db_chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    db.delete(db_chapter)
    db.commit()

    return {"message": "Chapter deleted successfully"}

@router.get("/{chapter_id}/sections", response_model=List[SectionResponse])
async def list_chapter_sections(
    chapter_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """List all sections in a chapter"""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    # Check if user can access unpublished chapters
    if not chapter.is_published and (not current_user or current_user.role == "student"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chapter not published"
        )

    sections = db.query(Section).filter(Section.chapter_id == chapter_id).order_by(Section.order_index).all()
    return sections

@router.post("/{chapter_id}/sections", response_model=SectionResponse)
async def create_section(
    chapter_id: str,
    section: SectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new section in a chapter"""
    # Check if user has permission
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

    # Verify chapter exists
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    # Create section
    db_section = Section(
        chapter_id=chapter_id,
        order_index=section.order_index,
        title=section.title,
        slug=section.slug,
        content=section.content,
        content_type=section.content_type,
        difficulty=section.difficulty,
        estimated_time=section.estimated_time,
        tags=section.tags or []
    )

    db.add(db_section)
    db.commit()
    db.refresh(db_section)

    return db_section

@router.get("/{chapter_id}/search")
async def search_chapter_content(
    chapter_id: str,
    query: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Search within chapter content"""
    # This would typically connect to a search service
    # For now, return a simple implementation

    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    # Simple text search in sections
    sections = db.query(Section).filter(
        Section.chapter_id == chapter_id,
        Section.content.ilike(f"%{query}%")
    ).all()

    return {
        "chapter_id": chapter_id,
        "query": query,
        "results": [section.to_dict() for section in sections],
        "total": len(sections)
    }