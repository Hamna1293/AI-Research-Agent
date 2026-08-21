"""
text_cleaner.py

This module cleans text extracted from PDF files before
it is passed to the chunking and embedding pipeline.
"""

import re
import unicodedata

from app.core.logger import logger


class TextCleaner:
    """
    Cleans extracted PDF text while preserving the
    semantic meaning of research papers.
    """

    def __init__(self):
        logger.info("TextCleaner initialized.")

    def normalize_unicode(self, text: str) -> str:
        """
        Normalize unicode characters.
        """

        return unicodedata.normalize("NFKC", text)

    def remove_extra_spaces(self, text: str) -> str:
        """
        Replace multiple spaces with a single space.
        """

        return re.sub(r"[ \t]+", " ", text)

    def remove_extra_blank_lines(self, text: str) -> str:
        """
        Replace multiple blank lines with a single blank line.
        """

        return re.sub(r"\n\s*\n+", "\n\n", text)

    def remove_trailing_spaces(self, text: str) -> str:
        """
        Remove leading and trailing spaces from every line.
        """

        return "\n".join(
        line.strip()
        for line in text.splitlines()
    )

    def clean_text(self, text: str) -> str:
        """
        Complete cleaning pipeline.
        """

        logger.info("Cleaning text...")

        text = self.normalize_unicode(text)
        text = self.remove_trailing_spaces(text)
        text = self.remove_extra_spaces(text)
        text = self.remove_extra_blank_lines(text)

        return text.strip()