"""
author_extractor.py

Extracts author names from the first page of a
research paper.
"""

import re

from app.core.logger import logger


class AuthorExtractor:
    """
    Extract author names from the first page.
    """

    def __init__(self):
        logger.info("AuthorExtractor initialized.")

    def extract(self, first_page: str) -> list[str]:
        """
        Extract probable author names.
        """

        authors = []

        lines = [
            line.strip()
            for line in first_page.splitlines()
            if line.strip()
        ]

        for line in lines:

            # Skip emails
            if "@" in line:
                continue

            # Skip affiliations
            if (
                "Google" in line
                or "University" in line
                or "Institute" in line
                or "Laboratory" in line
                or "School" in line
                or "Department" in line
            ):
                continue

            # Remove common footnote symbols
            cleaned = (
                line.replace("*", "")
                .replace("†", "")
                .replace("‡", "")
                .strip()
            )

            # Simple heuristic for person names
            if re.fullmatch(
                r"[A-Z][A-Za-z.\-']+(?:\s+[A-Z][A-Za-z.\-']+){1,5}",
                cleaned,
            ):
                authors.append(cleaned)

        # Remove duplicates while preserving order
        unique_authors = []
        for author in authors:
            if author not in unique_authors:
                unique_authors.append(author)

        return unique_authors