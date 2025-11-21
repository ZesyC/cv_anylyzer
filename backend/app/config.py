"""
Configuration constants for the CV Analyzer application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LLM Configuration (for future real API integration)
LLM_MODEL_NAME = "gpt-4"  # TODO: Replace with actual model when integrating real API
LLM_MAX_TOKENS = 2000
LLM_TEMPERATURE = 0.7

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
# Only use Gemini if API key is set and not the placeholder
USE_GEMINI_API = bool(GEMINI_API_KEY and GEMINI_API_KEY != "API key" and len(GEMINI_API_KEY) > 10)

# File Upload Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = [".pdf", ".docx"]

# Analysis Configuration
MIN_QUANTIFIED_BULLETS = 3  # Minimum number of quantified bullets expected
