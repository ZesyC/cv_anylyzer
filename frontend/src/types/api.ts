/**
 * TypeScript type definitions matching backend API models.
 * These ensure type safety when communicating with the FastAPI backend.
 */

export interface CVSectionChecklist {
  has_summary: boolean;
  has_skills: boolean;
  has_experience: boolean;
  has_projects: boolean;
  has_education: boolean;
}

export interface JDKeywordAnalysis {
  jd_keywords: string[];
  matched_keywords: string[];
  missing_keywords: string[];
}

export interface RewrittenExample {
  original: string;
  improved: string;
  section: string;
}

export interface SectionSuggestions {
  section_name: string;
  issues: string[];
  suggestions: string[];
}

export interface CVAnalysisResponse {
  overall_summary: string;
  strengths: string[];
  weaknesses: string[];
  section_checklist: CVSectionChecklist;
  jd_analysis: JDKeywordAnalysis | null;
  suggestions_by_section: SectionSuggestions[];
  rewritten_examples: RewrittenExample[];
}
