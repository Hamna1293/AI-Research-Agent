"""
txt_loader.py

Loads plain text files.
"""

from pathlib import Path

from app.ingestion.loaders.base_loader import BaseLoader
from app.ingestion.loaders.loader_utils import (
    create_default_metadata,
)

from app.schemas.document import Document
from app.schemas.page import Page


class TXTLoader(BaseLoader):
    """
    Loads plain text (.txt) documents.
    """

    def load(
        self,
        file_path: Path,
    ) -> Document:
        """
        Load a TXT file and return a Document.
        """

        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        page = Page(
            page_number=1,
            text=text,
        )

        return Document(
            filename=file_path.name,
            filepath=str(file_path),
            metadata=create_default_metadata(
                file_path=file_path,
                pages=1,
            ),
            pages=[page],
        )