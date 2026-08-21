"""
embedding.py

Schema representing a chunk together with
its embedding vector.
"""

from pydantic import BaseModel

from app.schemas.chunk import Chunk


class EmbeddedChunk(BaseModel):
    """
    Represents one embedded chunk.
    """

    chunk: Chunk

    embedding: list[float]