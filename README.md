# CV Analyzer

<div align="center">

**AI-Powered Resume Analysis Platform**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

_Transform your resume with AI-driven insights and actionable recommendations_

[Features](#-key-features) •
[Quick Start](#-quick-start) •
[Documentation](#-documentation) •
[API Reference](#-api-reference) •
[Contributing](#-contributing)

</div>

---

## 📋 Overview

CV Analyzer is a production-ready full-stack application that leverages Google's Gemini AI to provide intelligent resume analysis. The platform identifies keyword gaps, detects missing sections, and delivers contextual improvement suggestions by comparing resumes against job descriptions.

### Why CV Analyzer?

- **🎯 Targeted Feedback**: Get specific, actionable suggestions tailored to your target role
- **🔍 Keyword Optimization**: Identify missing keywords that ATS systems look for
- **📊 Section Analysis**: Ensure your resume has all critical components
- **✨ AI-Powered**: Powered by Google Gemini for contextual, intelligent recommendations
- **🚀 Production-Ready**: Fully Dockerized with comprehensive configuration options
- **🌐 Multilingual**: Supports English and Vietnamese analysis

---

## ✨ Key Features

### Core Capabilities

| Feature                           | Description                                                                            |
| --------------------------------- | -------------------------------------------------------------------------------------- |
| **Multi-format Support**          | Process PDF and DOCX resume formats seamlessly                                         |
| **Intelligent Section Detection** | Automatically identifies Summary, Skills, Experience, Projects, and Education sections |
| **Keyword Analysis**              | Compares resume against job descriptions to identify gaps                              |
| **AI-Powered Insights**           | Delivers contextual improvement suggestions using Google Gemini AI                     |
| **Content Enhancement**           | Provides before/after examples for strengthening bullet points                         |
| **Graceful Degradation**          | Automatic fallback to mock data when API is unavailable                                |

### Technical Highlights

- **Modern Tech Stack**: React 18 + TypeScript + TailwindCSS + FastAPI
- **Type-Safe Development**: Full TypeScript and Python type hints coverage
- **Optimized Performance**: Async processing, code splitting, and efficient extraction pipeline
- **Container-Ready**: Docker Compose orchestration for development and production
- **Comprehensive Documentation**: Detailed guides for development, deployment, and API usage

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  React 18 + TypeScript + Vite + TailwindCSS                 │
│  • Component-based architecture                             │
│  • Axios HTTP client with interceptors                      │
│  • Type-safe API communication                              │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST API
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                          Backend                             │
│  FastAPI + Python 3.8+ (Async)                              │
│  • RESTful API endpoints                                    │
│  • Pydantic data validation                                 │
│  • CORS middleware                                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   ┌──────────┐ ┌──────────┐ ┌──────────────┐
   │   PDF    │ │   DOCX   │ │   Google     │
   │ Extractor│ │ Extractor│ │  Gemini AI   │
   │(pdfplumber)│(python-docx)│(gemini-1.5-*) │
   └──────────┘ └──────────┘ └──────────────┘
```

### Technology Stack

#### Backend

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance async web framework
- **Document Processing**:
  - `pdfplumber` - PDF text extraction
  - `python-docx` - DOCX document processing
- **AI Integration**: Google Generative AI (Gemini 1.5 Flash/Pro)
- **Configuration**: `python-dotenv` for environment management
- **Validation**: Pydantic v2 for data validation

#### Frontend

- **Framework**: [React 18](https://react.dev/) with TypeScript
- **Build Tool**: [Vite](https://vitejs.dev/) - Next-generation frontend tooling
- **Styling**: [TailwindCSS](https://tailwindcss.com/) - Utility-first CSS framework
- **HTTP Client**: [Axios](https://axios-http.com/) with interceptors
- **Type Safety**: Full TypeScript coverage with strict mode

#### DevOps

- **Containerization**: Docker + Docker Compose
- **Web Server**: Uvicorn (ASGI) with Nginx for production
- **Development**: Hot reload for both frontend and backend

---

## 📁 Project Structure

```
cv-analyzer/
├── backend/                    # FastAPI backend service
│   ├── app/
│   │   ├── main.py            # Application entry point & routes
│   │   ├── models.py          # Pydantic data models
│   │   ├── config.py          # Configuration management
│   │   └── services/
│   │       ├── cv_extraction.py   # Document text extraction
│   │       ├── cv_analysis.py     # Rule-based analysis engine
│   │       └── llm_client.py      # Gemini AI integration
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend container definition
│   └── .env.example          # Environment variables template
│
├── frontend/                  # React TypeScript frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── FileUploadForm.tsx
│   │   │   ├── AnalysisResult.tsx
│   │   │   ├── SectionChecklist.tsx
│   │   │   ├── KeywordMatchList.tsx
│   │   │   └── SuggestionCard.tsx
│   │   ├── services/
│   │   │   └── apiClient.ts  # Axios API client
│   │   ├── types/
│   │   │   └── api.ts        # TypeScript type definitions
│   │   ├── App.tsx           # Main application component
│   │   ├── main.tsx          # Application entry point
│   │   └── index.css         # Global styles
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── docs/                      # Documentation
│   ├── development.md        # Development guide
│   ├── docker-deployment.md  # Deployment guide
│   ├── gemini-setup.md       # Gemini API setup
│   ├── api-reference.md      # API documentation
│   └── architecture.md       # Architecture details
│
├── scripts/
│   └── setup.sh              # Automated setup script
│
├── docker-compose.yml        # Multi-container orchestration
├── .env.docker.example       # Docker environment template
├── CONTRIBUTING.md           # Contribution guidelines
└── LICENSE                   # MIT License
```

---

## 🚀 Quick Start

### Prerequisites

| Requirement           | Version | Notes                                                  |
| --------------------- | ------- | ------------------------------------------------------ |
| **Python**            | 3.8+    | with pip                                               |
| **Node.js**           | 16+     | with npm                                               |
| **Gemini API Key**    | -       | [Get free key](https://aistudio.google.com/app/apikey) |
| **Docker** (optional) | 20.10+  | For containerized deployment                           |

### Option 1: Docker Compose (Recommended)

**Fastest way to get started:**

```bash
# 1. Clone the repository
git clone <repository-url>
cd cv-analyzer

# 2. Configure environment
cp .env.docker.example .env
# Edit .env and add your Gemini API key

# 3. Start all services
docker-compose up

# ✅ Application ready!
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

<details>
<summary><b>Click to expand local setup instructions</b></summary>

#### Backend Setup

```bash
# 1. Navigate to backend directory
cd cv-analyzer/backend

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add:
# GEMINI_API_KEY=your_api_key_here
# GEMINI_MODEL=gemini-1.5-flash

# 5. Start backend server
uvicorn app.main:app --reload

# ✅ Backend running at http://localhost:8000
```

#### Frontend Setup

```bash
# 1. Navigate to frontend directory (new terminal)
cd cv-analyzer/frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev

# ✅ Frontend running at http://localhost:5173
```

</details>

### Automated Setup

```bash
# Run automated setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This script will:

- ✅ Verify system prerequisites
- ✅ Create Python virtual environment
- ✅ Install all dependencies (backend & frontend)
- ✅ Set up environment files

---

## 📖 Documentation

Comprehensive documentation is available in the `/docs` directory:

| Document                                       | Description                                            |
| ---------------------------------------------- | ------------------------------------------------------ |
| [Development Guide](docs/development.md)       | Local development setup, coding standards, testing     |
| [Docker Deployment](docs/docker-deployment.md) | Container deployment strategies (AWS, GCP, Azure, VPS) |
| [Gemini API Setup](docs/gemini-setup.md)       | Detailed Gemini API configuration and troubleshooting  |
| [API Reference](docs/api-reference.md)         | Complete API endpoint documentation                    |
| [Architecture](docs/architecture.md)           | System architecture and design decisions               |
| [Contributing](CONTRIBUTING.md)                | Contribution guidelines and workflow                   |

---

## 🎯 Usage Guide

### Basic Workflow

1. **Upload Resume**

   - Drag & drop or browse for your resume file
   - Supported formats: PDF, DOCX (max 10 MB)

2. **Add Job Description** (Optional)

   - Paste target job description
   - Enables keyword matching analysis

3. **Analyze**

   - Click "Analyze CV"
   - Processing typically takes 2-5 seconds

4. **Review Results**

   - Overall summary and assessment
   - Strengths & weaknesses analysis
   - Section completeness checklist
   - Keyword gap analysis (if JD provided)
   - Targeted improvement suggestions
   - Enhanced bullet point examples

5. **Iterate**
   - Apply suggestions to your resume
   - Re-analyze to track improvements

### Example Analysis Output

<details>
<summary><b>View sample analysis response</b></summary>

```json
{
  "overall_summary": "Your resume demonstrates strong technical skills but could benefit from quantified achievements and a professional summary.",
  "strengths": [
    "Clear technical skills section with relevant technologies",
    "Well-structured experience section",
    "Consistent formatting throughout"
  ],
  "weaknesses": [
    "Missing professional summary/objective",
    "Limited quantification of achievements",
    "Projects section could use more detail"
  ],
  "section_checklist": {
    "has_summary": false,
    "has_skills": true,
    "has_experience": true,
    "has_projects": true,
    "has_education": true
  },
  "jd_analysis": {
    "jd_keywords": ["python", "fastapi", "docker", "kubernetes", "aws"],
    "matched_keywords": ["python", "docker"],
    "missing_keywords": ["fastapi", "kubernetes", "aws"]
  },
  "suggestions_by_section": [
    {
      "section_name": "Summary",
      "issues": ["Professional summary is missing"],
      "suggestions": [
        "Add a 2-3 sentence summary highlighting your key skills and career objectives"
      ]
    },
    {
      "section_name": "Experience",
      "issues": ["Achievements lack quantification"],
      "suggestions": [
        "Add metrics and numbers to demonstrate impact (e.g., 'Reduced API latency by 40%')"
      ]
    }
  ],
  "rewritten_examples": [
    {
      "original": "Developed backend services",
      "improved": "Architected and deployed 5 microservices using FastAPI and Docker, processing 10K+ daily requests with 99.9% uptime",
      "section": "Experience"
    }
  ]
}
```

</details>

---

## 🔌 API Reference

### Endpoints

#### `POST /api/analyze-cv`

Analyzes a resume and returns structured improvement suggestions.

**Request:**

```bash
curl -X POST "http://localhost:8000/api/analyze-cv" \
  -H "Content-Type: multipart/form-data" \
  -F "cv_file=@resume.pdf" \
  -F "jd_text=Seeking Python developer with FastAPI and Docker experience" \
  -F "language=en"
```

**Parameters:**

| Parameter  | Type   | Required | Description                                     |
| ---------- | ------ | -------- | ----------------------------------------------- |
| `cv_file`  | File   | ✅ Yes   | Resume file (PDF or DOCX, max 10MB)             |
| `jd_text`  | String | ❌ No    | Job description for keyword analysis            |
| `language` | String | ❌ No    | Analysis language (`en` or `vi`, default: `en`) |

**Response:** `CVAnalysisResponse` (See [API Reference](docs/api-reference.md) for complete schema)

#### `GET /`

Health check endpoint.

**Response:**

```json
{
  "message": "CV Analyzer API is running",
  "version": "1.0.0",
  "endpoints": {
    "analyze": "/api/analyze-cv"
  }
}
```

### Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔧 Configuration

### Environment Variables

#### Backend Configuration `.env`

```bash
# Gemini API Configuration
GEMINI_API_KEY=your_api_key_here          # Required: Get from https://aistudio.google.com/app/apikey
GEMINI_MODEL=gemini-1.5-flash             # Model: gemini-1.5-flash or gemini-1.5-pro
GEMINI_MAX_TOKENS=2000                    # Max tokens per request
GEMINI_TEMPERATURE=0.7                    # Response creativity (0.0-1.0)

# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true                               # Enable auto-reload in development

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# File Upload Limits
MAX_FILE_SIZE_MB=10                       # Maximum upload size in MB
```

#### Frontend Configuration `.env.local`

```bash
# API Configuration
VITE_API_URL=http://localhost:8000        # Backend API URL

# Feature Flags (optional)
VITE_ENABLE_ANALYTICS=false
```

### Gemini API Setup

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (format: `AIzaSy...`)
5. Add to `.env` file

**Model Options:**

| Model              | Requests/min | Tokens/min | Use Case                                 |
| ------------------ | ------------ | ---------- | ---------------------------------------- |
| `gemini-1.5-flash` | 15           | 1M         | Development, fast analysis (recommended) |
| `gemini-1.5-pro`   | 2            | 32K        | Higher quality, detailed analysis        |

> **Note**: The system automatically falls back to mock data if the API is unavailable or rate-limited.

See [Gemini Setup Guide](docs/gemini-setup.md) for detailed instructions.

---

## 🚢 Production Deployment

### Docker Compose (Recommended)

```bash
# Build and run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Scale backend for high availability
docker-compose up -d --scale backend=3

# Stop services
docker-compose down
```

### Manual Production Build

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend

```bash
cd frontend
npm run build  # Output: dist/
npm run preview  # Preview production build locally

# Serve with nginx, Apache, or any static file server
```

### Deployment Platforms

See [Docker Deployment Guide](docs/docker-deployment.md) for detailed instructions on:

- ☁️ **Cloud Platforms**: AWS (ECS/Fargate), Google Cloud Run, Azure Container Instances
- 📦 **Container Registries**: Docker Hub, AWS ECR, Google Container Registry
- 🎯 **Platform-as-a-Service**: Heroku, DigitalOcean App Platform, Railway
- 🖥️ **VPS Deployment**: Setup with nginx reverse proxy and SSL
- 🔄 **CI/CD Integration**: GitHub Actions, GitLab CI, Jenkins

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest

# With coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_services/test_extraction.py -v
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Watch mode
npm test -- --watch

# With coverage
npm test -- --coverage
```

### Manual Integration Testing

```bash
# Test API endpoint with sample CV
curl -X POST "http://localhost:8000/api/analyze-cv" \
  -F "cv_file=@/path/to/sample_cv.pdf" \
  -F "jd_text=Seeking Python developer with FastAPI and Docker experience"
```

---

## 🐛 Troubleshooting

### Common Issues

<details>
<summary><b>Backend won't start</b></summary>

**Symptoms**: Server fails to start or crashes immediately

**Solutions**:

```bash
# 1. Check Python version
python --version  # Should be 3.8+

# 2. Verify virtual environment is activated
which python  # Should point to venv

# 3. Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# 4. Check if port 8000 is in use
lsof -i :8000  # macOS/Linux
# Kill process if needed: kill -9 <PID>

# 5. Verify .env file exists and has correct format
cat .env
```

</details>

<details>
<summary><b>Frontend can't connect to backend</b></summary>

**Symptoms**: Network errors, CORS issues

**Solutions**:

```bash
# 1. Verify backend is running
curl http://localhost:8000/

# 2. Check CORS configuration in backend/app/main.py
# Ensure your frontend URL is in allowed_origins

# 3. Verify API URL in frontend
# Check .env.local has: VITE_API_URL=http://localhost:8000

# 4. Check browser console for specific error messages
```

</details>

<details>
<summary><b>Gemini API authentication errors</b></summary>

**Symptoms**: "Invalid API key" or "Authentication failed"

**Solutions**:

```bash
# 1. Verify API key format (should start with AIzaSy)
echo $GEMINI_API_KEY

# 2. Check for whitespace or newlines
# API key should be on single line with no spaces

# 3. Ensure API key is enabled in Google AI Studio
# Visit: https://aistudio.google.com/app/apikey

# 4. Check logs for specific error messages
docker-compose logs backend  # Docker
# or check terminal output for local development
```

</details>

<details>
<summary><b>Rate limiting / API quota exceeded</b></summary>

**Symptoms**: "429 Too Many Requests" or quota errors

**Solutions**:

- **Gemini 1.5 Flash**: 15 requests/minute, 1,500 requests/day
- **Gemini 1.5 Pro**: 2 requests/minute
- Wait 60 seconds before retrying
- System automatically falls back to mock data
- Consider implementing client-side request throttling

</details>

<details>
<summary><b>Docker container issues</b></summary>

**Symptoms**: Containers fail to start or crash

**Solutions**:

```bash
# 1. Check Docker daemon is running
docker ps

# 2. Verify .env file exists in project root
ls -la .env

# 3. View container logs
docker-compose logs backend
docker-compose logs frontend

# 4. Rebuild containers
docker-compose down
docker-compose up --build

# 5. Check port availability
lsof -i :8000  # Backend
lsof -i :5173  # Frontend
```

</details>

### Getting Help

- 📚 **Documentation**: Check [docs/](docs/) for detailed guides
- 🐛 **Issues**: [Search existing issues](../../issues) or create a new one
- 💬 **Discussions**: Use GitHub Discussions for questions
- 📧 **Contact**: Reach out to maintainers

---

## 🗺️ Roadmap

### Planned Features

- [ ] 🔐 User authentication and session management
- [ ] 📊 Resume version history and comparison
- [ ] 📄 PDF export of analysis results
- [ ] 📝 Additional file format support (RTF, TXT)
- [ ] 📚 Resume templates and examples library
- [ ] 🎯 ATS (Applicant Tracking System) compatibility scoring
- [ ] 🏢 Industry-specific analysis models
- [ ] 👥 Team collaboration features
- [ ] 📈 Usage analytics and insights dashboard
- [ ] ⚡ Enhanced caching strategies
- [ ] 🌍 Additional language support
- [ ] 🔗 Integration with LinkedIn and job boards

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Contribution Guide

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow [coding standards](docs/development.md#coding-standards)
   - Add tests for new functionality
   - Update documentation
4. **Commit with conventional format**
   ```bash
   git commit -m "feat: add keyword extraction feature"
   ```
5. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Development Resources

- [Development Guide](docs/development.md) - Setup, coding standards, workflow
- [Architecture Guide](docs/architecture.md) - System design and technical decisions
- [API Reference](docs/api-reference.md) - Complete API documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Commercial Use**: Free for personal and commercial use under MIT License terms.

---

## 🙏 Acknowledgments

Built with modern web technologies and best practices. Special thanks to:

- **Open Source Community**: For excellent tools and libraries
- **Google**: For the Gemini AI API
- **FastAPI**: For the amazing Python web framework
- **React Team**: For the powerful UI library
- **Contributors**: Everyone who has contributed to this project

---

## 📞 Contact & Support

- **Maintainer**: Zesy Callisto
- **Version**: 1.0.0
- **Last Updated**: November 2025
- **Repository**: [GitHub Repository](#)
- **Issues**: [Report Bug](../../issues/new?template=bug_report.md)
- **Feature Requests**: [Request Feature](../../issues/new?template=feature_request.md)

---

<div align="center">

**[⬆ back to top](#cv-analyzer)**
   
Made with ❤️ by the Zesy Callisto

</div>
