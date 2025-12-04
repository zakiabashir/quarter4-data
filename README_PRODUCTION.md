# AI Physical AI Textbook - Production Deployment Guide

## Overview

This guide provides complete instructions for deploying the AI-Native Physical AI Textbook in a production environment. The application consists of multiple microservices working together to provide an interactive learning experience.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend       │    │      API         │    │  MCP/RAG Server  │
│  (Docusaurus)    │◄──►│   (FastAPI)      │◄──►│   (Node.js)      │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 3001    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│     Nginx        │    │   PostgreSQL     │    │     Redis       │
│   (Reverse       │    │   (Database)     │    │    (Cache)      │
│    Proxy)        │    │   Port: 5432    │    │   Port: 6379    │
│   Port: 80/443   │    └──────────────────┘    └─────────────────┘
└─────────────────┘             │                       │
                                ▼                       ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │    Qdrant        │    │   File Storage  │
                       │ (Vector Store)   │    │   (Uploads)     │
                       │   Port: 6333     │    │                 │
                       └──────────────────┘    └─────────────────┘
```

## Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu 20.04+ recommended), macOS, or Windows with WSL2
- **RAM**: Minimum 8GB, recommended 16GB
- **Storage**: Minimum 50GB free space
- **CPU**: 4+ cores recommended

### Software Requirements
- **Docker**: Version 20.10+
- **Docker Compose**: Version 2.0+
- **Git**: For cloning the repository
- **OpenSSL**: For generating SSL certificates (optional)

### Optional Services
- **Domain Name**: For HTTPS configuration
- **SSL Certificate**: For secure HTTPS (Let's Encrypt recommended)
- **OpenAI API Key**: For enhanced AI responses

## Quick Deployment

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/ai-physical-textbook.git
cd ai-physical-textbook
```

### 2. Configure Environment Variables
```bash
# Copy environment template
cp .env.production.example .env

# Edit the configuration
nano .env
```

### 3. Deploy with Docker Compose
```bash
# Make the deployment script executable
chmod +x scripts/deploy.sh

# Run the deployment
./scripts/deploy.sh
```

### 4. Access the Application
- **Frontend**: http://localhost (or your domain)
- **API Documentation**: http://localhost/api/docs
- **MCP Server**: http://localhost/mcp/health

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Database Configuration
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://ai_textbook:your_password@postgres:5432/ai_textbook_prod

# Security
SECRET_KEY=your_super_secret_key_change_in_production

# OpenAI Configuration (Optional)
OPENAI_API_KEY=your_openai_api_key_here

# Domain Configuration
DOMAIN=your-domain.com

# Environment
ENVIRONMENT=production
```

### SSL/HTTPS Configuration

1. **Obtain SSL Certificate** (Let's Encrypt example):
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

2. **Update Nginx Configuration**:
```bash
# Edit nginx configuration
nano nginx/nginx.conf
```

## Manual Deployment Steps

### 1. Build and Start Services

```bash
# Build all services
docker-compose build

# Start services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f
```

### 2. Initialize Database

```bash
# Run database initialization
docker-compose exec api python scripts/init_db.py

# Create additional users (optional)
docker-compose exec api python -c "
from src.database import get_db
from src.models.user import User
from src.core.security import get_password_hash

db = next(get_db())
user = User(
    email='admin@example.com',
    username='admin',
    full_name='Administrator',
    hashed_password=get_password_hash('admin_password'),
    role='admin',
    is_active=True
)
db.add(user)
db.commit()
"
```

### 3. Verify Deployment

```bash
# Check all services
docker-compose ps

# Check API health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000

# Check MCP server
curl http://localhost:3001/health
```

## Service Management

### Viewing Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f frontend
docker-compose logs -f mcp-server
```

### Updating the Application
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

### Backup and Restore

#### Database Backup
```bash
# Create backup
docker-compose exec postgres pg_dump -U ai_textbook ai_textbook_prod > backup.sql

# Restore from backup
docker-compose exec -T postgres psql -U ai_textbook ai_textbook_prod < backup.sql
```

#### File Storage Backup
```bash
# Backup uploads
tar -czf uploads_backup.tar.gz uploads/

# Restore uploads
tar -xzf uploads_backup.tar.gz
```

## Scaling and Performance

### Horizontal Scaling
```yaml
# Update docker-compose.yml
services:
  api:
    replicas: 3  # Scale API to 3 instances

  frontend:
    replicas: 2  # Scale frontend to 2 instances
```

### Performance Optimization

1. **Database Optimization**:
   - Configure connection pooling
   - Add database indexes
   - Enable query caching

2. **Redis Caching**:
   - Cache API responses
   - Store session data
   - Cache frequently accessed content

3. **CDN Configuration**:
   - Serve static assets via CDN
   - Enable Gzip compression
   - Implement browser caching

## Monitoring

### Health Checks
All services include health check endpoints:
- API: `/health`
- MCP Server: `/health`
- Frontend: Returns 200 OK

### Metrics Collection
```bash
# Install monitoring tools
docker run -d \
  --name=prometheus \
  -p 9090:9090 \
  prom/prometheus

docker run -d \
  --name=grafana \
  -p 3001:3000 \
  grafana/grafana
```

### Logging
```yaml
# Add to docker-compose.yml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## Security Considerations

### Network Security
```yaml
# Network isolation in docker-compose.yml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
  database:
    driver: bridge
    internal: true
```

### Environment Security
- Use strong passwords
- Rotate secrets regularly
- Enable HTTPS in production
- Implement rate limiting
- Set up firewalls

### Application Security
- Validate all inputs
- Use parameterized queries
- Implement CSRF protection
- Secure file uploads
- Enable security headers

## Troubleshooting

### Common Issues

1. **Port Conflicts**:
   ```bash
   # Check port usage
   netstat -tulpn | grep :8000

   # Kill conflicting processes
   sudo kill -9 <PID>
   ```

2. **Database Connection Issues**:
   ```bash
   # Check database logs
   docker-compose logs postgres

   # Test connection
   docker-compose exec api python -c "
   from src.database import engine
   try:
       engine.connect()
       print('Database connected successfully')
   except Exception as e:
       print(f'Database error: {e}')
   "
   ```

3. **Memory Issues**:
   ```bash
   # Check memory usage
   docker stats

   # Increase swap space
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

### Debug Mode
```bash
# Run services with debug logging
docker-compose -f docker-compose.debug.yml up
```

## Support

### Documentation
- [API Documentation](http://localhost/api/docs)
- [Developer Guide](./DEVELOPER.md)
- [User Manual](./docs/user-guide.md)

### Getting Help
- GitHub Issues: [Create an issue](https://github.com/your-org/ai-physical-textbook/issues)
- Email: support@your-domain.com
- Discord: [Join our community](https://discord.gg/your-invite)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.