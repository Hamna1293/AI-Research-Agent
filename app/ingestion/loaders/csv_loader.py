"""
csv_loader.py

Loads CSV files.
"""

from pathlib import Path

import pandas as pd

from app.ingestion.loaders.base_loader import BaseLoader

from app.schemas.document import Document
from app.schemas.page import Page
from app.schemas.metadata import Metadata


class CSVLoader(BaseLoader):

    def load(
        self,
        file_path: Path,
    ) -> Document:


        dataframe = pd.read_csv(
            file_path
        )


        text = dataframe.to_string(
            index=False
        )


        return Document(
            filename=file_path.name,
            filepath=str(file_path),

            metadata=Metadata(),

            pages=[
                Page(
                    page_number=1,
                    text=text,
                )
            ],
        )