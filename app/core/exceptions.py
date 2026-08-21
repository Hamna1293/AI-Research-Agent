"""
exceptions.py

Global exception handlers for the AI Research Assistant.
"""

from fastapi import HTTPException
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logger import logger


# ==========================================================
# HTTP Exceptions
# ==========================================================

async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:

    logger.warning(
        f"{request.method} {request.url.path} | "
        f"{exc.status_code} | {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": "HTTPException",
            "message": exc.detail,
        },
    )


# ==========================================================
# Validation Exceptions
# ==========================================================

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:

    logger.warning(
        f"Validation error on "
        f"{request.method} {request.url.path}"
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "ValidationError",
            "message": exc.errors(),
        },
    )


# ==========================================================
# Unexpected Exceptions
# ==========================================================

async def general_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    logger.exception(
        f"Unhandled exception on "
        f"{request.method} {request.url.path}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "InternalServerError",
            "message": (
                "An unexpected server error occurred."
            ),
        },
    )
    
from fastapi import FastAPI


def register_exception_handlers(
    app: FastAPI,
) -> None:

    app.exception_handler(
        HTTPException
    )(http_exception_handler)

    app.exception_handler(
        RequestValidationError
    )(validation_exception_handler)

    app.exception_handler(
        Exception
    )(general_exception_handler)