/**
 * Analysis Result Component
 * Container for displaying all CV analysis results.
 */
import React from 'react';
import { CVAnalysisResponse } from '../types/api';
import SectionChecklist from './SectionChecklist';
import KeywordMatchList from './KeywordMatchList';
import SuggestionCard from './SuggestionCard';

interface AnalysisResultProps {
  result: CVAnalysisResponse;
}

const AnalysisResult: React.FC<AnalysisResultProps> = ({ result }) => {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">Analysis Results</h2>
        
        {/* Overall Summary */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Overall Summary</h3>
          <p className="text-gray-600 leading-relaxed">{result.overall_summary}</p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Strengths */}
          <div className="bg-green-50 rounded-lg p-4 border-l-4 border-success">
            <h3 className="text-lg font-semibold text-success mb-3 flex items-center gap-2">
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
              </svg>
              Strengths
            </h3>
            <ul className="list-disc list-inside space-y-1">
              {result.strengths.map((strength, idx) => (
                <li key={idx} className="text-gray-700 text-sm">{strength}</li>
              ))}
            </ul>
          </div>

          {/* Weaknesses */}
          <div className="bg-red-50 rounded-lg p-4 border-l-4 border-danger">
            <h3 className="text-lg font-semibold text-danger mb-3 flex items-center gap-2">
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path d="M18 9.5a1.5 1.5 0 11-3 0v-6a1.5 1.5 0 013 0v6zM14 9.667v-5.43a2 2 0 00-1.105-1.79l-.05-.025A4 4 0 0011.055 2H5.64a2 2 0 00-1.962 1.608l-1.2 6A2 2 0 004.44 12H8v4a2 2 0 002 2 1 1 0 001-1v-.667a4 4 0 01.8-2.4l1.4-1.866a4 4 0 00.8-2.4z" />
              </svg>
              Areas for Improvement
            </h3>
            <ul className="list-disc list-inside space-y-1">
              {result.weaknesses.map((weakness, idx) => (
                <li key={idx} className="text-gray-700 text-sm">{weakness}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Section Checklist */}
      <SectionChecklist checklist={result.section_checklist} />

      {/* Keyword Analysis (if JD was provided) */}
      {result.jd_analysis && <KeywordMatchList analysis={result.jd_analysis} />}

      {/* Section Suggestions */}
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Detailed Suggestions</h2>
        <div className="grid gap-6">
          {result.suggestions_by_section.map((suggestion, idx) => (
            <SuggestionCard
              key={idx}
              suggestion={suggestion}
              examples={result.rewritten_examples}
            />
          ))}
        </div>
      </div>

      {/* Scroll to Top Button */}
      <div className="flex justify-center pt-6">
        <button
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          className="px-6 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg font-medium transition-colors"
        >
          ↑ Back to Top
        </button>
      </div>
    </div>
  );
};

export default AnalysisResult;
