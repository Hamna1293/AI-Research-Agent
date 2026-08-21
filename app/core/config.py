"""
config.py

Central configuration file for the AI Research Assistant.

Defines project paths and loads environment variables.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()


# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ==========================================================
# Data Directories
# ==========================================================

DATA_DIR = PROJECT_ROOT / "data"


# All uploaded research documents
# Supports:
# PDF, TXT, DOCX, HTML, CSV, XLSX, PPTX
RAW_DOCUMENT_DIR = DATA_DIR / "raw_documents"
# Backward compatibility for old PDF tests
RAW_PDF_DIR = RAW_DOCUMENT_DIR

PROCESSED_DIR = DATA_DIR / "processed"


CHUNK_DIR = DATA_DIR / "chunks"


VECTOR_DB_DIR = DATA_DIR / "vector_db"


REPORTS_DIR = DATA_DIR / "reports"



# ==========================================================
# Automatically Create Directories
# ==========================================================

DIRECTORIES = [

    DATA_DIR,

    RAW_DOCUMENT_DIR,

    PROCESSED_DIR,

    CHUNK_DIR,

    VECTOR_DB_DIR,

    REPORTS_DIR,

]


for directory in DIRECTORIES:

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# LLM Configuration
# ==========================================================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)


GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)


if not GROQ_API_KEY:

    raise ValueError(
        "GROQ_API_KEY not found. Please add it to your .env file."
    )