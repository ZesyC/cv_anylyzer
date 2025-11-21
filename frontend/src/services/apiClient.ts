/**
 * API client for communicating with the FastAPI backend.
 */
import axios from 'axios';
import { CVAnalysisResponse } from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Analyze a CV file and optionally compare with a Job Description.
 * 
 * @param cvFile - The CV file (PDF or DOCX)
 * @param jdText - Optional Job Description text
 * @returns Analysis results from the backend
 */
export async function analyzeCV(
  cvFile: File,
  jdText?: string,
  language?: string
): Promise<CVAnalysisResponse> {
  const formData = new FormData();
  formData.append('cv_file', cvFile);
  
  if (jdText && jdText.trim()) {
    formData.append('jd_text', jdText.trim());
  }
  
  if (language) {
    formData.append('language', language);
  }

  try {
    const response = await axios.post<CVAnalysisResponse>(
      `${API_BASE_URL}/api/analyze-cv`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || error.message;
      throw new Error(`Failed to analyze CV: ${message}`);
    }
    throw error;
  }
}
