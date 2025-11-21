# CV Analyzer - AI-Powered Resume Improvement Tool

A full-stack web application that analyzes CVs/resumes and provides AI-powered suggestions for improvement. Optionally compares your CV against a Job Description to identify missing keywords and tailor your application.

##  Features

- **PDF & DOCX Support**: Upload your resume in PDF or DOCX format
- **Section Detection**: Automatically identifies key CV sections (Summary, Skills, Experience, Projects, Education)
- **Keyword Analysis**: Compare your CV against job descriptions to find missing keywords
- **AI-Powered Feedback**: Get detailed suggestions for improving each section
- **Bullet Point Enhancement**: See rewritten examples of weak bullet points with stronger alternatives
- **Modern UI**: Clean, responsive interface built with React and TailwindCSS
- **Fast Processing**: Efficient text extraction and analysis

##  Architecture

### Backend (FastAPI + Python)

- **FastAPI** framework for REST API
- **PDF extraction** using `pdfplumber`
- **DOCX extraction** using `python-docx`
- **Rule-based analysis** for section detection and metrics
- **Mock LLM integration** (ready for real API integration)

### Frontend (React + TypeScript)

- **React 18** with TypeScript for type safety
- **Vite** for fast development and building
- **TailwindCSS** for modern, responsive styling
- **Axios** for API communication
- Modular component architecture

##  Project Structure

```
cv-analyzer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app and routes
│   │   ├── models.py            # Pydantic models
│   │   ├── config.py            # Configuration constants
│   │   └── services/
│   │       ├── cv_extraction.py  # PDF/DOCX text extraction
│   │       ├── cv_analysis.py    # Rule-based analysis
│   │       └── llm_client.py     # LLM integration (mock)
│   ├── requirements.txt
│   └── .gitignore
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── FileUploadForm.tsx
    │   │   ├── AnalysisResult.tsx
    │   │   ├── SectionChecklist.tsx
    │   │   ├── KeywordMatchList.tsx
    │   │   └── SuggestionCard.tsx
    │   ├── services/
    │   │   └── apiClient.ts
    │   ├── types/
    │   │   └── api.ts
    │   ├── App.tsx
    │   ├── main.tsx
    │   └── index.css
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.js
    └── tsconfig.json
```

##  Getting Started

### Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** and **npm** (for frontend)
- **pip** (Python package manager)

### Backend Setup

1. **Navigate to the backend directory:**

   ```bash
   cd cv-analyzer/backend
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server:**

   ```bash
   uvicorn app.main:app --reload
   ```

   The backend API will be available at `http://localhost:8000`

5. **Verify the API is running:**
   Open `http://localhost:8000/docs` in your browser to see the interactive API documentation.

### Frontend Setup

1. **Navigate to the frontend directory:**

   ```bash
   cd cv-analyzer/frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Run the development server:**

   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

4. **Open the app:**
   Navigate to `http://localhost:5173` in your browser.

##  Usage

1. **Upload Your CV:**

   - Click "Browse Files" or drag and drop your PDF/DOCX CV
   - Supported formats: PDF, DOCX
   - Maximum file size: 10 MB

2. **Add Job Description (Optional):**

   - Paste the job description in the textarea
   - This enables keyword matching analysis

3. **Analyze:**

   - Click " Analyze CV"
   - Wait for the analysis to complete (usually 2-5 seconds)

4. **Review Results:**

   - **Overall Summary**: High-level assessment of your CV
   - **Strengths & Weaknesses**: What's working and what needs improvement
   - **Section Checklist**: Which CV sections are present/missing
   - **Keyword Analysis**: JD keywords matched vs missing (if JD provided)
   - **Detailed Suggestions**: Section-by-section improvement recommendations
   - **Rewritten Examples**: Before/after examples of stronger bullet points

5. **Implement Improvements:**
   - Use the suggestions to update your CV
   - Analyze again to see your progress!

## Configuration

### Backend Configuration

Edit `backend/app/config.py`:

```python
# LLM Configuration (for future real API integration)
LLM_MODEL_NAME = "gpt-4"
LLM_MAX_TOKENS = 2000
LLM_TEMPERATURE = 0.7

# File Upload Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = [".pdf", ".docx"]
```

### Frontend Configuration

Create `frontend/.env.local` to override the API URL:

```env
VITE_API_URL=http://localhost:8000
```

##  API Endpoints

### `POST /api/analyze-cv`

Analyzes a CV and returns improvement suggestions.

**Request:**

- `cv_file`: File (PDF or DOCX)
- `jd_text`: string (optional)

**Response:**

```json
{
  "overall_summary": "string",
  "strengths": ["string"],
  "weaknesses": ["string"],
  "section_checklist": {
    "has_summary": true,
    "has_skills": true,
    "has_experience": true,
    "has_projects": true,
    "has_education": true
  },
  "jd_analysis": {
    "jd_keywords": ["string"],
    "matched_keywords": ["string"],
    "missing_keywords": ["string"]
  },
  "suggestions_by_section": [
    {
      "section_name": "string",
      "issues": ["string"],
      "suggestions": ["string"]
    }
  ],
  "rewritten_examples": [
    {
      "original": "string",
      "improved": "string",
      "section": "string"
    }
  ]
}
```

##  LLM Integration

Currently, the app uses a **mock LLM implementation** that returns realistic sample data. To integrate a real LLM API:

1. **Install additional dependencies:**

   ```bash
   pip install openai  # or anthropic, etc.
   ```

2. **Update `backend/app/services/llm_client.py`:**

   - Add API key configuration
   - Replace `_generate_mock_feedback()` with real API calls
   - Implement proper error handling and retries

3. **Example OpenAI integration:**

   ```python
   import openai

   def generate_ai_feedback(cv_text, jd_text, rule_based_result):
       prompt = f"Analyze this CV and provide feedback: {cv_text}"
       response = openai.ChatCompletion.create(
           model="gpt-4",
           messages=[{"role": "user", "content": prompt}]
       )
       # Parse response and return CVAnalysisResponse
   ```

##  UI Features

- **Drag-and-drop** file upload
- **Loading states** with smooth animations
- **Expandable examples** - click to see before/after comparisons
- **Responsive design** - works on desktop and mobile
- **Visual indicators** - color-coded sections and keywords
- **Smooth scrolling** - auto-scroll to results
- **Error handling** - clear error messages

##  Testing

### Testing the Backend

```bash
cd backend

# Test with a sample CV using curl
curl -X POST "http://localhost:8000/api/analyze-cv" \
  -F "cv_file=@/path/to/sample_cv.pdf" \
  -F "jd_text=Looking for a Python developer with FastAPI experience"
```

### Testing the Frontend

1. Start both backend and frontend servers
2. Navigate to `http://localhost:5173`
3. Upload a sample CV (PDF or DOCX)
4. Optionally add a job description
5. Verify all components display correctly

##  Building for Production

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm run build
# Serve the dist/ folder with your preferred static file server
npm run preview  # For local preview
```

##  Future Enhancements

- [ ] Real LLM API integration (OpenAI, Anthropic, etc.)
- [ ] User authentication and CV history
- [ ] Export suggestions as PDF
- [ ] Additional file format support (RTF, TXT)
- [ ] Resume templates and examples
- [ ] ATS (Applicant Tracking System) compatibility checker
- [ ] Industry-specific analysis
- [ ] Multi-language support

##  Notes for Students/Developers

This project is designed to be:

- **Educational**: Clean code with extensive comments
- **Modular**: Easy to understand and extend
- **Production-ready structure**: Follows best practices
- **Beginner-friendly**: Suitable for 2nd-year CS/AI students

Key learning points:

- Full-stack development with modern technologies
- REST API design and implementation
- File upload handling (multipart/form-data)
- PDF/DOCX text extraction
- React component architecture
- TypeScript type safety
- State management in React
- TailwindCSS styling
- Mock vs real API integration patterns

## License

This project is provided as-is for educational and personal use.

## Contributing

Feel free to fork this project and add your own improvements!

---

Built with Zéy
