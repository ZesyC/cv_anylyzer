# Docker Deployment Guide

## Quick Start

### Prerequisites

- Docker installed (>= 20.10)
- Docker Compose installed (>= 2.0)

### Run with Docker Compose

```bash
# 1. Clone the repository
cd cv-analyzer

# 2. (Optional) Set up Gemini API key
cp .env.docker.example .env
# Edit .env and add your API key

# 3. Start all services
docker-compose up

# 4. Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
```

That's it! 🎉

---

## Detailed Setup

### 1. Environment Configuration

Create `.env` file from template:

```bash
cp .env.docker.example .env
```

Edit `.env` and configure:

```env
# Add your Gemini API key (or leave as "API key" to use mock data)
GEMINI_API_KEY=AIzaSy_your_actual_key_here
GEMINI_MODEL=gemini-1.5-flash
```

### 2. Build Images

```bash
# Build both frontend and backend
docker-compose build

# Or build individually
docker-compose build backend
docker-compose build frontend
```

### 3. Run Services

**Development mode** (with hot reload):

```bash
docker-compose up
```

**Production mode** (detached):

```bash
docker-compose up -d
```

**View logs**:

```bash
docker-compose logs -f
docker-compose logs -f backend  # Backend only
docker-compose logs -f frontend # Frontend only
```

### 4. Stop Services

```bash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## Docker Commands Reference

### Container Management

```bash
# List running containers
docker-compose ps

# Restart a service
docker-compose restart backend

# Execute command in container
docker-compose exec backend python -m pytest

# View container resource usage
docker stats
```

### Image Management

```bash
# List images
docker images | grep cv-analyzer

# Remove unused images
docker image prune

# Rebuild without cache
docker-compose build --no-cache
```

### Logs & Debugging

```bash
# Follow logs
docker-compose logs -f --tail=100

# Check container health
docker-compose ps

# Inspect a container
docker inspect cv-analyzer-backend
```

---

## Development vs Production

### Development Mode

- **Hot reload enabled** for backend (volume mount)
- **Source maps** available
- **Verbose logging**

Current docker-compose.yml is configured for development.

### Production Mode

For production, modify `docker-compose.yml`:

1. **Remove volume mounts** (no hot reload needed):

   ```yaml
   # Comment out or remove:
   # volumes:
   #   - ./backend/app:/app/app
   ```

2. **Add resource limits**:

   ```yaml
   services:
     backend:
       deploy:
         resources:
           limits:
             cpus: "1"
             memory: 1G
   ```

3. **Use environment file**:
   ```bash
   docker-compose --env-file .env.production up -d
   ```

---

## Deployment Options

### Option 1: Docker Hub

```bash
# Tag images
docker tag cv-analyzer-backend:latest username/cv-analyzer-backend:v1.0
docker tag cv-analyzer-frontend:latest username/cv-analyzer-frontend:v1.0

# Push to Docker Hub
docker push username/cv-analyzer-backend:v1.0
docker push username/cv-analyzer-frontend:v1.0

# Pull and run on server
docker pull username/cv-analyzer-backend:v1.0
docker-compose up -d
```

### Option 2: Cloud Platforms

**AWS ECS/Fargate:**

- Upload images to ECR
- Create task definitions
- Deploy with ECS service

**Google Cloud Run:**

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/cv-analyzer-backend
gcloud run deploy --image gcr.io/PROJECT_ID/cv-analyzer-backend
```

**DigitalOcean App Platform:**

- Connect GitHub repository
- Auto-detect Dockerfile
- Deploy with one click

### Option 3: VPS Deployment

```bash
# 1. Copy files to VPS
scp -r . user@your-server:/opt/cv-analyzer

# 2. SSH to server
ssh user@your-server

# 3. Run docker-compose
cd /opt/cv-analyzer
docker-compose up -d

# 4. (Optional) Setup nginx reverse proxy with SSL
# See nginx example below
```

---

## Nginx Reverse Proxy (Optional)

If deploying to VPS with domain name:

```nginx
# /etc/nginx/sites-available/cv-analyzer.conf
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
    }
}
```

Add SSL with Let's Encrypt:

```bash
sudo certbot --nginx -d your-domain.com
```

---

## Troubleshooting

### Port already in use

```bash
# Find process using port
lsof -i :8000
lsof -i :5173

# Kill process or change port in docker-compose.yml
ports:
  - "8001:8000"  # Use different host port
```

### Backend not connecting

```bash
# Check backend logs
docker-compose logs backend

# Verify network
docker network inspect cv-analyzer_cv-analyzer-network

# Test backend directly
curl http://localhost:8000/
```

### Frontend build fails

```bash
# Check Node version in Dockerfile
# Increase Node memory if needed
docker-compose build --no-cache frontend
```

### Cannot connect to Docker daemon

```bash
# Start Docker service
sudo systemctl start docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

---

## Health Checks

Both services include health checks:

**Backend:** Checks HTTP endpoint `/`
**Frontend:** Checks nginx availability

View health status:

```bash
docker-compose ps
# Should show "healthy" in STATUS column
```

---

## Monitoring & Logging

### View Resource Usage

```bash
docker stats cv-analyzer-backend cv-analyzer-frontend
```

### Centralized Logging

Consider adding logging drivers:

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## Security Best Practices

1. **Never commit .env file** (already in .gitignore)
2. **Use secrets management** for production
3. **Run as non-root user** in containers
4. **Keep images updated**: `docker-compose pull`
5. **Scan for vulnerabilities**: `docker scan cv-analyzer-backend`

---

## Performance Optimization

### Multi-stage Builds

Already implemented for frontend - reduces image size significantly.

### Layer Caching

Dockerfile layers are optimized for caching:

- Dependencies copied first
- Source code copied last
- Rebuilds are faster

### Image Sizes

- Backend: ~200-300 MB (python:3.9-slim)
- Frontend: ~20-30 MB (nginx:alpine)

---

## FAQ

**Q: Can I use mock data without Gemini API?**
A: Yes! Leave `GEMINI_API_KEY=API key` in .env

**Q: How to update code without rebuilding?**
A: Backend has volume mount for hot reload in dev mode

**Q: How to scale services?**
A: Use `docker-compose up --scale backend=3`

**Q: Where are uploaded files stored?**
A: Currently in-memory. Add volume to persist:

```yaml
volumes:
  - cv-uploads:/app/uploads
```

---

Để biết thêm chi tiết, xem [README.md](README.md) và [GEMINI_SETUP.md](GEMINI_SETUP.md)
