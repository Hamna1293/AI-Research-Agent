
"""
upload_service.py

Processes uploaded research documents.
"""

import shutil

from fastapi import HTTPException, UploadFile

from app.core.config import RAW_DOCUMENT_DIR
from app.core.logger import logger

from app.ingestion.document_loader_factory import DocumentLoaderFactory

from app.preprocessing.paper_preprocessor import PaperPreprocessor
from app.preprocessing.chunker import Chunker

from app.analysis.report_generator import ReportGenerator
from app.analysis.research_extractor import ResearchExtractor
from app.analysis.analysis_storage import AnalysisStorage

from app.storage.report_storage import ReportStorage

from app.embeddings.embedding_generator import EmbeddingGenerator

from app.vectorstore.chroma_manager import ChromaManager

class UploadService:
    """
    Handles the complete document upload pipeline.
    """

    def __init__(self):

        self.preprocessor = PaperPreprocessor()

        self.report_generator = ReportGenerator()

        self.report_storage = ReportStorage()

        self.extractor = ResearchExtractor()

        self.analysis_storage = AnalysisStorage()

        self.chunker = Chunker()

        self.embedder = EmbeddingGenerator()

        self.vector_store = ChromaManager()


    def process_upload(
        self,
        uploaded_file: UploadFile,
    ) -> dict[str, str | int]:
        """
        Upload, analyze, embed and store a research document.
        """


        # =====================================================
        # Validate upload
        # =====================================================

        if uploaded_file.filename is None:

            raise HTTPException(
                status_code=400,
                detail="Filename is missing.",
            )


        filename = uploaded_file.filename


        supported_extensions = [
            ".pdf",
            ".txt",
            ".docx",
            ".html",
            ".csv",
            ".xlsx",
            ".xls",
            ".ppt",
            ".pptx",
        ]


        extension = "." + filename.split(".")[-1].lower()


        if extension not in supported_extensions:

            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {extension}",
            )


        # =====================================================
        # Save uploaded document
        # =====================================================

        destination = RAW_DOCUMENT_DIR / filename


        with open(
            destination,
            "wb",
        ) as buffer:

            shutil.copyfileobj(
                uploaded_file.file,
                buffer,
            )


        logger.info(
            f"Saved document: {filename}"
        )


        # =====================================================
        # Load document using factory
        # =====================================================

        loader = DocumentLoaderFactory.get_loader(
            destination
        )


        document = loader.load(
            destination
        )


        # =====================================================
        # Preprocess document
        # =====================================================

        paper_text = self.preprocessor.preprocess(
            document
        )


        # =====================================================
        # Extract structured research knowledge
        # =====================================================

        analysis = self.extractor.extract(
            paper_text
        )


        analysis_path = self.analysis_storage.save(
            filename=document.filename,
            analysis=analysis,
        )


        logger.info(
            "Analysis completed successfully."
        )


        # =====================================================
        # Generate educational report
        # =====================================================

        try:

            report = self.report_generator.generate(
                paper_text
        )

        except Exception as e:

            logger.exception(
                "Report generation failed."
        )

            report = (
                "# Report Generation Failed\n\n"
                "The document was uploaded successfully, "
                "but the AI report could not be generated "
                "because the language model was unavailable."
            )
                    
        report_path = self.report_storage.save(
            filename=document.filename,
            report=report,
        )


        logger.info(
            "Report completed successfully."
        )

        # =====================================================
        # Create chunks
        # =====================================================

        chunks = self.chunker.chunk_document(
            document
        )


        # =====================================================
        # Generate embeddings
        # =====================================================

        embedded_chunks = self.embedder.generate(
            chunks
        )


        # =====================================================
        # Remove old vectors
        # =====================================================

        self.vector_store.delete_document(
            document.filename
        )


        # =====================================================
        # Store vectors
        # =====================================================

        self.vector_store.add_documents(
            embedded_chunks
        )


        logger.info(
            f"{document.filename} processed successfully."
        )


        return {

            "filename": document.filename,

            "pages": len(document.pages),

            "chunks": len(chunks),

            "report": str(report_path),

            "analysis": str(analysis_path),

            "message": "Upload successful.",

        }



    def list_documents(
        self,
    ) -> list[dict[str, str | int]]:
        """
        Return information about all uploaded documents.
        """


        documents = []


        for file_path in RAW_DOCUMENT_DIR.iterdir():

            if file_path.is_file():

                loader = DocumentLoaderFactory.get_loader(
                    file_path
                )


                document = loader.load(
                    file_path
                )


                documents.append(
                    document
                )


        document_list = []


        for document in documents:

            chunks = self.chunker.chunk_document(
                document
            )


            document_list.append(
                {

                    "filename": document.filename,

                    "pages": len(document.pages),

                    "chunks": len(chunks),

                }
            )


        return document_list



    def delete_document(
        self,
        filename: str,
    ) -> dict[str, str]:
        """
        Delete a document, report, analysis and vectors.
        """


        document_path = RAW_DOCUMENT_DIR / filename


        if not document_path.exists():

            raise FileNotFoundError(
                f"{filename} does not exist."
            )


        # =====================================================
        # Delete vectors
        # =====================================================

        self.vector_store.delete_document(
            filename
        )


        # =====================================================
        # Delete report
        # =====================================================

        if self.report_storage.exists(
            filename
        ):

            self.report_storage.delete(
                filename
            )


        # =====================================================
        # Delete extracted analysis
        # =====================================================

        if self.analysis_storage.exists(
            filename
        ):

            self.analysis_storage.delete(
                filename
            )


        # =====================================================
        # Delete original file
        # =====================================================

        document_path.unlink()


        logger.info(
            f"Deleted {filename}"
        )


        return {

            "message":
            f"{filename} deleted successfully."

        }