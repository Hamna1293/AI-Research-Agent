"""
pdf_loader.py

Load PDF research papers and convert them into
Document, Metadata, and Page schema objects.
"""

from pathlib import Path
from typing import cast

import fitz

from app.core.logger import logger
from app.ingestion.loaders.base_loader import BaseLoader
from app.schemas.document import Document
from app.schemas.metadata import Metadata
from app.schemas.page import Page


class PDFLoader(BaseLoader):
    """
    Handles loading PDF files from a directory.
    """

    def __init__(
        self,
        pdf_directory: str | Path,
    ):

        self.pdf_directory = Path(
            pdf_directory
        )

        logger.info(
            f"PDF directory set to: {self.pdf_directory}"
        )

    def load_directory(
        self,
    ) -> list[Path]:
        """
        Locate all PDF files inside the configured directory.
        """

        if not self.pdf_directory.exists():

            raise FileNotFoundError(
                f"Directory not found: {self.pdf_directory}"
            )

        pdf_files = sorted(
            self.pdf_directory.glob(
                "*.pdf"
            )
        )

        if not pdf_files:

            raise FileNotFoundError(
                f"No PDF files found in {self.pdf_directory}"
            )

        logger.info(
            f"Found {len(pdf_files)} PDF file(s)."
        )

        return pdf_files

    def extract_metadata(
        self,
        pdf_document: fitz.Document,
    ) -> Metadata:
        """
        Extract metadata from a PDF.
        """

        metadata = pdf_document.metadata or {}

        return Metadata(
            title=metadata.get("title", ""),
            author=metadata.get("author", ""),
            subject=metadata.get("subject", ""),
            keywords=metadata.get("keywords", ""),
            creator=metadata.get("creator", ""),
            producer=metadata.get("producer", ""),
            creation_date=metadata.get(
                "creationDate",
                "",
            ),
            modification_date=metadata.get(
                "modDate",
                "",
            ),
            pages=len(pdf_document),
        )

    def extract_pages(
        self,
        pdf_document: fitz.Document,
    ) -> list[Page]:
        """
        Extract every page from the PDF.
        """

        pages: list[Page] = []

        for page_index in range(
            len(pdf_document)
        ):

            page = cast(
                fitz.Page,
                pdf_document.load_page(
                    page_index
                ),
            )

            text = page.get_text( # type: ignore
                "text"
            ).strip()

            pages.append(
                Page(
                    page_number=page_index + 1,
                    text=text,
                )
            )

        logger.info(
            f"Extracted {len(pages)} page(s)."
        )

        return pages

    def load(
        self,
        file_path: Path,
    ) -> Document:
        """
        Load a single PDF and return a Document object.
        """

        logger.info(
            f"Processing PDF: {file_path.name}"
        )

        pdf_document = fitz.open(
            file_path
        )

        try:

            metadata = self.extract_metadata(
                pdf_document
            )

            pages = self.extract_pages(
                pdf_document
            )

        finally:

            pdf_document.close()

        document = Document(
            filename=file_path.name,
            filepath=str(file_path),
            metadata=metadata,
            pages=pages,
        )

        logger.info(
            f"Finished processing: {file_path.name}"
        )

        return document

    def process_directory(
        self,
    ) -> list[Document]:
        """
        Process every PDF inside the configured directory.
        """

        documents: list[Document] = []

        for pdf_path in self.load_directory():

            documents.append(
                self.load(
                    pdf_path
                )
            )

        logger.info(
            f"Successfully processed {len(documents)} document(s)."
        )

        return documents