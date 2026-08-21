"""
chunker.py

Creates overlapping text chunks from documents.
"""

import re

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.logger import logger
from app.schemas.chunk import Chunk
from app.schemas.document import Document


class Chunker:
    """
    Creates overlapping text chunks from documents.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ) -> None:

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                " ",
                "",
            ],
        )

        logger.info(
            f"Chunker initialized "
            f"(size={chunk_size}, overlap={chunk_overlap})"
        )


    def chunk_document(
        self,
        document: Document,
    ) -> list[Chunk]:
        """
        Split document pages into chunks.
        """

        chunks: list[Chunk] = []

        chunk_index = 0


        safe_filename = re.sub(
            r"[^a-zA-Z0-9_-]",
            "_",
            document.filename,
        )


        for page in document.pages:

            if not page.text.strip():

                continue


            page_chunks = (
                self.splitter.split_text(
                    page.text
                )
            )


            for chunk_text in page_chunks:

                if not chunk_text.strip():

                    continue


                chunk = Chunk(

                    chunk_id=(
                        f"{safe_filename}_"
                        f"{page.page_number}_"
                        f"{chunk_index}"
                    ),

                    document_name=document.filename,

                    page_number=page.page_number,

                    chunk_index=chunk_index,

                    text=chunk_text,

                    character_count=len(chunk_text),

                )


                chunks.append(
                    chunk
                )


                chunk_index += 1


        logger.info(
            f"Created {len(chunks)} chunks "
            f"from {document.filename}"
        )


        return chunks