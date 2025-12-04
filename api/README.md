# AI-Native Physical AI Textbook API

Backend API for the AI-Native Educational Platform, built with FastAPI and SQLAlchemy.

## Features

- **JWT Authentication**: Secure user authentication with role-based access control
- **Chapter Management**: CRUD operations for textbook chapters and sections
- **Progress Tracking**: Comprehensive learning analytics and progress monitoring
- **Chat with RAG**: AI-powered chat using Retrieval-Augmented Generation
- **Bookmarking & Notes**: Personal learning tools for students
- **RESTful API**: Clean, documented API endpoints

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 14+
- Node.js 18+ (for MCP server)
- Qdrant Vector Database (for RAG)

### Installation

1. Clone the repository
```bash
cd D:/quarter4-data/api
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Set up the database
```bash
# Create database
createdb ai_textbook

# Run migrations (when Alembic is set up)
alembic upgrade head
```

6. Start the API server
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user info
- `PUT /api/v1/auth/profile` - Update user profile

### Chapters
- `GET /api/v1/chapters` - List all chapters
- `GET /api/v1/chapters/{id}` - Get a specific chapter
- `POST /api/v1/chapters` - Create a new chapter (instructors/admins)
- `PUT /api/v1/chapters/{id}` - Update a chapter (instructors/admins)
- `DELETE /api/v1/chapters/{id}` - Delete a chapter (admins only)

### Progress
- `GET /api/v1/progress/` - Get overall progress
- `GET /api/v1/progress/overview` - Get detailed progress overview
- `GET /api/v1/progress/chapter/{id}` - Get chapter-specific progress
- `POST /api/v1/progress/chapter/{id}/update` - Update chapter progress
- `GET /api/v1/progress/bookmarks` - Get user bookmarks
- `POST /api/v1/progress/bookmarks` - Create a bookmark
- `GET /api/v1/progress/notes` - Get user notes
- `POST /api/v1/progress/notes` - Create a note

### Chat (RAG)
- `POST /api/v1/chat/search` - Search content using RAG
- `POST /api/v1/chat/conversations` - Create a new conversation
- `GET /api/v1/chat/conversations` - List conversations
- `GET /api/v1/chat/conversations/{id}` - Get a conversation
- `POST /api/v1/chat/` - Send a chat message
- `POST /api/v1/chat/feedback/{id}` - Submit feedback

## Database Schema

### Users
- Basic user information with roles (student, instructor, admin)
- Preferences and profile data stored as JSON
- Links to progress, bookmarks, and conversations

### Chapters
- Hierarchical structure (chapters -> sections)
- Metadata for difficulty, duration, prerequisites
- Content stored as structured JSON

### Progress Tracking
- User progress per chapter
- Time spent, completion percentage
- Quiz scores and lab completions
- Engagement metrics

### Chat System
- Conversations with message history
- RAG-powered responses with references
- Feedback system for continuous improvement

## RAG Integration

The API integrates with the MCP (Model Context Protocol) server for RAG functionality:

1. **MCP Server**: Runs on port 3001
   - Handles content ingestion
   - Provides search and chat endpoints
   - Integrates with Qdrant vector database

2. **Vector Database**: Qdrant
   - Stores embeddings of textbook content
   - Enables semantic search
   - Provides context for AI responses

## Configuration

Key environment variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_textbook

# Authentication
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# RAG Service
RAG_SERVICE_URL=http://localhost:3001

# OpenAI (optional)
OPENAI_API_KEY=sk-your-key-here
```

## Testing

Run the test suite:

```bash
pytest
```

With coverage:

```bash
pytest --cov=src --cov-report=html
```

## Development

### Code Style

We use:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Format code:

```bash
black src/
isort src/
```

### Adding New Endpoints

1. Create/update models in `src/models/`
2. Add schemas in `src/schemas/`
3. Implement routes in `src/routes/`
4. Update `main.py` to include new routes
5. Add tests in `tests/`

### Database Migrations

When making database changes:

1. Modify models
2. Generate migration:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```
3. Apply migration:
   ```bash
   alembic upgrade head
   ```

## Deployment

### Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production

- Set `DEBUG=false`
- Use a strong `SECRET_KEY`
- Configure proper database URL
- Set up CORS origins appropriately

## Security Considerations

- All endpoints except auth and health require authentication
- Role-based access control for sensitive operations
- Passwords are hashed using bcrypt
- JWT tokens have configurable expiration
- Input validation using Pydantic schemas

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is part of the AI-Native Physical AI Textbook initiative.