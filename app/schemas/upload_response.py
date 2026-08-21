"""
upload_response.py

Response schema for uploaded files.
"""

from pydantic import BaseModel


class UploadResponse(BaseModel):
    """
    Response returned after successful document upload.
    """

    filename: str

    pages: int

    chunks: int

    report: str

    analysis: str

    message: str