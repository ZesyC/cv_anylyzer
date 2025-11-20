"""
LLM integration service.
This module provides AI-powered feedback generation using an LLM API.

TODO: Replace mock implementation with real LLM API calls (e.g., OpenAI, Anthropic, etc.)
TODO: Add API key configuration and authentication
TODO: Implement proper error handling and retries
"""
from typing import Optional
from app.models import (
    CVAnalysisResponse,
    CVSectionChecklist,
    JDKeywordAnalysis,
    SectionSuggestions,
    RewrittenExample
)
from app.services.cv_analysis import RuleBasedResult, extract_keywords, compare_keywords


def generate_ai_feedback(
    cv_text: str,
    jd_text: Optional[str],
    rule_based_result: RuleBasedResult
) -> CVAnalysisResponse:
    """
    Generate AI-powered feedback for CV improvement.
    
    This function should call an LLM API to analyze the CV and provide suggestions.
    Currently using MOCK data for development and testing.
    
    Args:
        cv_text: The extracted CV text
        jd_text: Optional Job Description text
        rule_based_result: Results from rule-based analysis
        
    Returns:
        CVAnalysisResponse with comprehensive feedback
    """
    
    # TODO: Replace this entire function with real LLM API call
    # Example prompt structure for real implementation:
    """
    prompt = f'''
    You are an expert career advisor and resume consultant.
    
    CONTEXT:
    - The candidate is a junior or student-level applicant for technical roles (CS/AI/Data Science)
    - Their resume should highlight technical skills, projects, and quantifiable achievements
    
    RESUME TEXT:
    {cv_text}
    
    JOB DESCRIPTION (if provided):
    {jd_text or "Not provided"}
    
    BASIC ANALYSIS:
    - Has Summary: {rule_based_result.has_summary}
    - Has Skills: {rule_based_result.has_skills}
    - Has Experience: {rule_based_result.has_experience}
    - Has Projects: {rule_based_result.has_projects}
    - Has Education: {rule_based_result.has_education}
    - Quantified Bullets: {rule_based_result.quantified_bullet_count}/{rule_based_result.total_bullet_count}
    
    TASK:
    1. Provide an overall summary of the candidate's profile
    2. List 3-5 key strengths
    3. List 3-5 key weaknesses or areas for improvement
    4. For each major section (Skills, Experience, Projects, Education), provide:
       - Specific issues found
       - Concrete suggestions for improvement
    5. Provide 2-5 examples of weak bullet points rewritten to be stronger
    
    Format your response as JSON matching the CVAnalysisResponse schema.
    '''
    """
    
    # MOCK IMPLEMENTATION - Replace with real LLM call
    return _generate_mock_feedback(cv_text, jd_text, rule_based_result)


def _generate_mock_feedback(
    cv_text: str,
    jd_text: Optional[str],
    rule_based_result: RuleBasedResult
) -> CVAnalysisResponse:
    """
    Generate realistic mock feedback for development and testing.
    This simulates what an LLM would return.
    """
    
    # Analyze JD keywords if provided
    jd_analysis = None
    if jd_text:
        jd_keywords = extract_keywords(jd_text, top_n=20)
        matched, missing = compare_keywords(cv_text, jd_keywords)
        jd_analysis = JDKeywordAnalysis(
            jd_keywords=jd_keywords[:15],  # Limit for display
            matched_keywords=matched[:10],
            missing_keywords=missing[:10]
        )
    
    # Build section checklist
    section_checklist = CVSectionChecklist(
        has_summary=rule_based_result.has_summary,
        has_skills=rule_based_result.has_skills,
        has_experience=rule_based_result.has_experience,
        has_projects=rule_based_result.has_projects,
        has_education=rule_based_result.has_education
    )
    
    # Generate overall summary
    missing_sections = []
    if not rule_based_result.has_summary:
        missing_sections.append("professional summary")
    if not rule_based_result.has_skills:
        missing_sections.append("skills section")
    if not rule_based_result.has_projects:
        missing_sections.append("projects section")
    
    overall_summary = (
        f"This is a {'strong' if len(missing_sections) == 0 else 'developing'} CV for a technical role. "
        f"The resume demonstrates {'solid' if rule_based_result.has_experience else 'limited'} experience "
        f"and includes {rule_based_result.quantified_bullet_count} quantified achievements out of "
        f"{rule_based_result.total_bullet_count} total bullet points."
    )
    
    if missing_sections:
        overall_summary += f" However, it's missing: {', '.join(missing_sections)}."
    
    # Generate strengths
    strengths = []
    if rule_based_result.has_education:
        strengths.append("Clear educational background included")
    if rule_based_result.has_experience:
        strengths.append("Work experience section present")
    if rule_based_result.has_projects:
        strengths.append("Showcases relevant projects")
    if rule_based_result.quantified_bullet_count > 2:
        strengths.append("Some achievements are quantified with metrics")
    if jd_analysis and len(jd_analysis.matched_keywords) > 5:
        strengths.append(f"Good keyword match with JD ({len(jd_analysis.matched_keywords)} matches)")
    
    # Ensure at least 3 strengths
    if len(strengths) < 3:
        strengths.extend([
            "Structured format that's easy to scan",
            "Focuses on technical background"
        ])
    
    # Generate weaknesses
    weaknesses = []
    if not rule_based_result.has_summary:
        weaknesses.append("Missing professional summary/objective at the top")
    if not rule_based_result.has_skills:
        weaknesses.append("No dedicated skills section to highlight technical competencies")
    if not rule_based_result.has_projects:
        weaknesses.append("Missing projects section to showcase practical work")
    if rule_based_result.quantified_bullet_count < 3:
        weaknesses.append("Not enough quantified achievements - add specific metrics and numbers")
    if jd_analysis and len(jd_analysis.missing_keywords) > 5:
        weaknesses.append(f"Missing key terms from JD ({len(jd_analysis.missing_keywords)} keywords not found)")
    
    # Ensure at least 3 weaknesses
    if len(weaknesses) < 3:
        weaknesses.extend([
            "Bullet points could be more action-oriented",
            "Some sections could benefit from better formatting"
        ])
    
    # Generate section-specific suggestions
    suggestions_by_section = []
    
    # Skills section
    if not rule_based_result.has_skills:
        suggestions_by_section.append(SectionSuggestions(
            section_name="Skills",
            issues=["Skills section is missing entirely"],
            suggestions=[
                "Add a dedicated 'Technical Skills' section near the top",
                "Group skills by category (Programming Languages, Frameworks, Tools, etc.)",
                "List specific technologies you've used in projects or work"
            ]
        ))
    else:
        suggestions_by_section.append(SectionSuggestions(
            section_name="Skills",
            issues=["Skills may not be prominent enough"],
            suggestions=[
                "Ensure skills section is near the top for visibility",
                "Consider grouping skills by proficiency level or category",
                "Match skills to keywords in the job description"
            ]
        ))
    
    # Experience section
    if rule_based_result.has_experience:
        suggestions_by_section.append(SectionSuggestions(
            section_name="Experience",
            issues=[
                "Some bullet points lack quantifiable metrics",
                "Action verbs could be stronger"
            ],
            suggestions=[
                "Start each bullet with strong action verbs (Developed, Implemented, Optimized)",
                "Add specific metrics: percentages, numbers, time saved, users impacted",
                "Follow the STAR format: Situation, Task, Action, Result",
                "Focus on impact and outcomes, not just responsibilities"
            ]
        ))
    
    # Projects section
    if rule_based_result.has_projects:
        suggestions_by_section.append(SectionSuggestions(
            section_name="Projects",
            issues=["Project descriptions could be more impactful"],
            suggestions=[
                "Describe the problem solved and technologies used",
                "Include links to GitHub repos or live demos if available",
                "Mention team size if collaborative, or highlight solo work",
                "Quantify results where possible (users, performance improvements)"
            ]
        ))
    else:
        suggestions_by_section.append(SectionSuggestions(
            section_name="Projects",
            issues=["Projects section is missing"],
            suggestions=[
                "Add 2-4 relevant technical projects",
                "Include academic projects, personal projects, or hackathons",
                "For each project: name, technologies, brief description, and impact"
            ]
        ))
    
    # Summary section
    if not rule_based_result.has_summary:
        suggestions_by_section.append(SectionSuggestions(
            section_name="Summary",
            issues=["No professional summary or objective"],
            suggestions=[
                "Add a 2-3 sentence summary at the top",
                "Highlight your background, key skills, and career goals",
                "Tailor the summary to the specific role you're applying for"
            ]
        ))
    
    # Formatting suggestions
    suggestions_by_section.append(SectionSuggestions(
        section_name="Formatting",
        issues=["General formatting improvements needed"],
        suggestions=[
            "Ensure consistent date formatting (e.g., 'Jan 2023 - Present')",
            "Use clear section headers with adequate spacing",
            "Keep the resume to 1 page (for students/early career)",
            "Use a clean, professional font (11-12pt)",
            "Maintain consistent bullet point style throughout"
        ]
    ))
    
    # Generate rewritten examples
    rewritten_examples = [
        RewrittenExample(
            original="Worked on a machine learning project",
            improved="Developed a CNN-based image classifier achieving 94% accuracy on 10K+ images, reducing manual labeling time by 60%",
            section="Projects"
        ),
        RewrittenExample(
            original="Responsible for database management",
            improved="Optimized PostgreSQL database queries, reducing average response time from 2.3s to 0.4s and improving user experience for 5,000+ daily users",
            section="Experience"
        ),
        RewrittenExample(
            original="Built a web application using React",
            improved="Architected and deployed a full-stack React + Node.js web app with 1,000+ monthly active users, implementing JWT authentication and RESTful APIs",
            section="Projects"
        ),
        RewrittenExample(
            original="Assisted team with software development tasks",
            improved="Collaborated with 4-person engineering team to deliver 3 major features on time, writing 2,000+ lines of Python code and achieving 95% test coverage",
            section="Experience"
        )
    ]
    
    return CVAnalysisResponse(
        overall_summary=overall_summary,
        strengths=strengths[:5],
        weaknesses=weaknesses[:5],
        section_checklist=section_checklist,
        jd_analysis=jd_analysis,
        suggestions_by_section=suggestions_by_section,
        rewritten_examples=rewritten_examples
    )
