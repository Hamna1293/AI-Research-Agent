"""
analysis_storage.py

Stores extracted research paper information.
"""

import json
from pathlib import Path

from app.core.config import PROCESSED_DIR
from app.core.logger import logger



class AnalysisStorage:
    """
    Saves structured research analysis as JSON.
    """


    def __init__(self):

        self.directory = PROCESSED_DIR

        logger.info(
            "AnalysisStorage initialized."
        )


    def save(
        self,
        filename: str,
        analysis: dict,
    ) -> Path:
        """
        Save research analysis JSON.
        """

        json_filename = (
            Path(filename).stem
            + "_analysis.json"
        )

        path = self.directory / json_filename


        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                analysis,
                file,
                indent=4,
                ensure_ascii=False,
            )


        logger.info(
            f"Research analysis saved: {path}"
        )


        return path



    def exists(
        self,
        filename: str,
    ) -> bool:

        path = (
            self.directory
            /
            (
                Path(filename).stem
                +
                "_analysis.json"
            )
        )

        return path.exists()



    def delete(
        self,
        filename: str,
    ) -> None:

        path = (
            self.directory
            /
            (
                Path(filename).stem
                +
                "_analysis.json"
            )
        )

        if path.exists():

            path.unlink()

            logger.info(
                f"Deleted analysis: {path}"
            )