"""
report_service.py

Handles loading AI-generated research reports.
"""

from pathlib import Path

from fastapi import HTTPException

from app.core.logger import logger
from app.storage.report_storage import ReportStorage


class ReportService:
    """
    Service for accessing stored reports.
    """

    def __init__(self):

        self.storage = ReportStorage()

    def get_report(
        self,
        filename: str,
    ) -> str:
        """
        Load a generated research report.
        """

        report_name = Path(filename).stem + ".md"

        report_path = (
            self.storage.report_directory /
            report_name
        )

        logger.info("=" * 60)
        logger.info(f"Requested filename : {filename}")
        logger.info(f"Expected report    : {report_name}")
        logger.info(f"Searching path     : {report_path}")
        logger.info(f"File exists        : {report_path.exists()}")
        logger.info("=" * 60)

        if not report_path.exists():

            raise HTTPException(
                status_code=404,
                detail=f"Report not found.\nExpected location:\n{report_path}",
            )

        try:

            report = report_path.read_text(
                encoding="utf-8"
            )

            logger.info(
                f"Successfully loaded report: {report_name}"
            )

            return report

        except Exception as e:

            logger.exception(
                "Failed to read report."
            )

            raise HTTPException(
                status_code=500,
                detail=str(e),
            )