from pydantic import BaseModel

from app.schemas.metadata import Metadata
from app.schemas.page import Page


class Document(BaseModel):
    filename: str
    filepath: str
    metadata: Metadata
    pages: list[Page]