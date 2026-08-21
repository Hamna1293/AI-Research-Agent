"""
embedding_generator.py

Generates embeddings for document chunks.
"""

from app.core.logger import logger

from app.embeddings.embedding_model import EmbeddingModel

from app.schemas.chunk import Chunk
from app.schemas.embedding import EmbeddedChunk


class EmbeddingGenerator:
    """
    Generates embeddings for chunks.
    """

    def __init__(self):

        self.model = EmbeddingModel()

        logger.info(
            "EmbeddingGenerator initialized."
        )

    def generate(
        self,
        chunks: list[Chunk],
    ) -> list[EmbeddedChunk]:

        embedded_chunks: list[EmbeddedChunk] = []

        for chunk in chunks:

            embedding = self.model.encode(
                chunk.text
            )

            embedded_chunk = EmbeddedChunk(
                chunk=chunk,
                embedding=embedding,
            )

            embedded_chunks.append(
                embedded_chunk
            )

        logger.info(
            f"Generated embeddings for {len(embedded_chunks)} chunk(s)."
        )

        return embedded_chunks