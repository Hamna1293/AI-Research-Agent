"""
document_info.py

Schema representing an uploaded research document.
"""

from pydantic import BaseModel


class DocumentInfo(BaseModel):
    """
    Information about one uploaded document.
    """

    filename: str
    pages: int
    chunks: int