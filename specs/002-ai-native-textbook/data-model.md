# Data Model: AI-Native Physical AI & Humanoid Robotics Textbook

**Date**: 2024-12-04
**Purpose**: Entity definitions and relationships for the educational platform

## Core Entities

### 1. User

```typescript
interface User {
  id: string;
  email: string;
  name: string;
  role: 'student' | 'instructor' | 'admin';
  preferences: UserPreferences;
  profile: UserProfile;
  createdAt: Date;
  updatedAt: Date;
}

interface UserPreferences {
  language: 'en' | 'ur';
  theme: 'light' | 'dark' | 'auto';
  contentDepth: 'beginner' | 'intermediate' | 'advanced';
  notifications: NotificationSettings;
  accessibility: AccessibilitySettings;
}

interface UserProfile {
  avatar?: string;
  bio?: string;
  institution?: string;
  expertise: string[];
  learningGoals: string[];
}
```

### 2. Chapter

```typescript
interface Chapter {
  id: string;
  number: number;
  title: string;
  slug: string;
  description: string;
  learningObjectives: string[];
  prerequisites: string[];
  estimatedDuration: number; // in minutes
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  sections: Section[];
  metadata: ChapterMetadata;
  translations: Translation[];
}

interface Section {
  id: string;
  chapterId: string;
  order: number;
  title: string;
  content: string; // MDX content
  type: 'concept' | 'example' | 'exercise' | 'lab' | 'quiz';
  interactiveElements: InteractiveElement[];
  codeExamples: CodeExample[];
  assessments: Assessment[];
}

interface ChapterMetadata {
  tags: string[];
  topics: string[];
  tools: string[];
  lastUpdated: Date;
  version: string;
  contributors: string[];
}
```

### 3. Progress Tracking

```typescript
interface UserProgress {
  userId: string;
  chapterProgress: ChapterProgress[];
  overallProgress: OverallProgress;
  achievements: Achievement[];
  bookmarks: Bookmark[];
  notes: Note[];
}

interface ChapterProgress {
  chapterId: string;
  status: 'not_started' | 'in_progress' | 'completed';
  sectionsCompleted: string[];
  timeSpent: number; // in minutes
  lastAccessed: Date;
  quizScores: QuizScore[];
  labCompletions: LabCompletion[];
}

interface OverallProgress {
  chaptersCompleted: number;
  totalChapters: number;
  totalTimeSpent: number;
  startDate: Date;
  estimatedCompletion: Date;
  streak: number; // consecutive days
}
```

### 4. RAG System

```typescript
interface DocumentChunk {
  id: string;
  content: string;
  metadata: ChunkMetadata;
  embedding: number[];
  chapterId: string;
  sectionId?: string;
  order: number;
}

interface ChunkMetadata {
  type: 'text' | 'code' | 'diagram' | 'example';
  language?: string;
  difficulty: string;
  topics: string[];
  prerequisites: string[];
  learningObjectives: string[];
}

interface ChatSession {
  id: string;
  userId: string;
  messages: ChatMessage[];
  context: ChatContext;
  createdAt: Date;
  updatedAt: Date;
}

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources: SourceReference[];
  timestamp: Date;
}
```

### 5. Code Execution

```typescript
interface CodeExecution {
  id: string;
  userId: string;
  code: string;
  language: 'python' | 'cpp' | 'ros2';
  input?: string;
  output: string;
  error?: string;
  executionTime: number;
  timestamp: Date;
  chapterId: string;
  exampleId?: string;
}

interface CodeExample {
  id: string;
  title: string;
  description: string;
  code: string;
  language: string;
  runnable: boolean;
  expectedOutput?: string;
  explanation: string;
  dependencies: string[];
}
```

### 6. Simulation

```typescript
interface SimulationEnvironment {
  id: string;
  name: string;
  type: 'gazebo' | 'unity' | 'isaac' | 'webgl';
  url: string;
  status: 'active' | 'maintenance' | 'deprecated';
  configuration: SimulationConfig;
  assets: SimulationAsset[];
}

interface SimulationSession {
  id: string;
  userId: string;
  environmentId: string;
  scenarioId: string;
  state: SimulationState;
  startedAt: Date;
  lastActivity: Date;
}

interface Scenario {
  id: string;
  chapterId: string;
  title: string;
  description: string;
  objectives: string[];
  steps: SimulationStep[];
  assessment: ScenarioAssessment;
}
```

### 7. Assessment

```typescript
interface Quiz {
  id: string;
  chapterId: string;
  title: string;
  questions: Question[];
  timeLimit?: number;
  passingScore: number;
  maxAttempts: number;
}

interface Question {
  id: string;
  type: 'multiple-choice' | 'true-false' | 'short-answer' | 'code';
  question: string;
  options?: string[];
  correctAnswer: string | string[];
  explanation: string;
  difficulty: number;
  hints: string[];
}

interface LabExercise {
  id: string;
  chapterId: string;
  title: string;
  objectives: string[];
  prerequisites: string[];
  steps: LabStep[];
  resources: LabResource[];
  submission: LabSubmission;
  evaluation: LabEvaluation;
}
```

## Database Schema

### PostgreSQL (Neon)

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'student',
    preferences JSONB DEFAULT '{}',
    profile JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Chapters
CREATE TABLE chapters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    number INTEGER UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    learning_objectives TEXT[],
    prerequisites TEXT[],
    estimated_duration INTEGER,
    difficulty chapter_difficulty NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Sections
CREATE TABLE sections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id UUID REFERENCES chapters(id) ON DELETE CASCADE,
    order_index INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    type section_type NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(chapter_id, order_index)
);

-- User Progress
CREATE TABLE user_progress (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    chapter_id UUID REFERENCES chapters(id) ON DELETE CASCADE,
    status progress_status NOT NULL DEFAULT 'not_started',
    sections_completed TEXT[] DEFAULT '{}',
    time_spent INTEGER DEFAULT 0,
    last_accessed TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, chapter_id)
);

-- Chat Sessions
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    context JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Chat Messages
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role message_role NOT NULL,
    content TEXT NOT NULL,
    sources JSONB DEFAULT '[]',
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Code Executions
CREATE TABLE code_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    code TEXT NOT NULL,
    language execution_language NOT NULL,
    input_text TEXT,
    output TEXT,
    error_message TEXT,
    execution_time INTEGER,
    chapter_id UUID REFERENCES chapters(id),
    example_id UUID,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Quiz Attempts
CREATE TABLE quiz_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    quiz_id UUID REFERENCES quizzes(id) ON DELETE CASCADE,
    answers JSONB NOT NULL,
    score INTEGER NOT NULL,
    attempt_number INTEGER NOT NULL,
    completed_at TIMESTAMP DEFAULT NOW()
);
```

### Types

```sql
CREATE TYPE user_role AS ENUM ('student', 'instructor', 'admin');
CREATE TYPE chapter_difficulty AS ENUM ('beginner', 'intermediate', 'advanced');
CREATE TYPE progress_status AS ENUM ('not_started', 'in_progress', 'completed');
CREATE TYPE section_type AS ENUM ('concept', 'example', 'exercise', 'lab', 'quiz');
CREATE TYPE message_role AS ENUM ('user', 'assistant');
CREATE TYPE execution_language AS ENUM ('python', 'cpp', 'ros2');
```

## Vector Database Schema (Qdrant)

### Collections

1. **content_chunks** - Embeddings for RAG
   - Vector: 1536 dimensions (OpenAI embeddings)
   - Metadata: chapter_id, section_id, type, difficulty, topics

2. **code_snippets** - Code-specific embeddings
   - Vector: 1536 dimensions
   - Metadata: language, complexity, context

3. **user_interactions** - User behavior embeddings
   - Vector: 512 dimensions
   - Metadata: user_id, interaction_type, timestamp

### Payload Structure

```json
{
  "id": "chunk_id",
  "content": "text content",
  "metadata": {
    "chapter_id": "uuid",
    "section_id": "uuid",
    "type": "text|code|diagram",
    "language": "python|cpp|ros2",
    "difficulty": "beginner|intermediate|advanced",
    "topics": ["topic1", "topic2"],
    "prerequisites": ["prereq1"],
    "learning_objectives": ["obj1"]
  }
}
```

## API Contracts

### Core Endpoints

1. **Authentication**
   - `POST /api/auth/login`
   - `POST /api/auth/logout`
   - `GET /api/auth/profile`

2. **Content**
   - `GET /api/chapters` - List all chapters
   - `GET /api/chapters/:id` - Get chapter details
   - `GET /api/chapters/:id/sections` - List chapter sections

3. **Progress**
   - `GET /api/progress` - Get user progress
   - `POST /api/progress/:chapterId` - Update chapter progress
   - `POST /api/bookmarks` - Add bookmark

4. **Chat**
   - `POST /api/chat/sessions` - Create chat session
   - `POST /api/chat/sessions/:id/messages` - Send message
   - `GET /api/chat/sessions/:id` - Get chat history

5. **Code Execution**
   - `POST /api/code/execute` - Execute code
   - `GET /api/code/examples/:id` - Get code example

6. **Simulations**
   - `GET /api/simulations` - List available simulations
   - `POST /api/simulations/:id/sessions` - Start simulation
   - `PUT /api/simulations/sessions/:id` - Update simulation state

## State Management

### Client State (React Context)

```typescript
interface AppContext {
  user: User | null;
  currentChapter: Chapter | null;
  progress: UserProgress | null;
  theme: 'light' | 'dark';
  language: 'en' | 'ur';
  settings: UserPreferences;
}

interface ChatContext {
  session: ChatSession | null;
  messages: ChatMessage[];
  isLoading: boolean;
}

interface SimulationContext {
  activeSession: SimulationSession | null;
  availableEnvironments: SimulationEnvironment[];
  isConnected: boolean;
}
```

### Server State

- User sessions stored in Redis
- Progress updates batched to database
- Chat context maintained per session
- Code execution state ephemeral