"""
chunk.py

Schema representing one chunk of a document.
"""

from pydantic import BaseModel


class Chunk(BaseModel):
    """
    Represents one text chunk.
    """

    chunk_id: str

    document_name: str

    page_number: int

    chunk_index: int

    text: str

    character_count: int