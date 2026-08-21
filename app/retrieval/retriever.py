"""
retriever.py

Semantic retrieval from ChromaDB.
"""

from typing import Any

from app.core.logger import logger

from app.embeddings.embedding_model import EmbeddingModel
from app.vectorstore.chroma_manager import ChromaManager



class Retriever:
    """
    Retrieves the most relevant chunks from ChromaDB.
    """


    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.vector_store = ChromaManager()

        logger.info(
            "Retriever initialized."
        )



    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Search for the most relevant chunks.
        """


        logger.info(
            f"Searching for: {query}"
        )


        query_embedding = self.embedding_model.encode(
            query
        )


        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )


        documents = results.get(
            "documents"
        )

        metadatas = results.get(
            "metadatas"
        )

        distances = results.get(
            "distances"
        )


        if (
            not documents
            or not metadatas
            or not distances
        ):

            logger.warning(
                "No search results returned."
            )

            return []



        documents = documents[0]

        metadatas = metadatas[0]

        distances = distances[0]



        retrieved_chunks: list[dict[str, Any]] = []



        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):

            retrieved_chunks.append(
                {
                    "text": document,

                    "document": metadata.get(
                        "document",
                        "",
                    ),

                    "page": metadata.get(
                        "page",
                        0,
                    ),

                    "chunk_index": metadata.get(
                        "chunk_index",
                        0,
                    ),

                    "similarity": round(
                        1 - distance,
                        4,
                    ),
                }
            )



        logger.info(
            f"Retrieved {len(retrieved_chunks)} chunk(s)."
        )


        return retrieved_chunks