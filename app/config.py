
import os
from pathlib import Path
from dotenv import load_dotenv

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load root .env file
load_dotenv(BASE_DIR / ".env")

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash-lite"
)

# Application configuration
APP_NAME = "AI-Powered Website Link Analysis API"
APP_VERSION = "1.0.0"

# Website extraction limits
REQUEST_TIMEOUT = 15
MAX_HTML_SIZE = 2 * 1024 * 1024
MAX_CONTENT_LENGTH = 12000
