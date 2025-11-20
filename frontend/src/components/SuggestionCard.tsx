/**
 * Suggestion Card Component
 * Displays improvement suggestions for a specific CV section.
 */
import React, { useState } from 'react';
import { SectionSuggestions, RewrittenExample } from '../types/api';

interface SuggestionCardProps {
  suggestion: SectionSuggestions;
  examples: RewrittenExample[];
}

const SuggestionCard: React.FC<SuggestionCardProps> = ({ suggestion, examples }) => {
  const sectionExamples = examples.filter((ex) => ex.section === suggestion.section_name);
  const [expandedExample, setExpandedExample] = useState<number | null>(null);

  const getSectionIcon = (sectionName: string) => {
    const icons: { [key: string]: string } = {
      'Skills': '',
      'Experience': '',
      'Projects': '',
      'Summary': '',
      'Education': '',
      'Formatting': '',
    };
    return icons[sectionName] || '';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        <span>{getSectionIcon(suggestion.section_name)}</span>
        {suggestion.section_name}
      </h3>

      {/* Issues */}
      {suggestion.issues.length > 0 && (
        <div className="mb-4">
          <h4 className="font-semibold text-red-600 mb-2">Issues Found:</h4>
          <ul className="list-disc list-inside space-y-1">
            {suggestion.issues.map((issue, idx) => (
              <li key={idx} className="text-gray-700 text-sm">{issue}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Suggestions */}
      {suggestion.suggestions.length > 0 && (
        <div className="mb-4">
          <h4 className="font-semibold text-green-600 mb-2">Suggestions:</h4>
          <ul className="list-disc list-inside space-y-1">
            {suggestion.suggestions.map((sug, idx) => (
              <li key={idx} className="text-gray-700 text-sm">{sug}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Rewritten Examples */}
      {sectionExamples.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <h4 className="font-semibold text-primary-600 mb-3">Example Improvements:</h4>
          <div className="space-y-3">
            {sectionExamples.map((example, idx) => (
              <div
                key={idx}
                className="bg-gray-50 rounded-lg p-3 cursor-pointer hover:bg-gray-100 transition-colors"
                onClick={() => setExpandedExample(expandedExample === idx ? null : idx)}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold text-gray-600">Example {idx + 1}</span>
                  <svg
                    className={`w-5 h-5 text-gray-500 transform transition-transform ${
                      expandedExample === idx ? 'rotate-180' : ''
                    }`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 9l-7 7-7-7"
                    />
                  </svg>
                </div>
                
                {expandedExample === idx && (
                  <div className="space-y-2 animate-fade-in">
                    <div>
                      <p className="text-xs font-semibold text-red-600 mb-1">Original:</p>
                      <p className="text-sm text-gray-700 italic">{example.original}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-green-600 mb-1">Improved:</p>
                      <p className="text-sm text-gray-800 font-medium">{example.improved}</p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SuggestionCard;
