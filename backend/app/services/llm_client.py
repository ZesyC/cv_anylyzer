"""
LLM integration service.
This module provides AI-powered feedback generation using Gemini API or mock data.
"""
from typing import Optional
import logging
import json

from app.models import (
    CVAnalysisResponse,
    CVSectionChecklist,
    JDKeywordAnalysis,
    SectionSuggestions,
    RewrittenExample
)
from app.services.cv_analysis import RuleBasedResult, extract_keywords, compare_keywords
from app.config import GEMINI_API_KEY, GEMINI_MODEL, USE_GEMINI_API

# Initialize Gemini AI if API key is available
if USE_GEMINI_API:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)

logger = logging.getLogger(__name__)


def generate_ai_feedback(
    cv_text: str,
    jd_text: Optional[str],
    rule_based_result: RuleBasedResult,
    language: str = "en"
) -> CVAnalysisResponse:
    """
    Generate AI-powered feedback for CV improvement.
    
    Uses Gemini API if available and configured, otherwise falls back to mock data.
    
    Args:
        cv_text: The extracted CV text
        jd_text: Optional Job Description text
        rule_based_result: Results from rule-based analysis
        language: Language for feedback ("en" or "vi")
        
    Returns:
        CVAnalysisResponse with comprehensive feedback
    """
    
    # Try Gemini API if configured
    if USE_GEMINI_API:
        try:
            logger.info(f"Using Gemini API ({GEMINI_MODEL}) for CV analysis in {language}")
            return _generate_gemini_feedback(cv_text, jd_text, rule_based_result, language)
        except Exception as e:
            logger.warning(f"Gemini API failed, falling back to mock: {str(e)}")
            # Fall back to mock on any error
    else:
        logger.info("Gemini API not configured, using mock feedback")
    
    # Fall back to mock implementation
    return _generate_mock_feedback(cv_text, jd_text, rule_based_result, language)


def _generate_gemini_feedback(
    cv_text: str,
    jd_text: Optional[str],
    rule_based_result: RuleBasedResult,
    language: str = "en"
) -> CVAnalysisResponse:
    """
    Generate CV feedback using Google Gemini API.
    
    Args:
        cv_text: The extracted CV text
        jd_text: Optional Job Description text
        rule_based_result: Results from rule-based analysis
        language: Language for feedback ("en" or "vi")
        
    Returns:
        CVAnalysisResponse with Gemini-generated feedback
        
    Raises:
        Exception: If API call fails or response parsing fails
    """
    # Build language-specific prompt
    prompt = _build_gemini_prompt(cv_text, jd_text, rule_based_result, language)
    
    # Call Gemini API
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    
    # Extract JSON from response
    response_text = response.text.strip()
    
    # Try to extract JSON (Gemini might wrap it in markdown code blocks)
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()
    elif "```" in response_text:
        json_start = response_text.find("```") + 3
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()
    
    # Parse JSON response
    try:
        feedback_data = json.loads(response_text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response as JSON: {e}")
        logger.error(f"Response text: {response_text[:500]}")
        raise
    
    # Analyze JD keywords if provided
    jd_analysis = None
    if jd_text:
        jd_keywords = extract_keywords(jd_text, top_n=20)
        matched, missing = compare_keywords(cv_text, jd_keywords)
        jd_analysis = JDKeywordAnalysis(
            jd_keywords=jd_keywords[:15],
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
    
    # Convert feedback data to Pydantic models
    suggestions_by_section = [
        SectionSuggestions(**suggestion)
        for suggestion in feedback_data.get("section_suggestions", [])
    ]
    
    rewritten_examples = [
        RewrittenExample(**example)
        for example in feedback_data.get("rewritten_examples", [])
    ]
    
    return CVAnalysisResponse(
        overall_summary=feedback_data.get("overall_summary", ""),
        strengths=feedback_data.get("strengths", []),
        weaknesses=feedback_data.get("weaknesses", []),
        section_checklist=section_checklist,
        jd_analysis=jd_analysis,
        suggestions_by_section=suggestions_by_section,
        rewritten_examples=rewritten_examples
    )


def _build_gemini_prompt(
    cv_text: str,
    jd_text: Optional[str],
    rule_based_result: RuleBasedResult,
    language: str
) -> str:
    """Build language-specific prompt for Gemini API."""
    
    if language == "vi":
        return f"""Bạn là chuyên gia tư vấn CV chuyên nghiệp với kinh nghiệm nhiều năm.

**CV CẦN PHÂN TÍCH:**
{cv_text}

**MÔ TẢ CÔNG VIỆC (nếu có):**
{jd_text or "Không có"}

**PHÂN TÍCH CƠ BẢN:**
- Có phần Tóm tắt: {rule_based_result.has_summary}
- Có phần Kỹ năng: {rule_based_result.has_skills}
- Có phần Kinh nghiệm: {rule_based_result.has_experience}
- Có phần Dự án: {rule_based_result.has_projects}
- Có phần Học vấn: {rule_based_result.has_education}
- Số điểm có số liệu: {rule_based_result.quantified_bullet_count}/{rule_based_result.total_bullet_count}

**YÊU CẦU:**
Hãy phân tích CV trên và đưa ra phản hồi chi tiết bằng TIẾNG VIỆT. Trả về kết quả ở định dạng JSON với cấu trúc sau:

{{
  "overall_summary": "Tổng quan về CV (2-3 câu)",
  "strengths": ["Điểm mạnh 1", "Điểm mạnh 2", "Điểm mạnh 3", "..."],
  "weaknesses": ["Điểm yếu 1", "Điểm yếu 2", "Điểm yếu 3", "..."],
  "section_suggestions": [
    {{
      "section_name": "Tên phần (VD: Kỹ năng, Kinh nghiệm)",
      "issues": ["Vấn đề 1", "Vấn đề 2"],
      "suggestions": ["Gợi ý cải thiện 1", "Gợi ý cải thiện 2", "..."]
    }}
  ],
  "rewritten_examples": [
    {{
      "original": "Bullet point gốc từ CV",
      "improved": "Phiên bản cải thiện với số liệu cụ thể",
      "section": "Tên phần (Kinh nghiệm/Dự án)"
    }}
  ]
}}

**LƯU Ý:**
1. Đưa ra ít nhất 3-5 điểm mạnh và 3-5 điểm yếu
2. Phân tích ít nhất 3-4 phần: Kỹ năng, Kinh nghiệm, Dự án, Định dạng
3. Đưa ra 3-4 ví dụ cải thiện bullet points với số liệu cụ thể
4. Phản hồi PHẢI bằng TIẾNG VIỆT
5. Trả về ĐÚNG định dạng JSON, không thêm text khác"""
    
    else:  # English
        return f"""You are a professional CV consultant with years of experience.

**CV TO ANALYZE:**
{cv_text}

**JOB DESCRIPTION (if provided):**
{jd_text or "Not provided"}

**BASIC ANALYSIS:**
- Has Summary section: {rule_based_result.has_summary}
- Has Skills section: {rule_based_result.has_skills}
- Has Experience section: {rule_based_result.has_experience}
- Has Projects section: {rule_based_result.has_projects}
- Has Education section: {rule_based_result.has_education}
- Quantified bullets: {rule_based_result.quantified_bullet_count}/{rule_based_result.total_bullet_count}

**REQUIREMENTS:**
Analyze the CV above and provide detailed feedback in ENGLISH. Return the result in JSON format with this exact structure:

{{
  "overall_summary": "Overall CV assessment (2-3 sentences)",
  "strengths": ["Strength 1", "Strength 2", "Strength 3", "..."],
  "weaknesses": ["Weakness 1", "Weakness 2", "Weakness 3", "..."],
  "section_suggestions": [
    {{
      "section_name": "Section name (e.g., Skills, Experience)",
      "issues": ["Issue 1", "Issue 2"],
      "suggestions": ["Improvement suggestion 1", "Improvement suggestion 2", "..."]
    }}
  ],
  "rewritten_examples": [
    {{
      "original": "Original bullet point from CV",
      "improved": "Improved version with specific metrics",
      "section": "Section name (Experience/Projects)"
    }}
  ]
}}

**NOTES:**
1. Provide at least 3-5 strengths and 3-5 weaknesses
2. Analyze at least 3-4 sections: Skills, Experience, Projects, Formatting
3. Provide 3-4 examples of improved bullet points with specific metrics
4. Response MUST be in ENGLISH
5. Return ONLY valid JSON, no additional text"""
def _generate_mock_feedback(
    cv_text: str,
    jd_text: Optional[str],
    rule_based_result: RuleBasedResult,
    language: str = "en"
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
    
    # Generate overall summary (language-aware)
    if language == "vi":
        missing_sections_vi = []
        if not rule_based_result.has_summary:
            missing_sections_vi.append("tóm tắt chuyên môn")
        if not rule_based_result.has_skills:
            missing_sections_vi.append("phần kỹ năng")
        if not rule_based_result.has_projects:
            missing_sections_vi.append("phần dự án")
        
        overall_summary = (
            f"Đây là một CV {'tốt' if len(missing_sections_vi) == 0 else 'đang phát triển'} cho vị trí kỹ thuật. "
            f"CV thể hiện kinh nghiệm {'vững chắc' if rule_based_result.has_experience else 'hạn chế'} "
            f"và bao gồm {rule_based_result.quantified_bullet_count} thành tích có số liệu cụ thể "
            f"trong tổng số {rule_based_result.total_bullet_count} điểm liệt kê."
        )
        
        if missing_sections_vi:
            overall_summary += f" Tuy nhiên, CV còn thiếu: {', '.join(missing_sections_vi)}."
    else:
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
    
    # Generate strengths (language-aware)
    strengths = []
    if language == "vi":
        if rule_based_result.has_education:
            strengths.append("Có thông tin học vấn rõ ràng")
        if rule_based_result.has_experience:
            strengths.append("Có phần kinh nghiệm làm việc")
        if rule_based_result.has_projects:
            strengths.append("Thể hiện các dự án liên quan")
        if rule_based_result.quantified_bullet_count > 2:
            strengths.append("Một số thành tích được định lượng bằng số liệu")
        if jd_analysis and len(jd_analysis.matched_keywords) > 5:
            strengths.append(f"Khớp tốt với từ khóa JD ({len(jd_analysis.matched_keywords)} từ khớp)")
        
        if len(strengths) < 3:
            strengths.extend([
                "Định dạng có cấu trúc, dễ đọc",
                "Tập trung vào nền tảng kỹ thuật"
            ])
    else:
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
        
        if len(strengths) < 3:
            strengths.extend([
                "Structured format that's easy to scan",
                "Focuses on technical background"
            ])
    
    # Generate weaknesses (language-aware)
    weaknesses = []
    if language == "vi":
        if not rule_based_result.has_summary:
            weaknesses.append("Thiếu phần tóm tắt chuyên môn/mục tiêu nghề nghiệp ở đầu CV")
        if not rule_based_result.has_skills:
            weaknesses.append("Không có phần kỹ năng riêng để làm nổi bật năng lực kỹ thuật")
        if not rule_based_result.has_projects:
            weaknesses.append("Thiếu phần dự án để thể hiện công việc thực tế")
        if rule_based_result.quantified_bullet_count < 3:
            weaknesses.append("Chưa đủ thành tích được định lượng - cần thêm số liệu và chỉ số cụ thể")
        if jd_analysis and len(jd_analysis.missing_keywords) > 5:
            weaknesses.append(f"Thiếu các từ khóa quan trọng từ JD ({len(jd_analysis.missing_keywords)} từ không tìm thấy)")
        
        if len(weaknesses) < 3:
            weaknesses.extend([
                "Các điểm liệt kê có thể hành động hơn",
                "Một số phần có thể cải thiện định dạng"
            ])
    else:
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
        
        if len(weaknesses) < 3:
            weaknesses.extend([
                "Bullet points could be more action-oriented",
                "Some sections could benefit from better formatting"
            ])
    
    # Generate section-specific suggestions
    suggestions_by_section = []
    
    # Skills section (language-aware)
    if language == "vi":
        if not rule_based_result.has_skills:
            suggestions_by_section.append(SectionSuggestions(
                section_name="Kỹ năng",
                issues=["Thiếu hoàn toàn phần kỹ năng"],
                suggestions=[
                    "Thêm phần 'Kỹ năng Kỹ thuật' riêng gần đầu CV",
                    "Nhóm kỹ năng theo danh mục (Ngôn ngữ lập trình, Framework, Công cụ, v.v.)",
                    "Liệt kê các công nghệ cụ thể đã sử dụng trong dự án hoặc công việc"
                ]
            ))
        else:
            suggestions_by_section.append(SectionSuggestions(
                section_name="Kỹ năng",
                issues=["Phần kỹ năng có thể chưa nổi bật"],
                suggestions=[
                    "Đảm bảo phần kỹ năng ở gần đầu để dễ nhìn thấy",
                    "Cân nhắc nhóm kỹ năng theo mức độ thành thạo hoặc danh mục",
                    "Khớp kỹ năng với từ khóa trong mô tả công việc"
                ]
            ))
    else:
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
    
    # Experience section (language-aware)
    if rule_based_result.has_experience:
        if language == "vi":
            suggestions_by_section.append(SectionSuggestions(
                section_name="Kinh nghiệm",
                issues=[
                    "Một số điểm liệt kê thiếu số liệu định lượng",
                    "Động từ hành động có thể mạnh hơn"
                ],
                suggestions=[
                    "Bắt đầu mỗi điểm với động từ hành động mạnh (Phát triển, Triển khai, Tối ưu hóa)",
                    "Thêm số liệu cụ thể: phần trăm, con số, thời gian tiết kiệm, người dùng được tác động",
                    "Theo format STAR: Tình huống, Nhiệm vụ, Hành động, Kết quả",
                    "Tập trung vào tác động và kết quả, không chỉ trách nhiệm"
                ]
            ))
        else:
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
    
    # Projects section (language-aware)
    if language == "vi":
        if rule_based_result.has_projects:
            suggestions_by_section.append(SectionSuggestions(
                section_name="Dự án",
                issues=["Mô tả dự án có thể tác động hơn"],
                suggestions=[
                    "Mô tả vấn đề được giải quyết và công nghệ sử dụng",
                    "Bao gồm link đến GitHub repo hoặc demo trực tiếp nếu có",
                    "Đề cập quy mô nhóm nếu làm việc nhóm, hoặc nhấn mạnh công việc cá nhân",
                    "Định lượng kết quả khi có thể (người dùng, cải thiện hiệu suất)"
                ]
            ))
        else:
            suggestions_by_section.append(SectionSuggestions(
                section_name="Dự án",
                issues=["Thiếu phần dự án"],
                suggestions=[
                    "Thêm 2-4 dự án kỹ thuật liên quan",
                    "Bao gồm dự án học thuật, dự án cá nhân, hoặc hackathon",
                    "Cho mỗi dự án: tên, công nghệ, mô tả ngắn gọn, và tác động"
                ]
            ))
    else:
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
    
    # Summary section (language-aware)
    if not rule_based_result.has_summary:
        if language == "vi":
            suggestions_by_section.append(SectionSuggestions(
                section_name="Tóm tắt",
                issues=["Không có tóm tắt chuyên môn hoặc mục tiêu"],
                suggestions=[
                    "Thêm tóm tắt 2-3 câu ở đầu CV",
                    "Làm nổi bật nền tảng, kỹ năng chính, và mục tiêu nghề nghiệp",
                    "Tùy chỉnh tóm tắt theo vị trí cụ thể đang ứng tuyển"
                ]
            ))
        else:
            suggestions_by_section.append(SectionSuggestions(
                section_name="Summary",
                issues=["No professional summary or objective"],
                suggestions=[
                    "Add a 2-3 sentence summary at the top",
                    "Highlight your background, key skills, and career goals",
                    "Tailor the summary to the specific role you're applying for"
                ]
            ))
    
    # Formatting suggestions (language-aware)
    if language == "vi":
        suggestions_by_section.append(SectionSuggestions(
            section_name="Định dạng",
            issues=["Cần cải thiện định dạng chung"],
            suggestions=[
                "Đảm bảo định dạng ngày tháng nhất quán (ví dụ: 'Tháng 1/2023 - Hiện tại')",
                "Sử dụng tiêu đề phần rõ ràng với khoảng cách phù hợp",
                "Giữ CV trong 1 trang (cho sinh viên/người mới vào nghề)",
                "Sử dụng font chuyên nghiệp, rõ ràng (11-12pt)",
                "Duy trì style điểm liệt kê nhất quán trong toàn bộ CV"
            ]
        ))
    else:
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
    
    # Generate rewritten examples (language-aware)
    if language == "vi":
        rewritten_examples = [
            RewrittenExample(
                original="Làm việc trên dự án machine learning",
                improved="Phát triển bộ phân loại ảnh dựa trên CNN đạt độ chính xác 94% trên 10K+ ảnh, giảm 60% thời gian gán nhãn thủ công",
                section="Dự án"
            ),
            RewrittenExample(
                original="Chịu trách nhiệm quản lý cơ sở dữ liệu",
                improved="Tối ưu hóa các truy vấn PostgreSQL, giảm thời gian phản hồi trung bình từ 2.3s xuống 0.4s và cải thiện trải nghiệm cho 5,000+ người dùng hàng ngày",
                section="Kinh nghiệm"
            ),
            RewrittenExample(
                original="Xây dựng ứng dụng web sử dụng React",
                improved="Thiết kế và triển khai ứng dụng web full-stack React + Node.js với 1,000+ người dùng hoạt động hàng tháng, triển khai xác thực JWT và RESTful APIs",
                section="Dự án"
            ),
            RewrittenExample(
                original="Hỗ trợ nhóm với các tác vụ phát triển phần mềm",
                improved="Cộng tác với nhóm kỹ sư 4 người để hoàn thành 3 tính năng chính đúng hạn, viết 2,000+ dòng code Python và đạt 95% test coverage",
                section="Kinh nghiệm"
            )
        ]
    else:
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
