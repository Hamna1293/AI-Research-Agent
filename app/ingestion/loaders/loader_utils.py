"""
loader_utils.py

Shared helper functions for document loaders.
"""

from pathlib import Path

from app.schemas.metadata import Metadata


def create_default_metadata(
    file_path: Path,
    pages: int,
) -> Metadata:
    """
    Create default metadata for non-PDF documents.
    """

    return Metadata(
        title=file_path.stem,
        author="",
        subject="",
        keywords="",
        creator="",
        producer="",
        creation_date="",
        modification_date="",
        pages=pages,
    )