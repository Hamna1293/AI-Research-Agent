"""
chroma_manager.py

Stores and retrieves embeddings using ChromaDB.
"""

from typing import Any

from chromadb import PersistentClient

from app.core.config import VECTOR_DB_DIR
from app.core.logger import logger
from app.schemas.embedding import EmbeddedChunk


class ChromaManager:
    """
    Handles all interactions with ChromaDB.
    """


    def __init__(
        self,
        persist_directory: str = str(VECTOR_DB_DIR),
        collection_name: str = "research_documents",
    ):

        self.client = PersistentClient(
            path=persist_directory
        )


        self.collection_name = collection_name


        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name,
                metadata={
                    "hnsw:space": "cosine"
                },
            )
        )


        logger.info(
            "ChromaDB initialized."
        )



    def add_documents(
        self,
        embedded_chunks: list[EmbeddedChunk],
    ) -> None:
        """
        Store embedded chunks in ChromaDB.
        """


        if not embedded_chunks:

            logger.warning(
                "No chunks provided for storage."
            )

            return


        logger.info(
            f"Adding {len(embedded_chunks)} chunk(s)..."
        )


        self.collection.upsert(

            ids=[
                chunk.chunk.chunk_id
                for chunk in embedded_chunks
            ],


            embeddings=[
                chunk.embedding
                for chunk in embedded_chunks
            ],


            documents=[
                chunk.chunk.text
                for chunk in embedded_chunks
            ],


            metadatas=[

                {
                    "page": chunk.chunk.page_number,

                    "document": chunk.chunk.document_name,

                    "chunk_index": chunk.chunk.chunk_index,

                }

                for chunk in embedded_chunks

            ],

        )


        logger.info(
            "Chunks stored successfully."
        )



    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> dict[str, Any]:
        """
        Search the vector database.

        Returns a normal dictionary so Retriever
        can process results easily.
        """


        logger.info(
            f"Searching top {top_k} chunk(s)..."
        )


        try:

            results = (
                self.collection.query(

                    query_embeddings=[
                        query_embedding
                    ],

                    n_results=top_k,

                )
            )


            return {

                "documents": results.get(
                    "documents",
                    [],
                ),

                "metadatas": results.get(
                    "metadatas",
                    [],
                ),

                "distances": results.get(
                    "distances",
                    [],
                ),

            }


        except Exception:

            logger.exception(
                "Chroma search failed."
            )


            return {

                "documents": [],

                "metadatas": [],

                "distances": [],

            }



    def delete_document(
        self,
        document_name: str,
    ) -> None:
        """
        Delete all chunks belonging to a document.
        """


        logger.info(
            f"Deleting vectors for {document_name}"
        )


        self.collection.delete(

            where={
                "document": document_name,
            }

        )


        logger.info(
            "Document vectors deleted."
        )



    def document_exists(
        self,
        document_name: str,
    ) -> bool:
        """
        Check whether a document exists.
        """


        results = (
            self.collection.get(

                where={
                    "document": document_name,
                }

            )
        )


        return bool(
            results.get(
                "ids",
                []
            )
        )



    def count(
        self,
    ) -> int:
        """
        Return total stored vectors.
        """


        return self.collection.count()



    def clear(
        self,
    ) -> None:
        """
        Delete collection and recreate it.
        """


        logger.info(
            "Clearing ChromaDB collection..."
        )


        self.client.delete_collection(
            self.collection_name
        )


        self.collection = (
            self.client.get_or_create_collection(

                name=self.collection_name,

                metadata={
                    "hnsw:space": "cosine"
                },

            )
        )


        logger.info(
            "Collection recreated successfully."
        )
        