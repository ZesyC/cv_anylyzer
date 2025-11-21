export const en = {
  // Header
  header: {
    title: "CV Analyzer",
    subtitle: "Get AI-powered suggestions to improve your resume and stand out to employers"
  },

  // File Upload Form
  upload: {
    title: "Upload Your CV",
    dragDrop: "Drag and drop your CV here, or",
    browse: "Browse Files",
    supportedFormats: "Supports PDF and DOCX (max 10 MB)",
    fileName: "File selected",
    chooseAnother: "Choose a different file",
    jdLabel: "Job Description (Optional)",
    jdPlaceholder: "Paste the job description here to get tailored suggestions...",
    analyzeButton: "Analyze CV",
    analyzing: "Analyzing..."
  },

  // Analysis Result
  analysis: {
    title: "Analysis Results",
    overallSummary: "Overall Summary",
    strengths: "Strengths",
    weaknesses: "Areas for Improvement",
    detailedSuggestions: "Detailed Suggestions",
    backToTop: "↑ Back to Top",
    analyzeAnother: "← Analyze Another CV"
  },

  // Section Checklist
  sections: {
    title: "📋 Section Checklist",
    professionalSummary: "Professional Summary",
    skills: "Skills",
    experience: "Experience",
    projects: "Projects",
    education: "Education",
    present: "Present",
    missing: "Missing"
  },

  // Keyword Match
  keywords: {
    title: "🎯 Keyword Match Analysis",
    matched: "Matched Keywords",
    missing: "Missing Keywords",
    noMatched: "No matched keywords found",
    allPresent: "All JD keywords are present in your CV!",
    tip: "💡 Tip:",
    tipText: "Consider incorporating the missing keywords into your CV where relevant to better match the job description."
  },

  // Suggestions
  suggestions: {
    issuesFound: "Issues Found:",
    suggestions: "Suggestions:",
    exampleImprovements: "Example Improvements:",
    example: "Example",
    original: "Original:",
    improved: "Improved:"
  },

  // Error States
  error: {
    title: "Analysis Failed"
  },

  // Loading States
  loading: {
    title: "Analyzing Your CV...",
    subtitle: "Extracting text, detecting sections, and generating personalized feedback"
  },

  // Empty State
  empty: {
    title: "Ready to improve your CV?",
    subtitle: "Upload your resume above to get started with AI-powered analysis and suggestions"
  },

  // Footer
  footer: {
    builtWith: "Built with Zéy"
  }
};

export type TranslationKeys = typeof en;
