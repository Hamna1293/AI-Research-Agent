"""
report_storage.py

Handles saving and loading AI-generated
research reports.
"""

from pathlib import Path

from app.core.config import REPORTS_DIR
from app.core.logger import logger


class ReportStorage:
    """
    Saves and loads research reports.
    """

    def __init__(self):

        self.report_directory = REPORTS_DIR
        
        self.report_directory.mkdir(
        parents=True,
        exist_ok=True
        )
        logger.info(
            "ReportStorage initialized."
        )
        
    def save(
        self,
        filename: str,
        report: str,
    ) -> Path:
        """
        Save a report as a Markdown file.
        """

        report_name = (
            Path(filename).stem + ".md"
        )
        

        report_path = (
            self.report_directory /
            report_name
        )     
        if not report or not report.strip():

            raise ValueError(
                "Cannot save empty report."
            )

        report_path.write_text(
            report,
            encoding="utf-8",
        )

        logger.info(
            f"Saved report: {report_name}"
        )

        return report_path

    def load(
        self,
        filename: str,
    ) -> str:
        """
        Load a saved report.
        """

        report_name = (
            Path(filename).stem + ".md"
        )

        report_path = (
            self.report_directory /
            report_name
        )

        if not report_path.exists():

            raise FileNotFoundError(
                f"Report not found: {report_name}"
            )

        return report_path.read_text(
            encoding="utf-8"
        )

    def exists(
        self,
        filename: str,
    ) -> bool:
        """
        Check whether a report already exists.
        """

        report_name = (
            Path(filename).stem + ".md"
        )

        return (
            self.report_directory /
            report_name
        ).exists()

    def delete(
        self,
        filename: str,
    ) -> None:
        """
        Delete a report.
        """

        report_name = (
            Path(filename).stem + ".md"
        )

        report_path = (
            self.report_directory /
            report_name
        )

        if report_path.exists():

            report_path.unlink()

            logger.info(
                f"Deleted report: {report_name}"
            )