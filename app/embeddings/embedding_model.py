"""
embedding_model.py

Loads a SentenceTransformer model and converts
text into dense normalized vector embeddings.
"""

from sentence_transformers import SentenceTransformer

from app.core.logger import logger


class EmbeddingModel:
    """
    Wrapper around SentenceTransformer.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):

        logger.info(
            f"Loading embedding model: {model_name}"
        )

        self.model = SentenceTransformer(
            model_name
        )

        logger.info(
            "Embedding model loaded successfully."
        )


    def encode(
        self,
        text: str,
    ) -> list[float]:
        """
        Convert text into a normalized embedding vector.
        """


        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )


        return embedding.tolist()