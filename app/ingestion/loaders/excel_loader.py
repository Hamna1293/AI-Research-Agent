from pathlib import Path

import pandas as pd

from app.ingestion.loaders.base_loader import BaseLoader

from app.schemas.document import Document
from app.schemas.page import Page
from app.schemas.metadata import Metadata


class ExcelLoader(BaseLoader):

    def load(
        self,
        file_path: Path,
    ) -> Document:


        sheets = pd.read_excel(
            file_path,
            sheet_name=None
        )


        text = ""


        for name, dataframe in sheets.items():

            text += f"\nSheet: {name}\n"

            text += dataframe.to_string(
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