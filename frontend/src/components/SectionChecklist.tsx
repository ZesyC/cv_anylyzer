/**
 * Section Checklist Component
 * Displays which CV sections are present or missing with visual indicators.
 */
import React from 'react';
import { CVSectionChecklist } from '../types/api';

interface SectionChecklistProps {
  checklist: CVSectionChecklist;
}

const SectionChecklistComponent: React.FC<SectionChecklistProps> = ({ checklist }) => {
  const sections = [
    { name: 'Professional Summary', key: 'has_summary' as keyof CVSectionChecklist },
    { name: 'Skills', key: 'has_skills' as keyof CVSectionChecklist },
    { name: 'Experience', key: 'has_experience' as keyof CVSectionChecklist },
    { name: 'Projects', key: 'has_projects' as keyof CVSectionChecklist },
    { name: 'Education', key: 'has_education' as keyof CVSectionChecklist },
  ];

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">📋 Section Checklist</h2>
      <div className="space-y-3">
        {sections.map((section) => {
          const isPresent = checklist[section.key];
          return (
            <div
              key={section.key}
              className="flex items-center justify-between p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors"
            >
              <span className="text-gray-700 font-medium">{section.name}</span>
              <div className="flex items-center gap-2">
                {isPresent ? (
                  <>
                    <span className="text-success text-sm font-semibold">Present</span>
                    <svg
                      className="w-6 h-6 text-success"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </>
                ) : (
                  <>
                    <span className="text-danger text-sm font-semibold">Missing</span>
                    <svg
                      className="w-6 h-6 text-danger"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default SectionChecklistComponent;
