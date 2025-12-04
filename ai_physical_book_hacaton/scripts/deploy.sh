#!/bin/bash

# AI Physical AI Textbook Deployment Script
# This script sets up and deploys the entire application stack

set -e  # Exit on any error

echo "🚀 Starting AI Physical AI Textbook deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="ai_textbook"
DOMAIN=${DOMAIN:-"localhost"}
ENVIRONMENT=${ENVIRONMENT:-"production"}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Create necessary directories
echo -e "${YELLOW}📁 Creating necessary directories...${NC}"
mkdir -p logs/nginx
mkdir -p nginx/ssl
mkdir -p uploads
mkdir -p vector_store

# Generate secure password if not set
if [ -z "$POSTGRES_PASSWORD" ]; then
    POSTGRES_PASSWORD=$(openssl rand -base64 32)
    echo -e "${YELLOW}🔐 Generated PostgreSQL password${NC}"
fi

# Generate secret key if not set
if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(openssl rand -hex 32)
    echo -e "${YELLOW}🔐 Generated application secret key${NC}"
fi

# Create environment file
cat > .env << EOF
# Database Configuration
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
DATABASE_URL=postgresql://ai_textbook:${POSTGRES_PASSWORD}@postgres:5432/ai_textbook_prod

# Security
SECRET_KEY=${SECRET_KEY}

# OpenAI Configuration (Optional)
OPENAI_API_KEY=${OPENAI_API_KEY:-}

# Domain Configuration
DOMAIN=${DOMAIN}

# Environment
ENVIRONMENT=${ENVIRONMENT}
EOF

echo -e "${GREEN}✅ Environment file created${NC}"

# Stop any existing containers
echo -e "${YELLOW}🛑 Stopping existing containers...${NC}"
docker-compose down

# Build and start services
echo -e "${YELLOW}🔨 Building and starting services...${NC}"
docker-compose up --build -d

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
sleep 30

# Initialize database
echo -e "${YELLOW}💾 Initializing database...${NC}"
docker-compose exec api python scripts/init_db.py

# Check service health
echo -e "${YELLOW}🏥 Checking service health...${NC}"

# Check API health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API service is healthy${NC}"
else
    echo -e "${RED}❌ API service is not responding${NC}"
fi

# Check MCP server health
if curl -f http://localhost:3001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ MCP server is healthy${NC}"
else
    echo -e "${RED}❌ MCP server is not responding${NC}"
fi

# Check frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is running${NC}"
else
    echo -e "${RED}❌ Frontend is not responding${NC}"
fi

# Display access information
echo -e "\n${GREEN}🎉 Deployment completed successfully!${NC}\n"
echo -e "${YELLOW}📋 Access Information:${NC}"
echo -e "  Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "  API Documentation: ${GREEN}http://localhost:8000/docs${NC}"
echo -e "  MCP Server: ${GREEN}http://localhost:3001${NC}"
echo -e "  Nginx Proxy: ${GREEN}http://localhost${NC}\n"

echo -e "${YELLOW}👤 Demo Credentials:${NC}"
echo -e "  Email: ${GREEN}student@example.com${NC}"
echo -e "  Password: ${GREEN}password123${NC}\n"

echo -e "${YELLOW}🔧 Management Commands:${NC}"
echo -e "  View logs: ${GREEN}docker-compose logs -f [service_name]${NC}"
echo -e "  Stop services: ${GREEN}docker-compose down${NC}"
echo -e "  Restart services: ${GREEN}docker-compose restart${NC}"
echo -e "  Update code: ${GREEN}docker-compose up --build -d${NC}\n"

# Show running containers
echo -e "${YELLOW}📦 Running Containers:${NC}"
docker-compose ps

echo -e "\n${GREEN}✨ Happy teaching and learning with AI Physical AI Textbook! ✨${NC}"