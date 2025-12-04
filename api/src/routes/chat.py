from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from datetime import datetime, timedelta
from typing import List, Optional
import asyncio
import httpx

from ..database import get_db
from ..models.chat import Conversation, ChatMessage, ChatUsage, ChatFeedback
from ..models.user import User
from ..models.chapter import Chapter
from ..schemas.chat import (
    ChatRequest, ChatResponse, ConversationCreate, ConversationUpdate,
    ConversationResponse, ChatMessageResponse, RAGSearchRequest,
    RAGSearchResponse, ChatSummary
)
from ..middleware.auth import get_current_active_user
from ..config import settings

router = APIRouter(prefix="/chat", tags=["Chat"])

# RAG service integration
RAG_SERVICE_URL = settings.RAG_SERVICE_URL or "http://localhost:3001"

async def call_rag_service(endpoint: str, payload: dict):
    """Call the RAG service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{RAG_SERVICE_URL}/{endpoint}",
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"RAG service unavailable: {str(e)}"
        )

@router.post("/search", response_model=RAGSearchResponse)
async def search_content(
    search_request: RAGSearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Search content using RAG"""
    # Prepare search payload
    payload = {
        "query": search_request.query,
        "context": {
            "chapter_ids": search_request.context_chapter_ids,
            "section_ids": search_request.context_section_ids,
            "content_types": search_request.content_types
        },
        "limit": search_request.limit,
        "similarity_threshold": search_request.similarity_threshold,
        "user_id": current_user.id
    }

    # Call RAG service
    search_results = await call_rag_service("search", payload)

    return RAGSearchResponse(
        results=search_results.get("results", []),
        total_found=search_results.get("total_found", 0),
        search_time_ms=search_results.get("search_time_ms", 0.0)
    )

@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new conversation"""
    db_conversation = Conversation(
        user_id=current_user.id,
        title=conversation.title,
        context_type=conversation.context_type,
        context_ids=conversation.context_ids or []
    )

    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)

    return db_conversation

@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    skip: int = 0,
    limit: int = 50,
    include_archived: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List user's conversations"""
    query = db.query(Conversation).filter(Conversation.user_id == current_user.id)

    if not include_archived:
        query = query.filter(Conversation.is_archived == False)

    conversations = query.order_by(desc(Conversation.last_message_at)).offset(skip).limit(limit).all()
    return conversations

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific conversation"""
    conversation = db.query(Conversation).filter(
        and_(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    return conversation

@router.put("/conversations/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: str,
    conversation_update: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a conversation"""
    conversation = db.query(Conversation).filter(
        and_(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Update fields
    update_data = conversation_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(conversation, field, value)

    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(conversation)

    return conversation

@router.get("/conversations/{conversation_id}/messages", response_model=List[ChatMessageResponse])
async def get_conversation_messages(
    conversation_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get messages in a conversation"""
    # Verify conversation ownership
    conversation = db.query(Conversation).filter(
        and_(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    messages = db.query(ChatMessage).filter(
        ChatMessage.conversation_id == conversation_id
    ).order_by(ChatMessage.created_at).offset(skip).limit(limit).all()

    return messages

@router.post("/", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Send a chat message and get AI response"""
    start_time = datetime.utcnow()

    # Get or create conversation
    conversation = None
    if chat_request.conversation_id:
        conversation = db.query(Conversation).filter(
            and_(
                Conversation.id == chat_request.conversation_id,
                Conversation.user_id == current_user.id
            )
        ).first()
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        # Create new conversation
        conversation = Conversation(
            user_id=current_user.id,
            title=chat_request.message[:50] + ("..." if len(chat_request.message) > 50 else ""),
            context_type="general"
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Create user message
    user_message = ChatMessage(
        conversation_id=conversation.id,
        user_id=current_user.id,
        content=chat_request.message,
        role="user",
        message_type="text",
        metadata=chat_request.context or {}
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # Get context for RAG if requested
    search_results = []
    references = []
    if chat_request.search_context:
        search_payload = {
            "query": chat_request.message,
            "context": chat_request.context or {},
            "limit": chat_request.max_context_items,
            "user_id": current_user.id
        }

        try:
            search_results = await call_rag_service("search", search_payload)
            references = search_results.get("results", [])
        except:
            # Continue without search results if RAG service fails
            pass

    # Generate AI response
    chat_payload = {
        "message": chat_request.message,
        "context": chat_request.context or {},
        "conversation_history": [],  # TODO: Get recent messages
        "references": references,
        "temperature": chat_request.temperature,
        "max_tokens": chat_request.max_tokens,
        "user_id": current_user.id
    }

    try:
        ai_response = await call_rag_service("chat", chat_payload)
        assistant_message_content = ai_response.get("response", "I'm sorry, I couldn't generate a response.")
        usage_data = ai_response.get("usage", {})
    except:
        # Fallback response if AI service fails
        assistant_message_content = "I'm sorry, the AI service is currently unavailable. Please try again later."
        usage_data = {}

    # Create assistant message
    assistant_message = ChatMessage(
        conversation_id=conversation.id,
        user_id=current_user.id,
        parent_message_id=user_message.id,
        content=assistant_message_content,
        role="assistant",
        message_type="text",
        references=references
    )
    db.add(assistant_message)

    # Update conversation
    conversation.message_count += 2  # user + assistant messages
    conversation.last_message_at = datetime.utcnow()
    if conversation.message_count == 2:  # First exchange
        conversation.title = chat_request.message[:50] + ("..." if len(chat_request.message) > 50 else "")

    # Track usage
    response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
    usage = ChatUsage(
        user_id=current_user.id,
        conversation_id=conversation.id,
        message_id=assistant_message.id,
        prompt_tokens=usage_data.get("prompt_tokens", 0),
        completion_tokens=usage_data.get("completion_tokens", 0),
        total_tokens=usage_data.get("total_tokens", 0),
        model_used=usage_data.get("model", "unknown"),
        response_time_ms=int(response_time)
    )
    db.add(usage)

    db.commit()
    db.refresh(assistant_message)
    db.refresh(conversation)

    return ChatResponse(
        message=assistant_message,
        conversation=conversation,
        references=references,
        search_results=search_results if chat_request.search_context else None,
        usage=usage_data
    )

@router.post("/feedback/{message_id}")
async def create_feedback(
    message_id: str,
    rating: int,
    comment: Optional[str] = None,
    helpful: Optional[bool] = None,
    issue_types: Optional[List[str]] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create feedback for a chat message"""
    # Verify message ownership
    message = db.query(ChatMessage).filter(
        and_(
            ChatMessage.id == message_id,
            ChatMessage.user_id == current_user.id,
            ChatMessage.role == "assistant"
        )
    ).first()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    # Check if feedback already exists
    existing_feedback = db.query(ChatFeedback).filter(
        ChatFeedback.message_id == message_id
    ).first()

    if existing_feedback:
        # Update existing feedback
        existing_feedback.rating = rating
        existing_feedback.comment = comment
        existing_feedback.helpful = helpful
        existing_feedback.issue_types = issue_types or []
        existing_feedback.updated_at = datetime.utcnow()
        feedback = existing_feedback
    else:
        # Create new feedback
        feedback = ChatFeedback(
            message_id=message_id,
            user_id=current_user.id,
            rating=rating,
            comment=comment,
            helpful=helpful,
            issue_types=issue_types or []
        )
        db.add(feedback)

    db.commit()
    db.refresh(feedback)

    return {"message": "Feedback submitted successfully", "feedback_id": feedback.id}

@router.get("/summary", response_model=ChatSummary)
async def get_chat_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get chat usage summary"""
    # Basic counts
    total_conversations = db.query(func.count(Conversation.id)).filter(
        Conversation.user_id == current_user.id
    ).scalar() or 0

    total_messages = db.query(func.count(ChatMessage.id)).filter(
        ChatMessage.user_id == current_user.id
    ).scalar() or 0

    active_conversations = db.query(func.count(Conversation.id)).filter(
        and_(
            Conversation.user_id == current_user.id,
            Conversation.is_archived == False
        )
    ).scalar() or 0

    archived_conversations = total_conversations - active_conversations

    # Average messages per conversation
    avg_messages = 0.0
    if total_conversations > 0:
        avg_messages = total_messages / total_conversations

    # Activity last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_activity = db.query(
        func.date(ChatMessage.created_at).label('date'),
        func.count(ChatMessage.id).label('count')
    ).filter(
        and_(
            ChatMessage.user_id == current_user.id,
            ChatMessage.created_at >= thirty_days_ago
        )
    ).group_by(func.date(ChatMessage.created_at)).all()

    activity_data = [
        {"date": str(item.date), "count": item.count}
        for item in recent_activity
    ]

    # TODO: Most discussed topics (needs message content analysis)
    most_discussed_topics = []

    return ChatSummary(
        total_conversations=total_conversations,
        total_messages=total_messages,
        active_conversations=active_conversations,
        archived_conversations=archived_conversations,
        average_messages_per_conversation=round(avg_messages, 2),
        most_discussed_topics=most_discussed_topics,
        activity_last_30_days=activity_data
    )