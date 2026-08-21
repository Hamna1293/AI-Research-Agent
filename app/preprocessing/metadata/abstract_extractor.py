"""
abstract_extractor.py

Extracts the abstract from the first page
of a research paper.
"""

import re

from app.core.logger import logger


class AbstractExtractor:
    """
    Extract the abstract section from a research paper.
    """

    def __init__(self):
        logger.info("AbstractExtractor initialized.")

    def extract(self, first_page: str) -> str:
        """
        Extract abstract text from the first page.
        """

        # Find the word "Abstract"
        start = first_page.find("Abstract")

        if start == -1:
            logger.warning("Abstract heading not found.")
            return ""

        # Everything after "Abstract"
        text = first_page[start + len("Abstract"):]

        # Possible endings of the abstract
        end_markers = [
            "∗Equal contribution",
            "†Work performed",
            "‡Work performed",
            "31st Conference",
            "Neural Information Processing Systems",
            "arXiv:",
        ]

        end = len(text)

        for marker in end_markers:

            position = text.find(marker)

            if position != -1:
                end = min(end, position)

        abstract = text[:end].strip()

        # Normalize whitespace
        abstract = re.sub(r"\s+", " ", abstract)

        return abstract