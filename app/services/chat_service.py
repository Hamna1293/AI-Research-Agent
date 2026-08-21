from app.rag.rag_pipeline import RAGPipeline


class ChatService:

    def __init__(self):

        self.pipeline = RAGPipeline()

    def ask(
        self,
        question: str,
        top_k: int = 5,
    ) -> str:

        return self.pipeline.answer(
            question=question,
            top_k=top_k,
        )