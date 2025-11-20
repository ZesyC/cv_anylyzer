/**
 * Main Application Component
 * Manages the overall app state and layout.
 */
import { useState } from 'react';
import FileUploadForm from './components/FileUploadForm';
import AnalysisResult from './components/AnalysisResult';
import { analyzeCV } from './services/apiClient';
import { CVAnalysisResponse } from './types/api';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<CVAnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyzeCV = async (file: File, jdText: string) => {
    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const result = await analyzeCV(file, jdText);
      setAnalysisResult(result);
      // Scroll to results smoothly
      setTimeout(() => {
        const resultsElement = document.getElementById('results-section');
        resultsElement?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(errorMessage);
      console.error('Analysis error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setError(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-primary-800">
            CV Analyzer
          </h1>
          <p className="text-gray-600 mt-2">
            Get AI-powered suggestions to improve your resume and stand out to employers
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Upload Section */}
        <div className="mb-8">
          <FileUploadForm onSubmit={handleAnalyzeCV} isLoading={isLoading} />
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 bg-red-50 border-l-4 border-danger rounded-lg p-4 animate-fade-in">
            <div className="flex items-start gap-3">
              <svg
                className="w-6 h-6 text-danger flex-shrink-0 mt-0.5"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
              <div>
                <h3 className="font-semibold text-danger mb-1">Analysis Failed</h3>
                <p className="text-gray-700 text-sm">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="bg-white rounded-lg shadow-md p-12 text-center animate-fade-in">
            <div className="flex flex-col items-center gap-4">
              <svg
                className="animate-spin h-12 w-12 text-primary-500"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              <div>
                <h3 className="text-xl font-semibold text-gray-800 mb-2">Analyzing Your CV...</h3>
                <p className="text-gray-600">
                  Extracting text, detecting sections, and generating personalized feedback
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Results Section */}
        {analysisResult && !isLoading && (
          <div id="results-section">
            <div className="mb-4 flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-800">Your CV Analysis</h2>
              <button
                onClick={handleReset}
                className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors font-medium"
              >
                ← Analyze Another CV
              </button>
            </div>
            <AnalysisResult result={analysisResult} />
          </div>
        )}

        {/* Empty State */}
        {!isLoading && !analysisResult && !error && (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <svg
              className="w-24 h-24 mx-auto text-gray-300 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              Ready to improve your CV?
            </h3>
            <p className="text-gray-500">
              Upload your resume above to get started with AI-powered analysis and suggestions
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <p className="text-center text-gray-600 text-sm">
            Built with Zéy
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
