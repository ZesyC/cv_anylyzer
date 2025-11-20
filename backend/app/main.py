"""
FastAPI main application.
Provides REST API endpoints for CV analysis.
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import logging

from app.models import CVAnalysisResponse
from app.services.cv_extraction import extract_cv_text
from app.services.cv_analysis import analyze_cv
from app.services.llm_client import generate_ai_feedback
from app.config import MAX_FILE_SIZE, ALLOWED_EXTENSIONS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CV Analyzer API",
    description="AI-powered CV analysis and improvement suggestions",
    version="1.0.0"
)

# Configure CORS - allow frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and CRA default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "CV Analyzer API is running",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze-cv"
        }
    }


@app.post("/api/analyze-cv", response_model=CVAnalysisResponse)
async def analyze_cv_endpoint(
    cv_file: UploadFile = File(..., description="CV file (PDF or DOCX)"),
    jd_text: Optional[str] = Form(None, description="Optional Job Description text")
):
    """
    Analyze a CV and provide improvement suggestions.
    
    Args:
        cv_file: Uploaded CV file (PDF or DOCX format)
        jd_text: Optional Job Description to compare against
        
    Returns:
        CVAnalysisResponse with comprehensive feedback
        
    Raises:
        HTTPException: If file format is unsupported or processing fails
    """
    try:
        # Validate file extension
        filename = cv_file.filename or ""
        file_ext = filename.lower().split('.')[-1] if '.' in filename else ""
        
        if f".{file_ext}" not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Read file content
        file_content = await cv_file.read()
        
        # Validate file size
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.1f} MB"
            )
        
        logger.info(f"Processing CV file: {filename} ({len(file_content)} bytes)")
        
        # Extract text from CV
        try:
            cv_text = extract_cv_text(file_content, filename)
        except Exception as e:
            logger.error(f"Text extraction failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to extract text from file: {str(e)}"
            )
        
        if not cv_text or len(cv_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Could not extract meaningful text from the CV. Please ensure the file is not corrupted or password-protected."
            )
        
        logger.info(f"Extracted {len(cv_text)} characters from CV")
        
        # Perform rule-based analysis
        rule_based_result = analyze_cv(cv_text, jd_text)
        
        logger.info(f"Rule-based analysis complete. Sections found: "
                   f"Summary={rule_based_result.has_summary}, "
                   f"Skills={rule_based_result.has_skills}, "
                   f"Experience={rule_based_result.has_experience}, "
                   f"Projects={rule_based_result.has_projects}, "
                   f"Education={rule_based_result.has_education}")
        
        # Generate AI-powered feedback
        analysis_result = generate_ai_feedback(cv_text, jd_text, rule_based_result)
        
        logger.info("Analysis complete, returning results")
        
        return analysis_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during CV analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while analyzing the CV: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
