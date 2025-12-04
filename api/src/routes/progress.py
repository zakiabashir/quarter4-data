from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from typing import List, Optional

from ..database import get_db
from ..models.progress import UserProgress, ChapterProgress, Bookmark, Note, Achievement
from ..models.user import User
from ..models.chapter import Chapter
from ..schemas.progress import UserProgressResponse, ChapterProgressResponse, BookmarkCreate, BookmarkResponse, NoteCreate, NoteResponse
from ..middleware.auth import get_current_active_user
from decimal import Decimal

router = APIRouter(prefix="/progress", tags=["Progress"])

def update_user_progress(db: Session, user_id: str):
    """Update user's overall progress"""
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()

    if not progress:
        progress = UserProgress(user_id=user_id)
        db.add(progress)

    # Count completed chapters
    completed_chapters = db.query(ChapterProgress).filter(
        and_(
            ChapterProgress.user_id == user_id,
            ChapterProgress.status == "completed"
        )
    ).count()

    progress.total_chapters_completed = completed_chapters
    progress.last_activity_date = datetime.utcnow()

    # Calculate total time spent across all chapters
    total_time = db.query(ChapterProgress).filter(
        ChapterProgress.user_id == user_id
    ).with_entities(ChapterProgress.time_spent).all()

    progress.total_time_spent = sum(cp.time_spent for cp in total_time)

    # Update streak (simple implementation)
    if progress.last_activity_date and progress.last_activity_date.date() < datetime.utcnow().date():
        # Check if they missed yesterday
        yesterday = datetime.utcnow() - timedelta(days=1)
        if progress.last_activity_date.date() != yesterday:
            progress.current_streak = 0
        else:
            progress.current_streak += 1

    db.commit()
    return progress

@router.get("/", response_model=UserProgressResponse)
async def get_user_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's overall progress"""
    progress = update_user_progress(db, current_user.id)
    return progress

@router.get("/overview")
async def get_progress_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get detailed progress overview including all chapters"""
    user_progress = update_user_progress(db, current_user.id)

    # Get all chapters with progress
    chapters_progress = db.query(ChapterProgress).filter(
        ChapterProgress.user_id == current_user.id
    ).all()

    chapter_progress_data = []
    total_chapters = db.query(Chapter).count()

    for cp in chapters_progress:
        chapter = db.query(Chapter).filter(Chapter.id == cp.chapter_id).first()
        if chapter:
            chapter_data = {
                "id": cp.id,
                "chapter": {
                    "id": chapter.id,
                    "number": chapter.number,
                    "title": chapter.title,
                    "slug": chapter.slug,
                    "difficulty": chapter.difficulty,
                    "estimated_duration": chapter.estimated_duration
                },
                "status": cp.status,
                "completion_percentage": cp.completion_percentage,
                "sections_completed": cp.sections_completed or [],
                "total_sections": cp.total_sections,
                "time_spent": cp.time_spent,
                "quiz_attempts": cp.quiz_attempts,
                "best_quiz_score": cp.best_quiz_score,
                "last_accessed": cp.last_accessed,
                "engagement_score": cp.engagement_score or 0.0
            }
            chapter_progress_data.append(chapter_data)

    return {
        "overall": {
            "total_chapters": total_chapters,
            "completed_chapters": user_progress.total_chapters_completed,
            "completion_percentage": user_progress.calculate_completion_percentage(),
            "total_time_spent": user_progress.total_time_spent,
            "current_streak": user_progress.current_streak
        },
        "chapters": chapter_progress_data,
        "learning_paths": user_progress.learning_paths or [],
        "achievements": user_progress.achievements or []
    }

@router.get("/chapter/{chapter_id}", response_model=ChapterProgressResponse)
async def get_chapter_progress(
    chapter_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get progress for a specific chapter"""
    # Verify chapter exists
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    progress = db.query(ChapterProgress).filter(
        and_(
            ChapterProgress.user_id == current_user.id,
            ChapterProgress.chapter_id == chapter_id
        )
    ).first()

    if not progress:
        # Create new progress entry
        progress = ChapterProgress(
            user_id=current_user.id,
            chapter_id=chapter_id,
            first_accessed=datetime.utcnow()
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)

    return progress

@router.post("/chapter/{chapter_id}/update")
async def update_chapter_progress(
    chapter_id: str,
    progress_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update chapter progress"""
    # Verify chapter exists
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    progress = db.query(ChapterProgress).filter(
        and_(
            ChapterProgress.user_id == current_user.id,
            ChapterProgress.chapter_id == chapter_id
        )
    ).first()

    if not progress:
        progress = ChapterProgress(
            user_id=current_user.id,
            chapter_id=chapter_id,
            first_accessed=datetime.utcnow()
        )
        db.add(progress)

    # Update progress
    if "sections_completed" in progress_data:
        progress.sections_completed = progress_data["sections_completed"]

    if "time_spent_delta" in progress_data:
        progress.time_spent += progress_data["time_spent_delta"]

    if "quiz_score" in progress_data:
        quiz_score = progress_data["quiz_score"]
        progress.quiz_attempts += 1
        progress.quiz_scores.append({
            "score": quiz_score,
            "attempt": progress.quiz_attempts,
            "date": datetime.utcnow().isoformat()
        })

        if quiz_score > progress.best_quiz_score:
            progress.best_quiz_score = quiz_score

    if "lab_completed" in progress_data:
        lab_id = progress_data["lab_completed"]
        if lab_id not in progress.labs_completed:
            progress.labs_completed.append(lab_id)
        progress.lab_attempts += 1

    # Update completion percentage
    if progress.total_sections > 0:
        progress.completion_percentage = round(
            (len(progress.sections_completed or []) / progress.total_sections) * 100, 2
        )
        if progress.completion_percentage >= 100 and progress.status != "completed":
            progress.status = "completed"
            progress.completion_date = datetime.utcnow()
        elif progress.completion_percentage < 100 and progress.status == "completed":
            progress.status = "in_progress"

    progress.last_accessed = datetime.utcnow()
    db.commit()

    # Update overall progress
    update_user_progress(db, current_user.id)

    return progress

@router.get("/bookmarks", response_model=List[BookmarkResponse])
async def get_bookmarks(
    chapter_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's bookmarks"""
    query = db.query(Bookmark).filter(Bookmark.user_id == current_user.id)

    if chapter_id:
        query = query.filter(Bookmark.chapter_id == chapter_id)

    bookmarks = query.order_by(Bookmark.created_at.desc()).all()
    return bookmarks

@router.post("/bookmarks", response_model=BookmarkResponse)
async def create_bookmark(
    bookmark: BookmarkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new bookmark"""
    # Verify chapter exists
    chapter = db.query(Chapter).filter(Chapter.id == bookmark.chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    db_bookmark = Bookmark(
        user_id=current_user.id,
        chapter_id=bookmark.chapter_id,
        content_type=bookmark.content_type,
        content_id=bookmark.content_id,
        title=bookmark.title,
        description=bookmark.description,
        note=bookmark.note,
        tags=bookmark.tags or [],
        position=bookmark.position or {},
        context=bookmark.context or {}
    )

    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)

    return db_bookmark

@router.delete("/bookmarks/{bookmark_id}")
async def delete_bookmark(
    bookmark_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a bookmark"""
    bookmark = db.query(Bookmark).filter(
        and_(
            Bookmark.id == bookmark_id,
            Bookmark.user_id == current_user.id
        )
    ).first()

    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )

    db.delete(bookmark)
    db.commit()

    return {"message": "Bookmark deleted successfully"}

@router.get("/notes", response_model=List[NoteResponse])
async def get_notes(
    chapter_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's notes"""
    query = db.query(Note).filter(Note.user_id == current_user.id)

    if chapter_id:
        query = query.filter(Note.chapter_id == chapter_id)

    notes = query.order_by(Note.updated_at.desc()).all()
    return notes

@router.post("/notes", response_model=NoteResponse)
async def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new note"""
    # Verify chapter exists
    chapter = db.query(Chapter).filter(Chapter.id == note.chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    db_note = Note(
        user_id=current_user.id,
        chapter_id=note.chapter_id,
        title=note.title,
        content=note.content,
        is_private=note.is_private,
        tags=note.tags or [],
        highlighted_text=note.highlighted_text,
        highlight_start=note.highlight_start,
        highlight_end=note.highlight_end
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note

@router.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: str,
    note_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a note"""
    note = db.query(Note).filter(
        and_(
            Note.id == note_id,
            Note.user_id == current_user.id
        )
    ).first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    # Update fields
    for field, value in note_update.items():
        setattr(note, field, value)

    note.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(note)

    return note

@router.delete("/notes/{note_id}")
async def delete_note(
    note_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a note"""
    note = db.query(Note).filter(
        and_(
            Note.id == note_id,
            Note.user_id == current_user.id
        )
    ).first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    db.delete(note)
    db.commit()

    return {"message": "Note deleted successfully"}

@router.get("/stats")
async def get_progress_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get progress statistics"""
    progress = update_user_progress(db, current_user.id)

    # Calculate engagement score based on various factors
    engagement_score = 0.0
    if progress.total_chapters_completed > 0:
        engagement_score += Decimal('0.3') * (progress.total_chapters_completed / 9)

    if progress.total_time_spent > 0:
        # Normalize time spent (assuming 100 hours = 1.0)
        engagement_score += Decimal('0.3') * min(progress.total_time_spent / 6000, 1.0)

    if progress.current_streak > 0:
        engagement_score += Decimal('0.2') * min(progress.current_streak / 7, 1.0)

    return {
        "total_chapters": 9,
        "completed_chapters": progress.total_chapters_completed,
        "completion_percentage": progress.calculate_completion_percentage(),
        "total_time_spent_hours": round(progress.total_time_spent / 60, 2),
        "current_streak_days": progress.current_streak,
        "engagement_score": float(engagement_score),
        "achievements_count": len(progress.achievements or []),
        "bookmarks_count": len(db.query(Bookmark).filter(Bookmark.user_id == current_user.id).all()),
        "notes_count": len(db.query(Note).filter(Note.user_id == current_user.id).all())
    }