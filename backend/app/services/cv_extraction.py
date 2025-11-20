"""
CV text extraction service.
Handles extraction of text from PDF and DOCX files.
"""
import io
from typing import Union
import pdfplumber
from docx import Document


def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        file_content: Raw bytes of the PDF file
        
    Returns:
        Extracted text as a single string
    """
    text_parts = []
    
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    
    return "\n".join(text_parts)


def extract_text_from_docx(file_content: bytes) -> str:
    """
    Extract text from a DOCX file.
    
    Args:
        file_content: Raw bytes of the DOCX file
        
    Returns:
        Extracted text as a single string
    """
    doc = Document(io.BytesIO(file_content))
    text_parts = []
    
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text_parts.append(paragraph.text)
    
    return "\n".join(text_parts)


def extract_cv_text(file_content: bytes, filename: str) -> str:
    """
    Unified interface for extracting text from CV files.
    Automatically detects file type based on extension.
    
    Args:
        file_content: Raw bytes of the file
        filename: Original filename (used to detect file type)
        
    Returns:
        Extracted text as a single string
        
    Raises:
        ValueError: If file type is not supported
    """
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.pdf'):
        return extract_text_from_pdf(file_content)
    elif filename_lower.endswith('.docx'):
        return extract_text_from_docx(file_content)
    else:
        raise ValueError(f"Unsupported file type: {filename}")
