"""
routes.py

FastAPI API routes.
"""

from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile
from fastapi import HTTPException
from fastapi import BackgroundTasks

from app.schemas.upload_response import UploadResponse
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.document_info import DocumentInfo

from app.services.upload_job_manager import upload_job_manager
from app.services.upload_worker import upload_worker
from app.services.upload_service import UploadService
from app.services.chat_service import ChatService
from app.services.report_service import ReportService

from app.services.insight_service import InsightService

from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile
from fastapi import HTTPException
from fastapi import BackgroundTasks

import shutil

from app.core.config import RAW_DOCUMENT_DIR
from app.core.logger import logger
router = APIRouter()


upload_service = UploadService()

chat_service = ChatService()

report_service = ReportService()
insight_service = InsightService()


@router.get("/")
def root():

    return {
        "message": "Welcome to AI Research Assistant",
        "docs": "/docs",
        "health": "/health",
    }



@router.get("/health")
def health():

    return {
        "status": "ok",
        "message": "Research Assistant is running.",
    }



@router.post(
    "/upload",
    response_model=UploadResponse,
)
def upload_document(
    file: UploadFile = File(...),
):
    """
    Upload and process any supported research document.

    Supported:
    - PDF
    - TXT
    - DOCX
    - HTML
    - CSV
    - XLSX
    - PPTX
    """


    return upload_service.process_upload(
        file
    )



@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):

    answer = chat_service.ask(
        question=request.question,
        top_k=request.top_k,
    )


    return ChatResponse(
        answer=answer,
    )



@router.get(
    "/documents",
    response_model=list[DocumentInfo],
)
def list_documents():

    return upload_service.list_documents()



@router.delete(
    "/documents/{filename}",
)
def delete_document(
    filename: str,
):

    try:

        return upload_service.delete_document(
            filename
        )


    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )



@router.get(
    "/report/{filename}",
)
def get_report(
    filename: str,
):

    report = report_service.get_report(
        filename
    )


    return {
        "filename": filename,
        "report": report,
    }
    
@router.get(
    "/insights/{filename}",
)
def get_insights(
    filename: str,
):
    """
    Return research papers related to
    the selected indexed paper.
    """

    return {
        "filename": filename,
        "insights": insight_service.get_insights(
            filename=filename,
            top_k=10,
        ),
    }
    
# ==========================================================
# START BACKGROUND UPLOAD
# ==========================================================

@router.post("/upload/start")
async def start_upload(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    """
    Start document processing in the background.

    The uploaded file is first saved to disk.
    The background worker then processes the saved file.
    """

    # ------------------------------------------------------
    # 1. Get filename
    # ------------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is missing.",
        )

    filename = file.filename

    # ------------------------------------------------------
    # 2. Create upload job
    # ------------------------------------------------------

    job = upload_job_manager.create_job(
        filename
    )

    # ------------------------------------------------------
    # 3. Create upload directory
    # ------------------------------------------------------

    RAW_DOCUMENT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ------------------------------------------------------
    # 4. Define destination
    # ------------------------------------------------------

    destination = (
        RAW_DOCUMENT_DIR / filename
    )

    # ------------------------------------------------------
    # 5. Save uploaded file
    # ------------------------------------------------------

    try:

        with open(
            destination,
            "wb",
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer,
            )

        logger.info(
            f"Background upload file saved: {filename}"
        )

    except Exception as e:

        logger.exception(
            f"Failed to save upload: {filename}"
        )

        upload_job_manager.fail(
            job.job_id,
            str(e),
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to save uploaded document.",
        )

    finally:

        await file.close()

    # ------------------------------------------------------
    # 6. Start background processing
    # ------------------------------------------------------

    background_tasks.add_task(
        upload_worker.process,
        job.job_id,
        str(destination),
        filename,
    )

    # ------------------------------------------------------
    # 7. Return job information
    # ------------------------------------------------------

    return {
        "job_id": job.job_id,
        "filename": job.filename,
        "status": job.status,
        "progress": job.progress,
        "stage": job.stage,
    }

# ==========================================================
# CANCEL UPLOAD
# ==========================================================

@router.post("/upload/cancel/{job_id}")
def cancel_upload(
    job_id: str,
):
    """
    Request cancellation of an upload.
    """

    job = upload_job_manager.get_job(
        job_id
    )

    if job is None:

        raise HTTPException(
            status_code=404,
            detail="Upload job not found.",
        )

    if job.status == "completed":

        raise HTTPException(
            status_code=400,
            detail="Upload has already completed.",
        )

    if job.status == "cancelled":

        return {
            "job_id": job.job_id,
            "status": "cancelled",
            "message": "Upload is already cancelled.",
        }

    cancelled = upload_job_manager.cancel(
        job_id
    )

    if not cancelled:

        raise HTTPException(
            status_code=400,
            detail="Unable to cancel upload.",
        )

    return {
        "job_id": job.job_id,
        "status": "cancelled",
        "message": "Upload cancellation requested.",
    }