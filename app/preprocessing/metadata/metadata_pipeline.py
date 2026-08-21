"""
metadata_pipeline.py

Combines all metadata extractors into one pipeline.
"""

from app.core.logger import logger

from app.preprocessing.metadata.title_extractor import TitleExtractor
from app.preprocessing.metadata.author_extractor import AuthorExtractor
from app.preprocessing.metadata.abstract_extractor import AbstractExtractor


class MetadataPipeline:
    """
    Runs all metadata extractors.
    """

    def __init__(self):

        logger.info("MetadataPipeline initialized.")

        self.title_extractor = TitleExtractor()
        self.author_extractor = AuthorExtractor()
        self.abstract_extractor = AbstractExtractor()

    def extract(self, first_page: str) -> dict:

        metadata = {
            "title": self.title_extractor.extract(first_page),
            "authors": self.author_extractor.extract(first_page),
            "abstract": self.abstract_extractor.extract(first_page),
        }

        return metadata