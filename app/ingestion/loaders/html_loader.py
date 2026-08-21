"""
html_loader.py

Loads HTML documents.
"""

from pathlib import Path

from bs4 import BeautifulSoup

from app.ingestion.loaders.base_loader import BaseLoader

from app.schemas.document import Document
from app.schemas.page import Page
from app.schemas.metadata import Metadata


class HTMLLoader(BaseLoader):

    def load(
        self,
        file_path: Path,
    ) -> Document:


        html = file_path.read_text(
            encoding="utf-8"
        )


        soup = BeautifulSoup(
            html,
            "html.parser"
        )


        text = soup.get_text(
            separator="\n"
        )


        return Document(
            filename=file_path.name,
            filepath=str(file_path),

            metadata=Metadata(),

            pages=[
                Page(
                    page_number=1,
                    text=text.strip(),
                )
            ],
        )