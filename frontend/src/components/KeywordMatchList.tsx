/**
 * Keyword Match List Component
 * Displays JD keyword analysis: matched vs missing keywords.
 */
import React from 'react';
import { JDKeywordAnalysis } from '../types/api';

interface KeywordMatchListProps {
  analysis: JDKeywordAnalysis;
}

const KeywordMatchList: React.FC<KeywordMatchListProps> = ({ analysis }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">🎯 Keyword Match Analysis</h2>
      
      <div className="space-y-6">
        {/* Matched Keywords */}
        <div>
          <h3 className="text-lg font-semibold text-success mb-3 flex items-center gap-2">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            Matched Keywords ({analysis.matched_keywords.length})
          </h3>
          <div className="flex flex-wrap gap-2">
            {analysis.matched_keywords.length > 0 ? (
              analysis.matched_keywords.map((keyword, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium"
                >
                  {keyword}
                </span>
              ))
            ) : (
              <p className="text-gray-500 italic">No matched keywords found</p>
            )}
          </div>
        </div>

        {/* Missing Keywords */}
        <div>
          <h3 className="text-lg font-semibold text-danger mb-3 flex items-center gap-2">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
            Missing Keywords ({analysis.missing_keywords.length})
          </h3>
          <div className="flex flex-wrap gap-2">
            {analysis.missing_keywords.length > 0 ? (
              analysis.missing_keywords.map((keyword, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium"
                >
                  {keyword}
                </span>
              ))
            ) : (
              <p className="text-gray-500 italic">All JD keywords are present in your CV!</p>
            )}
          </div>
        </div>

        {/* Recommendation */}
        {analysis.missing_keywords.length > 0 && (
          <div className="mt-4 p-4 bg-blue-50 rounded-lg border-l-4 border-primary-500">
            <p className="text-sm text-gray-700">
              <strong>💡 Tip:</strong> Consider incorporating the missing keywords into your CV 
              where relevant to better match the job description.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default KeywordMatchList;
