"""
Rule-based CV analysis service.
Performs basic analysis without requiring LLM: section detection, keyword matching, etc.
"""
import re
from dataclasses import dataclass
from typing import List, Set, Optional, Tuple


@dataclass
class RuleBasedResult:
    """Results from rule-based CV analysis."""
    has_summary: bool
    has_skills: bool
    has_experience: bool
    has_projects: bool
    has_education: bool
    quantified_bullet_count: int
    total_bullet_count: int


def detect_sections(cv_text: str) -> dict:
    """
    Detect presence of standard CV sections using keyword matching.
    
    Args:
        cv_text: The full CV text
        
    Returns:
        Dictionary with boolean flags for each section
    """
    cv_lower = cv_text.lower()
    
    # Define section keywords (case-insensitive)
    summary_keywords = ['summary', 'profile', 'objective', 'about me']
    skills_keywords = ['skills', 'technical skills', 'competencies', 'expertise']
    experience_keywords = ['experience', 'work experience', 'employment', 'work history']
    projects_keywords = ['projects', 'personal projects', 'portfolio']
    education_keywords = ['education', 'academic', 'degree', 'university', 'college']
    
    return {
        'has_summary': any(keyword in cv_lower for keyword in summary_keywords),
        'has_skills': any(keyword in cv_lower for keyword in skills_keywords),
        'has_experience': any(keyword in cv_lower for keyword in experience_keywords),
        'has_projects': any(keyword in cv_lower for keyword in projects_keywords),
        'has_education': any(keyword in cv_lower for keyword in education_keywords),
    }


def count_quantified_bullets(cv_text: str) -> Tuple[int, int]:
    """
    Count bullet points and how many contain quantifiable metrics.
    A bullet is considered quantified if it contains numbers, percentages, or metrics.
    
    Args:
        cv_text: The full CV text
        
    Returns:
        Tuple of (quantified_count, total_count)
    """
    # Find bullet points (lines starting with -, •, *, or similar)
    bullet_pattern = r'^[\s]*[•\-\*◦]+[\s]*.+$'
    bullets = re.findall(bullet_pattern, cv_text, re.MULTILINE)
    
    total_count = len(bullets)
    
    # Count bullets with numbers, percentages, or common metrics
    quantified_count = 0
    for bullet in bullets:
        # Check for numbers, percentages, or quantifiable terms
        if re.search(r'\d+%|\d+\+|\d+x|\d+,\d+|\d+ [a-zA-Z]+', bullet):
            quantified_count += 1
    
    return quantified_count, total_count


def extract_keywords(text: Optional[str], top_n: int = 30) -> List[str]:
    """
    Extract meaningful keywords from text.
    Simple implementation: tokenize, remove stopwords, keep unique words.
    
    Args:
        text: Input text (e.g., Job Description)
        top_n: Maximum number of keywords to return
        
    Returns:
        List of extracted keywords
    """
    if not text:
        return []
    
    # Common English stopwords (simplified list)
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
    }
    
    # Tokenize and clean
    words = re.findall(r'\b[a-z]+\b', text.lower())
    
    # Filter stopwords and short words, keep unique
    keywords = []
    seen = set()
    for word in words:
        if len(word) > 2 and word not in stopwords and word not in seen:
            keywords.append(word)
            seen.add(word)
            if len(keywords) >= top_n:
                break
    
    return keywords


def compare_keywords(cv_text: str, jd_keywords: List[str]) -> Tuple[List[str], List[str]]:
    """
    Compare JD keywords with CV content.
    
    Args:
        cv_text: The full CV text
        jd_keywords: List of keywords from Job Description
        
    Returns:
        Tuple of (matched_keywords, missing_keywords)
    """
    cv_lower = cv_text.lower()
    
    matched = []
    missing = []
    
    for keyword in jd_keywords:
        if keyword.lower() in cv_lower:
            matched.append(keyword)
        else:
            missing.append(keyword)
    
    return matched, missing


def analyze_cv(cv_text: str, jd_text: Optional[str] = None) -> RuleBasedResult:
    """
    Perform complete rule-based analysis of CV.
    
    Args:
        cv_text: The full CV text
        jd_text: Optional Job Description text
        
    Returns:
        RuleBasedResult with analysis findings
    """
    sections = detect_sections(cv_text)
    quantified_count, total_count = count_quantified_bullets(cv_text)
    
    return RuleBasedResult(
        has_summary=sections['has_summary'],
        has_skills=sections['has_skills'],
        has_experience=sections['has_experience'],
        has_projects=sections['has_projects'],
        has_education=sections['has_education'],
        quantified_bullet_count=quantified_count,
        total_bullet_count=total_count,
    )
