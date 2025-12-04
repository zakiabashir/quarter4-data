from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import os
from contextlib import asynccontextmanager

# Import routers
from src.routes import auth, chapters, progress, chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("AI Textbook API is starting up...")
    yield
    print("AI Textbook API is shutting down...")
    print("AI Textbook API is shutting down...")

app = FastAPI(
    title="AI-Native Physical AI Textbook API",
    description="Backend API for the AI-Native Educational Platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://ai-textbook.example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(chapters.router, prefix="/api/v1/chapters", tags=["Chapters"])
app.include_router(progress.router, prefix="/api/v1/progress", tags=["Progress"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "AI-Native Physical AI Textbook API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Run the app
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("ENVIRONMENT") == "development" else False
    )