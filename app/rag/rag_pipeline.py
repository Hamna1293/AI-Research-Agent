"""
rag_pipeline.py

Complete Retrieval-Augmented Generation pipeline.
"""

from app.core.logger import logger

from app.retrieval.retriever import Retriever
from app.rag.prompt_builder import PromptBuilder
from app.rag.llm import LLM


class RAGPipeline:
    """
    Complete Retrieval-Augmented Generation pipeline.
    """


    def __init__(self):

        self.retriever = Retriever()

        self.prompt_builder = PromptBuilder()

        self.llm = LLM()

        logger.info(
            "RAG Pipeline initialized."
        )


    def answer(
        self,
        question: str,
        top_k: int = 5,
    ) -> str:
        """
        Generate an answer using retrieved context.
        """

        retrieved_chunks = self.retriever.search(
            query=question,
            top_k=top_k,
        )


        prompt = self.prompt_builder.build(
            query=question,
            retrieved_chunks=retrieved_chunks,
        )


        answer = self.llm.generate(
            prompt
        )


        return answer