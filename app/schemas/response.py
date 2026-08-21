"""
response.py

Response schemas.
"""

from pydantic import BaseModel


class ChatResponse(BaseModel):

    answer: str