from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    Chat request.
    """

    question: str

    top_k: int = 5