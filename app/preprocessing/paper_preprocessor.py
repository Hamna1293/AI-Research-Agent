"""
paper_preprocessor.py

Cleans extracted document text before
sending it to the LLM.
"""

import re

from app.core.logger import logger
from app.schemas.document import Document


class PaperPreprocessor:
    """
    Cleans extracted documents for AI analysis.
    """

    def __init__(self) -> None:

        logger.info(
            "PaperPreprocessor initialized."
        )


    def preprocess(
        self,
        document: Document,
    ) -> str:
        """
        Convert a Document into clean text.
        """

        logger.info(
            "Preprocessing document..."
        )


        pages = []


        for page in document.pages:

            text = page.text.strip()


            if not text:

                continue


            pages.append(
                text
            )


        document_text = "\n\n".join(
            pages
        )


        document_text = self._normalize(
            document_text
        )


        logger.info(
            f"Preprocessed text size: "
            f"{len(document_text)} characters"
        )


        logger.info(
            "Document preprocessing completed."
        )


        return document_text



    def _normalize(
        self,
        text: str,
    ) -> str:
        """
        Normalize whitespace.
        """


        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )


        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )


        return text.strip()