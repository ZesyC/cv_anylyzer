# Development Guide

## Local Development Setup

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git** for version control
- **Google Gemini API Key** ([Get one free](https://aistudio.google.com/app/apikey))
- **Code Editor**: VS Code (recommended), PyCharm, or any IDE

### Initial Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd cv-analyzer
   ```

2. **Run the setup script**:

   ```bash
   chmod +x scripts/setup.sh
   scripts/setup.sh
   ```

   This will:

   - Create Python virtual environment
   - Install backend dependencies
   - Install frontend dependencies
   - Verify system requirements

3. **Configure environment variables**:
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and add your Gemini API key
   ```

### Running in Development Mode

#### Option 1: Manual Start (Recommended for debugging)

**Terminal 1 - Backend**:

```bash
cd backend
source venv/bin/activate  # macOS/Linux
# or venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend**:

```bash
cd frontend
npm run dev
```

#### Option 2: Using Development Script

```bash
scripts/dev.sh
```

This starts both backend and frontend in a single terminal session.

### Accessing the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
cv-analyzer/
├── backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── main.py          # Application entry point
│   │   ├── config.py        # Configuration
│   │   ├── models.py        # Data models
│   │   └── services/        # Business logic
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         # React TypeScript frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API clients
│   │   ├── types/           # TypeScript types
│   │   ├── App.tsx          # Main component
│   │   └── main.tsx         # Entry point
│   ├── package.json
│   └── Dockerfile
├── docs/             # Documentation
├── scripts/          # Utility scripts
└── config/           # Shared configuration
```

## Development Workflow

### Git Workflow

We follow the **Git Flow** branching model:

1. **Main Branches**:

   - `main`: Production-ready code
   - `develop`: Integration branch for features

2. **Supporting Branches**:

   - `feature/feature-name`: New features
   - `bugfix/bug-name`: Bug fixes
   - `hotfix/hotfix-name`: Production hotfixes
   - `release/version`: Release preparation

3. **Workflow**:

   ```bash
   # Create feature branch
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name

   # Make changes and commit
   git add .
   git commit -m "feat: your feature description"

   # Push and create PR
   git push origin feature/your-feature-name
   ```

### Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

**Format**: `<type>(<scope>): <subject>`

**Types**:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:

```bash
git commit -m "feat(backend): add keyword extraction service"
git commit -m "fix(frontend): resolve file upload validation issue"
git commit -m "docs: update API reference with new endpoints"
git commit -m "refactor(backend): improve error handling"
```

## Coding Standards

### Python (Backend)

**Style Guide**: [PEP 8](https://pep8.org/)

**Key Conventions**:

- 4 spaces for indentation
- Maximum line length: 88 characters (Black formatter)
- Use type hints for all functions
- Docstrings for public functions and classes

**Example**:

```python
from typing import List, Optional

def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Extract keywords from text.

    Args:
        text: Input text to analyze
        min_length: Minimum keyword length

    Returns:
        List of extracted keywords
    """
    # Implementation
    pass
```

**Linting & Formatting**:

```bash
# Install tools
pip install black flake8 mypy

# Format code
black .

# Lint code
flake8 .

# Type check
mypy app/
```

### TypeScript (Frontend)

**Style Guide**: [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)

**Key Conventions**:

- 2 spaces for indentation
- Use functional components with hooks
- Explicit type annotations
- PropTypes or TypeScript interfaces for components

**Example**:

```typescript
interface FileUploadProps {
  onFileSelect: (file: File) => void;
  acceptedFormats: string[];
  maxSize: number;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  acceptedFormats,
  maxSize,
}) => {
  // Implementation
};
```

**Linting & Formatting**:

```bash
# Install tools
npm install --save-dev eslint prettier

# Lint code
npm run lint

# Format code
npm run format
```

## Testing

### Backend Testing

**Framework**: pytest

**Structure**:

```
backend/tests/
├── conftest.py           # Shared fixtures
├── test_api/
│   └── test_analyze.py   # API endpoint tests
└── test_services/
    └── test_extraction.py # Service tests
```

**Running Tests**:

```bash
cd backend
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest -k "test_name"     # Run specific test
pytest --cov=app          # With coverage
```

**Example Test**:

```python
def test_cv_extraction_pdf(sample_pdf):
    """Test PDF text extraction."""
    result = extract_text_from_pdf(sample_pdf)
    assert result is not None
    assert len(result) > 0
```

### Frontend Testing

**Frameworks**: Vitest + React Testing Library

**Structure**:

```
frontend/src/
├── components/
│   ├── FileUpload.tsx
│   └── FileUpload.test.tsx
└── services/
    ├── apiClient.ts
    └── apiClient.test.ts
```

**Running Tests**:

```bash
cd frontend
npm test              # Run tests
npm test -- --watch   # Watch mode
npm test -- --coverage # With coverage
```

**Example Test**:

```typescript
import { render, screen } from "@testing-library/react";
import { FileUpload } from "./FileUpload";

test("renders file upload button", () => {
  render(<FileUpload onFileSelect={jest.fn()} />);
  expect(screen.getByText("Upload CV")).toBeInTheDocument();
});
```

## Debugging

### Backend Debugging

**Print Debugging**:

```python
import logging

# Configure logging in main.py
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use in code
logger.debug(f"Processing file: {filename}")
logger.error(f"Error occurred: {error}")
```

**VS Code Debugger**:
Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "cwd": "${workspaceFolder}/backend",
      "env": { "PYTHONPATH": "${workspaceFolder}/backend" }
    }
  ]
}
```

### Frontend Debugging

**Browser DevTools**:

- React DevTools extension
- Network tab for API calls
- Console for errors and logs

**VS Code Debugger**:

```json
{
  "name": "Chrome: Frontend",
  "type": "chrome",
  "request": "launch",
  "url": "http://localhost:5173",
  "webRoot": "${workspaceFolder}/frontend"
}
```

## Common Development Tasks

### Adding a New API Endpoint

1. Define Pydantic model in `models.py`
2. Create route handler in `main.py`
3. Implement business logic in `services/`
4. Add tests
5. Update API documentation

### Adding a New Frontend Component

1. Create component file in `src/components/`
2. Define TypeScript interfaces
3. Implement component logic
4. Add styles (TailwindCSS)
5. Add tests
6. Import and use in parent component

### Updating Dependencies

**Backend**:

```bash
cd backend
pip install --upgrade package-name
pip freeze > requirements.txt
```

**Frontend**:

```bash
cd frontend
npm update package-name
# or
npm install package-name@latest
```

## Environment Variables

### Backend (.env)

```env
# Gemini API
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# Server
HOST=0.0.0.0
PORT=8000
RELOAD=true

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# File Upload
MAX_FILE_SIZE_MB=10
```

### Frontend (.env.local)

```env
# API Configuration
VITE_API_URL=http://localhost:8000

# Feature Flags
VITE_ENABLE_ANALYTICS=false
```

## Performance Optimization

### Backend

- Use async/await for I/O operations
- Implement caching for repeated analyses
- Use connection pooling
- Profile with `cProfile`:
  ```bash
  python -m cProfile -o profile.stats app/main.py
  ```

### Frontend

- Lazy load components:
  ```typescript
  const AnalysisResult = lazy(() => import("./components/AnalysisResult"));
  ```
- Memoize expensive computations:
  ```typescript
  const processedData = useMemo(() => processData(data), [data]);
  ```
- Use React.memo for component optimization
- Analyze bundle size:
  ```bash
  npm run build
  npm run preview
  ```

## Troubleshooting

### Backend Issues

**Port already in use**:

```bash
lsof -i :8000
kill -9 <PID>
```

**Dependencies issues**:

```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Issues

**Node modules issues**:

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Build errors**:

```bash
npm run type-check  # Check TypeScript errors
npm run lint        # Check linting errors
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Gemini API Documentation](https://ai.google.dev/docs)
