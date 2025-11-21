# CV Analyzer - AI-Powered Resume Analysis Platform

A production-ready full-stack web application that leverages AI to analyze resumes and provide actionable improvement suggestions. The platform compares CVs against job descriptions to identify keyword gaps and optimize application materials.

## Key Features

- **Multi-format Support**: Processes PDF and DOCX resume formats
- **Intelligent Section Detection**: Automatically identifies key resume sections (Summary, Skills, Experience, Projects, Education)
- **Keyword Analysis**: Performs comparative analysis between resumes and job descriptions
- **AI-Powered Insights**: Delivers detailed, contextual improvement suggestions using Google Gemini AI
- **Content Enhancement**: Provides before/after examples for strengthening bullet points
- **Modern Tech Stack**: Built with React, TypeScript, and TailwindCSS for optimal performance
- **Efficient Processing**: Optimized text extraction and analysis pipeline
- **Multilingual AI Support**: Gemini API integration with Vietnamese language support
- **Production-Ready**: Docker containerization with comprehensive configuration options

## Architecture Overview

### Backend Stack

- **Framework**: FastAPI with async support for high-performance API endpoints
- **Document Processing**:
  - PDF extraction via `pdfplumber`
  - DOCX extraction via `python-docx`
- **Analysis Engine**:
  - Rule-based section detection and metrics calculation
  - Google Gemini AI integration for intelligent analysis
  - Automatic fallback to mock data when API is unavailable
- **Configuration**: Environment-based configuration with `.env` support

### Frontend Stack

- **Framework**: React 18 with TypeScript for type-safe development
- **Build Tool**: Vite for fast HMR and optimized production builds
- **Styling**: TailwindCSS with custom design system
- **HTTP Client**: Axios with interceptors for API communication
- **Architecture**: Modular component-based structure with clear separation of concerns

## Project Structure

```
cv-analyzer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application & route definitions
│   │   ├── models.py            # Pydantic data models
│   │   ├── config.py            # Configuration management
│   │   └── services/
│   │       ├── cv_extraction.py  # Document text extraction service
│   │       ├── cv_analysis.py    # Rule-based analysis engine
│   │       └── llm_client.py     # Gemini API integration layer
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUploadForm.tsx
│   │   │   ├── AnalysisResult.tsx
│   │   │   ├── SectionChecklist.tsx
│   │   │   ├── KeywordMatchList.tsx
│   │   │   └── SuggestionCard.tsx
│   │   ├── services/
│   │   │   └── apiClient.ts
│   │   ├── types/
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.docker.example
├── setup.sh
├── README.md
├── GEMINI_SETUP.md
└── DOCKER.md
```

## Getting Started

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Google Gemini API Key** (Free tier available at https://aistudio.google.com/app/apikey)
- **Docker & Docker Compose** (optional, for containerized deployment)

### Backend Setup

1. **Navigate to backend directory:**

   ```bash
   cd cv-analyzer/backend
   ```

2. **Create and activate virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your Gemini API credentials:

   ```env
   # Obtain free API key at: https://aistudio.google.com/app/apikey
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-1.5-flash
   ```

5. **Start the development server:**

   ```bash
   uvicorn app.main:app --reload
   ```

   API server runs at `http://localhost:8000`

6. **Verify deployment:**

   Access interactive API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**

   ```bash
   cd cv-analyzer/frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Start development server:**

   ```bash
   npm run dev
   ```

   Development server runs at `http://localhost:5173`

4. **Access the application:**

   Navigate to `http://localhost:5173` in your browser

## Docker Deployment

See [DOCKER.md](DOCKER.md) for comprehensive deployment documentation.

### Quick Start with Docker Compose

```bash
# Clone and navigate to project
cd cv-analyzer

# Configure environment
cp .env.docker.example .env
# Edit .env and add your Gemini API key

# Start all services
docker-compose up

# Access application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Production Deployment

```bash
# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Usage Guide

1. **Upload Resume:**

   - Use drag-and-drop or file browser to select your resume
   - Supported formats: PDF, DOCX
   - Maximum file size: 10 MB

2. **Add Job Description (Optional):**

   - Paste the target job description for keyword matching analysis
   - Enables comparison of resume content against job requirements

3. **Analyze:**

   - Click "Analyze CV" to initiate processing
   - Analysis typically completes in 2-5 seconds

4. **Review Results:**

   - **Overall Summary**: High-level assessment of resume quality
   - **Strengths & Weaknesses**: Detailed SWOT analysis
   - **Section Checklist**: Presence/absence of key resume sections
   - **Keyword Analysis**: Matched and missing keywords (when JD provided)
   - **Section-specific Suggestions**: Targeted improvement recommendations
   - **Rewritten Examples**: Enhanced versions of weak bullet points

5. **Iterate and Improve:**
   - Apply suggestions to your resume
   - Re-analyze to track improvements

## Configuration

### Backend Configuration

Edit `backend/app/config.py`:

```python
# Gemini API Configuration
GEMINI_MODEL_NAME = "gemini-1.5-flash"  # or "gemini-1.5-pro"
GEMINI_MAX_TOKENS = 2000
GEMINI_TEMPERATURE = 0.7

# File Upload Constraints
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = [".pdf", ".docx"]
```

### Frontend Configuration

Create `frontend/.env.local` to override defaults:

```env
VITE_API_URL=http://localhost:8000
```

## API Reference

### `POST /api/analyze-cv`

Analyzes a resume and returns structured improvement suggestions.

**Request:**

- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `cv_file`: File (required) - PDF or DOCX format
  - `jd_text`: string (optional) - Job description for keyword analysis

**Response:**

```json
{
  "overall_summary": "Comprehensive assessment of resume quality...",
  "strengths": [
    "Clear technical skills section",
    "Quantified achievements in experience"
  ],
  "weaknesses": [
    "Missing professional summary",
    "Limited project descriptions"
  ],
  "section_checklist": {
    "has_summary": true,
    "has_skills": true,
    "has_experience": true,
    "has_projects": true,
    "has_education": true
  },
  "jd_analysis": {
    "jd_keywords": ["python", "fastapi", "docker"],
    "matched_keywords": ["python", "docker"],
    "missing_keywords": ["fastapi"]
  },
  "suggestions_by_section": [
    {
      "section_name": "Experience",
      "issues": ["Bullet points lack quantification"],
      "suggestions": ["Add metrics to demonstrate impact"]
    }
  ],
  "rewritten_examples": [
    {
      "original": "Worked on backend development",
      "improved": "Architected and deployed scalable backend services using FastAPI, reducing API response time by 40%",
      "section": "Experience"
    }
  ]
}
```

## Gemini AI Integration

The application leverages Google's Gemini AI for intelligent resume analysis with multilingual support.

### API Key Setup

1. Navigate to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key (format: `AIzaSy...`)

For detailed setup instructions, see [GEMINI_SETUP.md](GEMINI_SETUP.md)

### Model Options

**Gemini 1.5 Flash** (Recommended for development):

- 15 requests per minute
- 1 million tokens per minute
- 1,500 requests per day
- Optimized for speed

**Gemini 1.5 Pro** (Higher quality):

- 2 requests per minute
- 32,000 tokens per minute
- Enhanced analysis quality
- Configure via `.env`: `GEMINI_MODEL=gemini-1.5-pro`

### Automatic Fallback

The system implements graceful degradation:

- If the Gemini API is unavailable or rate-limited, the application automatically falls back to mock data
- Ensures continuous operation without service interruption
- Logs indicate whether real AI or mock data is being used

## Testing

### Backend Testing

```bash
cd backend

# Test API endpoint with sample resume
curl -X POST "http://localhost:8000/api/analyze-cv" \
  -F "cv_file=@/path/to/sample_cv.pdf" \
  -F "jd_text=Seeking Python developer with FastAPI and Docker experience"
```

### Frontend Testing

1. Ensure both backend and frontend servers are running
2. Navigate to `http://localhost:5173`
3. Upload a test resume (PDF or DOCX)
4. Optionally provide a job description
5. Verify all UI components render correctly and data populates as expected

### Integration Testing

```bash
# Run backend tests (if test suite exists)
cd backend
pytest

# Run frontend tests (if test suite exists)
cd frontend
npm test
```

## Production Build

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend

```bash
cd frontend
npm run build
# Output directory: dist/
# Serve with any static file server (nginx, Apache, etc.)

# Preview production build locally
npm run preview
```

### Docker Production Build

```bash
# Build and run in production mode
docker-compose up -d

# Scale backend for high availability
docker-compose up -d --scale backend=3
```

## Deployment Strategies

See [DOCKER.md](DOCKER.md) for detailed deployment guides covering:

- **Container Registries**: Docker Hub, AWS ECR, Google Container Registry
- **Cloud Platforms**: AWS ECS/Fargate, Google Cloud Run, Azure Container Instances
- **Platform-as-a-Service**: Heroku, DigitalOcean App Platform, Railway
- **VPS Deployment**: Setup with nginx reverse proxy and SSL
- **CI/CD Integration**: GitHub Actions, GitLab CI, Jenkins

## Technology Highlights

### Backend Technologies

- **FastAPI**: Modern, fast async web framework
- **Pydantic**: Data validation using Python type hints
- **PDFPlumber**: Robust PDF text extraction
- **python-docx**: Microsoft Word document processing
- **Google Generative AI**: LLM integration for intelligent analysis
- **python-dotenv**: Environment variable management

### Frontend Technologies

- **React 18**: Latest React with concurrent features
- **TypeScript**: Static typing for enhanced developer experience
- **Vite**: Next-generation frontend tooling
- **TailwindCSS**: Utility-first CSS framework
- **Axios**: Promise-based HTTP client

### DevOps & Infrastructure

- **Docker**: Container runtime
- **Docker Compose**: Multi-container orchestration
- **Uvicorn**: ASGI server for FastAPI
- **Nginx**: Reverse proxy and static file serving (in Docker)

## Security Considerations

- **API Key Protection**: Environment variables, never committed to version control
- **File Upload Validation**: Size limits and format restrictions prevent abuse
- **CORS Configuration**: Properly configured cross-origin policies
- **Input Sanitization**: All user inputs are validated and sanitized
- **Error Handling**: Generic error messages prevent information leakage
- **Dependency Management**: Regular updates to patch security vulnerabilities

## Troubleshooting

### Backend Issues

**Server fails to start:**

- Verify Python version (3.8 or higher)
- Ensure virtual environment is activated
- Check all dependencies are installed: `pip list`
- Confirm port 8000 is not in use: `lsof -i :8000`

**API errors:**

- Check backend logs for detailed error messages
- Verify Gemini API key is correctly configured
- Ensure `.env` file exists in backend directory

### Frontend Issues

**Cannot connect to backend:**

- Verify backend is running at `http://localhost:8000`
- Check CORS settings in `backend/app/main.py`
- Inspect browser console for network errors
- Confirm `VITE_API_URL` is correctly configured

**Build failures:**

- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version compatibility (16+)
- Verify no TypeScript compilation errors: `npm run build`

### Gemini API Issues

**Authentication errors:**

- Verify API key format (should start with `AIzaSy`)
- Ensure no whitespace in the API key
- Check API key is enabled in Google AI Studio

**Rate limiting:**

- Gemini 1.5 Flash: 15 requests per minute
- Wait 60 seconds before retrying
- Consider implementing client-side rate limiting
- System will automatically fall back to mock data

### Docker Issues

**Container fails to start:**

- Check Docker daemon is running: `docker ps`
- Verify `.env` file exists and is properly formatted
- Review logs: `docker-compose logs backend`
- Ensure ports 8000 and 5173 are available

**Network issues:**

- Inspect Docker network: `docker network ls`
- Verify service connectivity: `docker-compose exec backend ping frontend`
- Check firewall rules are not blocking container communication

## Performance Optimization

- **Backend**: Async processing with FastAPI for concurrent request handling
- **Frontend**: Code splitting and lazy loading for optimal bundle size
- **Docker**: Multi-stage builds minimize image size
- **Caching**: Dependency layer caching in Docker for faster rebuilds
- **CDN**: Consider serving static assets via CDN in production

## Roadmap

- [ ] User authentication and session management
- [ ] Resume version history and comparison
- [ ] PDF export of analysis results
- [ ] Additional file format support (RTF, TXT)
- [ ] Resume templates and examples library
- [ ] ATS (Applicant Tracking System) compatibility scoring
- [ ] Industry-specific analysis models
- [ ] Team collaboration features
- [ ] API rate limiting and usage analytics
- [ ] Enhanced caching strategies

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes with clear, descriptive messages
4. Write tests for new functionality
5. Ensure all tests pass
6. Submit a pull request with a detailed description

## License

This project is provided as-is for educational and personal use. For commercial use, please contact the maintainers.

## Acknowledgments

Built with modern web technologies and best practices in mind. Special thanks to the open-source community for the excellent tools and libraries that made this project possible.

---

**Version**: 1.0.0  
**Last Updated**: November 2024  
**Maintainer**: Professional Development Team
