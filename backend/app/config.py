"""
Configuration constants for the CV Analyzer application.
"""

# LLM Configuration (for future real API integration)
LLM_MODEL_NAME = "gpt-4"  # TODO: Replace with actual model when integrating real API
LLM_MAX_TOKENS = 2000
LLM_TEMPERATURE = 0.7

# File Upload Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = [".pdf", ".docx"]

# Analysis Configuration
MIN_QUANTIFIED_BULLETS = 3  # Minimum number of quantified bullets expected
