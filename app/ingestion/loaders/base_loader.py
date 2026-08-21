"""
base_loader.py

Abstract base class for all document loaders.
"""

from abc import ABC
from abc import abstractmethod

from pathlib import Path

from app.schemas.document import Document


class BaseLoader(ABC):
    """
    Base class for all document loaders.
    """

    @abstractmethod
    def load(
        self,
        file_path: Path,
    ) -> Document:
        """
        Load a document and return a Document object.
        """
        pass