/**
 * File Upload Form Component
 * Handles CV file upload and optional Job Description input.
 */
import React, { useState, useRef } from 'react';

interface FileUploadFormProps {
  onSubmit: (file: File, jdText: string) => void;
  isLoading: boolean;
}

const FileUploadForm: React.FC<FileUploadFormProps> = ({ onSubmit, isLoading }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [jdText, setJdText] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedFile) {
      onSubmit(selectedFile, jdText);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Upload Your CV</h2>

      {/* File Upload Area */}
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-primary-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx"
          onChange={handleFileChange}
          className="hidden"
          disabled={isLoading}
        />

        {selectedFile ? (
          <div className="space-y-2">
            <svg
              className="w-16 h-16 mx-auto text-success"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            <p className="text-lg font-semibold text-gray-800">{selectedFile.name}</p>
            <p className="text-sm text-gray-500">
              {(selectedFile.size / 1024).toFixed(2)} KB
            </p>
            <button
              type="button"
              onClick={() => setSelectedFile(null)}
              className="text-sm text-primary-600 hover:text-primary-700 font-medium"
            >
              Choose a different file
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            <svg
              className="w-16 h-16 mx-auto text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
            <p className="text-lg text-gray-700">
              Drag and drop your CV here, or
            </p>
            <button
              type="button"
              onClick={handleBrowseClick}
              className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors font-medium"
            >
              Browse Files
            </button>
            <p className="text-sm text-gray-500">Supports PDF and DOCX (max 10 MB)</p>
          </div>
        )}
      </div>

      {/* Job Description Textarea */}
      <div className="mt-6">
        <label htmlFor="jd-text" className="block text-sm font-semibold text-gray-700 mb-2">
          Job Description (Optional)
        </label>
        <textarea
          id="jd-text"
          value={jdText}
          onChange={(e) => setJdText(e.target.value)}
          placeholder="Paste the job description here to get tailored suggestions..."
          rows={6}
          disabled={isLoading}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none disabled:bg-gray-100 disabled:cursor-not-allowed"
        />
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={!selectedFile || isLoading}
        className="mt-6 w-full py-3 px-6 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-lg font-semibold text-lg hover:from-primary-600 hover:to-primary-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all shadow-md hover:shadow-lg"
      >
        {isLoading ? (
          <span className="flex items-center justify-center gap-2">
            <svg
              className="animate-spin h-5 w-5"
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
            Analyzing...
          </span>
        ) : (
          'Analyze CV'
        )}
      </button>
    </form>
  );
};

export default FileUploadForm;
