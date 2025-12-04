# Quick Start Guide: AI-Native Physical AI & Humanoid Robotics Textbook

This guide helps you get started with the AI-Native Educational Platform for Physical AI and Humanoid Robotics.

## Prerequisites

- Node.js 18+ and npm
- Git
- Docker (for local development)
- Code editor (VS Code recommended)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/ai-physical-textbook.git
cd ai-physical-textbook
```

### 2. Install Dependencies

```bash
# Install root dependencies
npm install

# Install app dependencies
cd apps/book-docusaurus
npm install

# Install package dependencies
cd ../../packages/spec-kit-plus
npm install
```

### 3. Environment Configuration

Create environment files:

```bash
# In apps/book-docusaurus/.env
CONTEXT7_MCP_SERVER=http://localhost:3001
QDRANT_URL=http://localhost:6333
NEON_DATABASE_URL=postgresql://user:password@localhost:5432/dbname
OPENAI_API_KEY=your-openai-key
```

```bash
# In .env at root
NODE_ENV=development
```

### 4. Start Development Services

```bash
# Start Qdrant (vector database)
docker run -p 6333:6333 qdrant/qdrant

# Start the MCP server
npm run start:mcp

# In a new terminal, start the Docusaurus app
cd apps/book-docusaurus
npm run start
```

### 5. Verify Installation

Open http://localhost:3000 in your browser. You should see:
- The textbook homepage
- Chapter navigation
- Interactive chatbot (may need data ingestion)

## First Time Setup

### 1. Ingest Content

```bash
# From project root
npm run ingest:content
```

This processes all Markdown files and creates vector embeddings for the RAG system.

### 2. Create Test User

```bash
npm run create:test-user
```

This creates a test user account for development.

### 3. Run Health Check

```bash
npm run health:check
```

Verifies all services are running correctly.

## Development Workflow

### Creating New Chapter Content

1. Create chapter directory:
```bash
mkdir -p apps/book-docusaurus/docs/chapterX-title
```

2. Add content file:
```markdown
---
title: "Chapter X: Title"
description: "Chapter description"
---

## Learning Objectives

- Objective 1
- Objective 2

## Content

Your chapter content here...

### Code Example

```python
print("Hello, Physical AI!")
```

### Diagram

```mermaid
graph LR
    A[Input] --> B[Process]
    B --> C[Output]
```

### Quiz

<Quiz
  question="What is Physical AI?"
  options={[
    "AI in physical robots",
    "AI in software only",
    "AI in data analysis"
  ]}
  correctAnswer={0}
/>
```

3. Update navigation:
Edit `apps/book-docusaurus/sidebars.js` to include the new chapter.

### Adding Interactive Components

1. Code execution:
```jsx
<CodeBlock language="python" runnable>
  {codeString}
</CodeBlock>
```

2. Simulation integration:
```jsx
<Simulation
  environment="gazebo"
  scenario="basic_robot"
/>
```

3. Interactive chat:
```jsx
<ChatAssistant
  context={chapterContext}
  initialMessage="Ask me about this chapter!"
/>
```

## Testing

### Unit Tests
```bash
npm run test
```

### Integration Tests
```bash
npm run test:integration
```

### E2E Tests
```bash
npm run test:e2e
```

### Content Validation
```bash
npm run validate:content
```

## Deployment

### Build for Production

```bash
# Build the application
npm run build

# Test production build locally
npm run serve
```

### Deploy to Vercel

1. Connect repository to Vercel
2. Set environment variables
3. Deploy on push to main branch

### Deploy Services

1. **Qdrant**: Use Qdrant Cloud or self-hosted
2. **MCP Server**: Deploy to Railway/Heroku
3. **Database**: Neon PostgreSQL

## Common Issues

### Port Already in Use
```bash
# Find process using port 3000
lsof -ti:3000
# Kill it
kill -9 $(lsof -ti:3000)
```

### Docker Issues
```bash
# Reset Docker
docker system prune -a
```

### MCP Server Not Responding
1. Check the server is running: `npm run start:mcp`
2. Verify environment variables
3. Check server logs

### RAG Not Working
1. Ensure content is ingested: `npm run ingest:content`
2. Check Qdrant connection
3. Verify OpenAI API key

## Development Tools

### VS Code Extensions
- ES7+ React/Redux/React-Native snippets
- Prettier - Code formatter
- ESLint
- Markdown All in One
- Mermaid Preview

### Browser Extensions
- React Developer Tools
- Redux DevTools

### Debugging
```bash
# Debug Docusaurus
DEBUG=docusaurus:* npm run start

# Debug MCP Server
DEBUG=mcp:* npm run start:mcp
```

## Contributing

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes
3. Run tests: `npm run test`
4. Commit: `git commit -m "feat: add new feature"`
5. Push: `git push origin feature/new-feature`
6. Create pull request

## Getting Help

- Documentation: https://ai-textbook-docs.example
- Issues: https://github.com/your-org/ai-physical-textbook/issues
- Discord: https://discord.gg/ai-textbook

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   AI Services   │
│   (Docusaurus)  │◄──►│   (FastAPI)     │◄──►│   (OpenAI)      │
│                 │    │                 │    │                 │
│ - React SPA     │    │ - REST API      │    │ - ChatGPT       │
│ - MDX Content   │    │ - Auth          │    │ - Embeddings    │
│ - WebAssembly   │    │ - Progress      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CDN           │    │   PostgreSQL    │    │   Qdrant        │
│   (Vercel)      │    │   (Neon)        │    │   (Vector DB)   │
│                 │    │                 │    │                 │
│ - Static Assets │    │ - User Data     │    │ - Embeddings    │
│ - Edge Cache    │    │ - Progress      │    │ - Search Index  │
│ - Global CDN    │    │ - Sessions      │    │ - RAG Storage   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Performance Tips

1. **Images**: Use WebP format with proper dimensions
2. **Code Blocks**: Lazy load heavy syntax highlighting
3. **Simulations**: Use streaming for large data
4. **Caching**: Implement edge caching for static content
5. **Bundle Size**: Regularly audit with `npm run analyze`

## Security Best Practices

1. Never commit API keys
2. Use environment variables for secrets
3. Implement rate limiting
4. Sanitize user inputs
5. Keep dependencies updated

## Monitoring

### Local Development
```bash
# Monitor bundle size
npm run analyze

# Check performance
npm run lighthouse
```

### Production
- Monitor Core Web Vitals
- Track error rates
- Watch API response times
- Monitor database performance