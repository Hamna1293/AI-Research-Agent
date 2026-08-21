"""
prompt_builder.py

Builds prompts for the LLM using retrieved context.
"""

from typing import Any

from app.core.logger import logger



class PromptBuilder:
    """
    Builds prompts for the LLM.
    """


    def __init__(self):

        logger.info(
            "PromptBuilder initialized."
        )



    def build(
        self,
        query: str,
        retrieved_chunks: list[dict[str, Any]],
    ) -> str:
        """
        Create the final prompt for the LLM.
        """


        if not retrieved_chunks:

            context = (
                "No relevant context was retrieved "
                "from the documents."
            )


        else:

            context = ""


            for chunk in retrieved_chunks:


                context += (

                    f"[Document: {chunk.get('document', '')} | "

                    f"Page: {chunk.get('page', '')} | "

                    f"Similarity: "
                    f"{chunk.get('similarity', 0)}]\n"

                    f"{chunk.get('text', '')}\n\n"

                )



        prompt = f"""
You are an expert AI Research Assistant.

Your task is to answer the user's question ONLY using the provided document context.

Rules:
- Use only the information available in the context.
- Do not use outside knowledge.
- Do not hallucinate facts.
- If the answer is not available, reply exactly:

"I could not find the answer in the provided documents."

- When possible, mention the document name and page number supporting the answer.


-------------------------
Document Context
-------------------------

{context}


-------------------------
User Question
-------------------------

{query}


-------------------------
Answer
-------------------------
"""


        return prompt