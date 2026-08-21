from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    Request body for chat endpoint.
    """

    question: str
    top_k: int = 5


class ChatResponse(BaseModel):
    """
    Response body for chat endpoint.
    """

    answer: str