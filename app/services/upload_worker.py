"""
upload_worker.py

Runs document processing in the background while updating
upload progress and respecting cancellation requests.

The existing UploadService pipeline is reused unchanged.
"""

from pathlib import Path

from fastapi import UploadFile

from app.core.config import RAW_DOCUMENT_DIR
from app.core.logger import logger

from app.services.upload_job_manager import upload_job_manager
from app.services.upload_service import UploadService


class UploadWorker:
    """
    Background worker for document uploads.
    """

    def __init__(self):

        self.upload_service = UploadService()

    # ==========================================================
    # PROCESS
    # ==========================================================

    def process(
        self,
        job_id: str,
        file_path: str,
        filename: str,
    ) -> None:
        """
        Process an already-saved document in the background.

        The file is saved by the API route first.
        The worker then opens the saved file itself so it does
        not depend on FastAPI's request-scoped UploadFile.
        """

        try:

            # ==================================================
            # START
            # ==================================================

            if upload_job_manager.is_cancelled(job_id):

                logger.info(
                    f"Upload {job_id} cancelled before processing."
                )

                return

            upload_job_manager.start(
                job_id
            )

            logger.info(
                f"Background upload started: {job_id}"
            )

            # ==================================================
            # VALIDATION
            # ==================================================

            upload_job_manager.update(
                job_id=job_id,
                progress=5,
                stage="Validating document...",
            )

            if upload_job_manager.is_cancelled(job_id):

                logger.info(
                    f"Upload {job_id} cancelled during validation."
                )

                return

            path = Path(file_path)

            if not path.exists():

                upload_job_manager.fail(
                    job_id,
                    f"Uploaded file not found: {filename}",
                )

                return

            # ==================================================
            # LOADING
            # ==================================================

            upload_job_manager.update(
                job_id=job_id,
                progress=10,
                stage="Loading research document...",
            )

            if upload_job_manager.is_cancelled(job_id):

                logger.info(
                    f"Upload {job_id} cancelled before loading."
                )

                return

            logger.info(
                f"Opening saved document: {path}"
            )

            # ==================================================
            # CREATE A NEW UPLOADFILE
            # ==================================================
            #
            # IMPORTANT:
            #
            # We create a NEW UploadFile from the saved file.
            #
            # This means the background worker does not depend on
            # the original request's UploadFile object.
            #

            with open(
                path,
                "rb",
            ) as file_object:

                background_file = UploadFile(
                    file=file_object,
                    filename=filename,
                )

                # ==============================================
                # EXISTING PIPELINE
                # ==============================================

                upload_job_manager.update(
                    job_id=job_id,
                    progress=20,
                    stage="Analyzing research document...",
                )

                if upload_job_manager.is_cancelled(job_id):

                    logger.info(
                        f"Upload {job_id} cancelled before analysis."
                    )

                    return

                result = self.upload_service.process_upload(
                    background_file
                )

            # ==================================================
            # PIPELINE FINISHED
            # ==================================================

            if upload_job_manager.is_cancelled(job_id):

                logger.info(
                    f"Upload {job_id} cancelled after processing."
                )

                return

            # ==================================================
            # FINALIZATION
            # ==================================================

            upload_job_manager.update(
                job_id=job_id,
                progress=95,
                stage="Finalizing upload...",
            )

            if upload_job_manager.is_cancelled(job_id):

                logger.info(
                    f"Upload {job_id} cancelled during finalization."
                )

                return

            # ==================================================
            # COMPLETE
            # ==================================================

            upload_job_manager.complete(
                job_id
            )

            logger.info(
                f"Background upload completed successfully: "
                f"{filename}"
            )

        except Exception as e:

            logger.exception(
                f"Background upload failed: {job_id}"
            )

            upload_job_manager.fail(
                job_id,
                str(e),
            )


# ==============================================================
# GLOBAL WORKER
# ==============================================================

upload_worker = UploadWorker()