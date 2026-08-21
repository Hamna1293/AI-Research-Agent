"""
title_extractor.py

Extracts the title of a research paper from
the first page.
"""

from app.core.logger import logger


class TitleExtractor:
    """
    Extract the title from the first page of a paper.
    """

    def __init__(self):
        logger.info("TitleExtractor initialized.")

    def extract(self, first_page: str) -> str:
        """
        Extract the paper title.

        Strategy:
        - Skip Google's permission notice.
        - Find the line 'Attention Is All You Need'.
        - Later we'll make this work for all papers.
        """

        lines = [
            line.strip()
            for line in first_page.splitlines()
            if line.strip()
        ]

        for i, line in enumerate(lines):

            # Ignore Google permission notice
            if (
                "Provided proper attribution" in line
                or "reproduce the tables" in line
                or "scholarly works." in line
            ):
                continue

            # Ignore emails
            if "@" in line:
                continue

            # Ignore affiliations
            if "Google Brain" in line:
                continue

            if "Google Research" in line:
                continue

            if "University of Toronto" in line:
                continue

            # Ignore very short lines
            if len(line) < 10:
                continue

            # Ignore long paragraphs
            if len(line) > 120:
                continue

            # Ignore Abstract
            if line.lower() == "abstract":
                continue

            # Ignore numbered headings
            if line.startswith("1 "):
                continue

            # This is probably the title
            return line

        return ""