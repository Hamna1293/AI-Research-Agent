from pydantic import BaseModel


class ChatResponse(BaseModel):
    """
    Chat response.
    """

    answer: str