"""
main.py

FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.exceptions import register_exception_handlers


app = FastAPI(
    title="AI Research Assistant",
    description=(
        "An AI-powered research assistant "
        "using RAG, embeddings, ChromaDB and Groq."
    ),
    version="1.0.0",
)


# ==========================================================
# Global Exception Handlers
# ==========================================================

register_exception_handlers(app)


# ==========================================================
# CORS Configuration
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# API Routes
# ==========================================================

app.include_router(router)