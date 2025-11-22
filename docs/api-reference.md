# API Reference

## Overview

The CV Analyzer API provides endpoints for analyzing resumes against job descriptions and extracting actionable insights.

**Base URL**: `http://localhost:8000`

**API Documentation**: `http://localhost:8000/docs` (Swagger UI)

## Authentication

Currently, the API does not require authentication. For production deployments, consider implementing:

- API key authentication
- JWT tokens
- OAuth 2.0

## Endpoints

### Analyze CV

Analyzes a resume and returns structured improvement suggestions.

**Endpoint**: `POST /api/analyze-cv`

**Content-Type**: `multipart/form-data`

#### Request Parameters

| Parameter | Type   | Required | Description                               |
| --------- | ------ | -------- | ----------------------------------------- |
| `cv_file` | File   | Yes      | Resume file (PDF or DOCX format)          |
| `jd_text` | string | No       | Job description text for keyword matching |

#### Request Example

```bash
curl -X POST "http://localhost:8000/api/analyze-cv" \
  -F "cv_file=@/path/to/resume.pdf" \
  -F "jd_text=Seeking Python developer with FastAPI and Docker experience"
```

#### Response Schema

```json
{
  "overall_summary": "string",
  "strengths": ["string"],
  "weaknesses": ["string"],
  "section_checklist": {
    "has_summary": boolean,
    "has_skills": boolean,
    "has_experience": boolean,
    "has_projects": boolean,
    "has_education": boolean
  },
  "jd_analysis": {
    "jd_keywords": ["string"],
    "matched_keywords": ["string"],
    "missing_keywords": ["string"]
  },
  "suggestions_by_section": [
    {
      "section_name": "string",
      "issues": ["string"],
      "suggestions": ["string"]
    }
  ],
  "rewritten_examples": [
    {
      "original": "string",
      "improved": "string",
      "section": "string"
    }
  ]
}
```

#### Response Fields

##### Overall Summary

- **Type**: `string`
- **Description**: Comprehensive assessment of the resume quality

##### Strengths

- **Type**: `array<string>`
- **Description**: List of identified strengths in the resume

##### Weaknesses

- **Type**: `array<string>`
- **Description**: List of identified weaknesses

##### Section Checklist

Object indicating presence of key resume sections:

- `has_summary`: Professional summary section
- `has_skills`: Skills section
- `has_experience`: Work experience section
- `has_projects`: Projects section
- `has_education`: Education section

##### JD Analysis

Keyword analysis when job description is provided:

- `jd_keywords`: Keywords extracted from job description
- `matched_keywords`: Keywords found in resume
- `missing_keywords`: Keywords missing from resume

##### Suggestions by Section

Array of section-specific improvement suggestions:

- `section_name`: Name of the resume section
- `issues`: Identified problems
- `suggestions`: Recommended improvements

##### Rewritten Examples

Array of before/after examples:

- `original`: Original text from resume
- `improved`: Enhanced version
- `section`: Section where text appears

#### Success Response

**Status Code**: `200 OK`

```json
{
  "overall_summary": "Strong technical resume with clear experience section. Missing professional summary.",
  "strengths": [
    "Clear technical skills section with relevant technologies",
    "Quantified achievements in work experience",
    "Well-structured project descriptions"
  ],
  "weaknesses": [
    "Missing professional summary at the top",
    "Limited use of action verbs",
    "Some bullet points lack metrics"
  ],
  "section_checklist": {
    "has_summary": false,
    "has_skills": true,
    "has_experience": true,
    "has_projects": true,
    "has_education": true
  },
  "jd_analysis": {
    "jd_keywords": ["python", "fastapi", "docker", "kubernetes", "ci/cd"],
    "matched_keywords": ["python", "docker"],
    "missing_keywords": ["fastapi", "kubernetes", "ci/cd"]
  },
  "suggestions_by_section": [
    {
      "section_name": "Experience",
      "issues": ["Several bullet points lack quantification"],
      "suggestions": [
        "Add specific metrics (percentages, numbers, time saved)",
        "Use strong action verbs to start each bullet point"
      ]
    },
    {
      "section_name": "Skills",
      "issues": ["Missing keywords from job description"],
      "suggestions": [
        "Add FastAPI if you have experience with it",
        "Include CI/CD tools if applicable"
      ]
    }
  ],
  "rewritten_examples": [
    {
      "original": "Worked on backend development using Python",
      "improved": "Architected and deployed scalable backend services using Python and FastAPI, reducing API response time by 40% and handling 10K+ requests/day",
      "section": "Experience"
    }
  ]
}
```

#### Error Responses

##### 400 Bad Request

Invalid file format or missing required parameters.

```json
{
  "detail": "Invalid file format. Only PDF and DOCX are supported."
}
```

##### 413 Payload Too Large

File exceeds maximum size limit (10 MB).

```json
{
  "detail": "File size exceeds maximum limit of 10 MB."
}
```

##### 422 Unprocessable Entity

Validation error in request parameters.

```json
{
  "detail": [
    {
      "loc": ["body", "cv_file"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

##### 500 Internal Server Error

Server-side error during processing.

```json
{
  "detail": "An error occurred while processing your request."
}
```

## Rate Limiting

When using the Gemini API:

**Gemini 1.5 Flash** (Default):

- 15 requests per minute
- 1 million tokens per minute
- 1,500 requests per day

**Gemini 1.5 Pro**:

- 2 requests per minute
- 32,000 tokens per minute

**Note**: The application automatically falls back to mock data when rate limits are exceeded.

## File Upload Constraints

- **Maximum file size**: 10 MB
- **Supported formats**: PDF, DOCX
- **Encoding**: UTF-8 recommended

## CORS Configuration

The API is configured to accept requests from:

- `http://localhost:5173` (development)
- `http://localhost:3000` (alternative dev port)

For production, update CORS origins in `backend/app/main.py`.

## Health Check

**Endpoint**: `GET /`

**Response**:

```json
{
  "status": "ok",
  "message": "CV Analyzer API is running"
}
```

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Use these interfaces to:

- Test API endpoints
- View request/response schemas
- Download OpenAPI specification
