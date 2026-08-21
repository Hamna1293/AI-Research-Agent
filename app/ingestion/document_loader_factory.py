"""
document_loader_factory.py

Returns the correct loader based on file extension.
"""

from pathlib import Path

from app.ingestion.loaders.pdf_loader import PDFLoader
from app.ingestion.loaders.txt_loader import TXTLoader
from app.ingestion.loaders.docx_loader import DOCXLoader
from app.ingestion.loaders.html_loader import HTMLLoader
from app.ingestion.loaders.csv_loader import CSVLoader
from app.ingestion.loaders.excel_loader import ExcelLoader
from app.ingestion.loaders.ppt_loader import PPTLoader

from app.core.config import RAW_DOCUMENT_DIR

class DocumentLoaderFactory:
    """
    Factory for selecting the correct document loader.
    """

    @staticmethod
    def get_loader(
        file_path: Path,
    ):

        extension = file_path.suffix.lower()

        if extension == ".pdf":
            return PDFLoader(
                pdf_directory=RAW_DOCUMENT_DIR
            )

        if extension == ".txt":
            return TXTLoader()

        if extension == ".docx":
            return DOCXLoader()

        if extension == ".html":
            return HTMLLoader()

        if extension == ".csv":
            return CSVLoader()

        if extension in [
            ".xlsx",
            ".xls",
        ]:
            return ExcelLoader()

        if extension in [
            ".ppt",
            ".pptx",
        ]:
            return PPTLoader()

        raise ValueError(
            f"Unsupported file type: {extension}"
        )