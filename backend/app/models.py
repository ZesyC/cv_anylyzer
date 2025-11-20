"""
Pydantic models for API requests and responses.
These models define the structure of data exchanged between frontend and backend.
"""
from typing import List, Optional
from pydantic import BaseModel


class CVSectionChecklist(BaseModel):
    """Checklist of standard CV sections and their presence."""
    has_summary: bool
    has_skills: bool
    has_experience: bool
    has_projects: bool
    has_education: bool


class JDKeywordAnalysis(BaseModel):
    """Analysis of Job Description keywords vs CV content."""
    jd_keywords: List[str]
    matched_keywords: List[str]
    missing_keywords: List[str]


class RewrittenExample(BaseModel):
    """Example of original CV text vs AI-improved version."""
    original: str
    improved: str
    section: str  # e.g., "Experience", "Projects"


class SectionSuggestions(BaseModel):
    """Suggestions for a specific CV section."""
    section_name: str  # e.g., "Skills", "Experience", "Projects"
    issues: List[str]  # Problems detected in this section
    suggestions: List[str]  # Recommended improvements


class CVAnalysisResponse(BaseModel):
    """Complete analysis result returned to the frontend."""
    overall_summary: str
    strengths: List[str]
    weaknesses: List[str]
    section_checklist: CVSectionChecklist
    jd_analysis: Optional[JDKeywordAnalysis] = None
    suggestions_by_section: List[SectionSuggestions]
    rewritten_examples: List[RewrittenExample]
