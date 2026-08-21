"""
llm.py

Groq LLM wrapper for RAG generation.
"""

from groq import Groq

from app.core.config import GROQ_API_KEY
from app.core.logger import logger


class LLM:
    """
    Groq LLM wrapper.
    """


    MAX_PROMPT_CHARS = 60000


    def __init__(self) -> None:

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

        self.model = (
            "openai/gpt-oss-120b"
        )

        logger.info(
            f"Groq initialized with model: {self.model}"
        )



    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate response from Groq.
        """


        logger.info(
            "Generating Groq response..."
        )


        original_length = len(prompt)


        if original_length > self.MAX_PROMPT_CHARS:

            logger.warning(
                f"Prompt too large "
                f"({original_length} chars). "
                f"Truncating."
            )

            prompt = prompt[
                :self.MAX_PROMPT_CHARS
            ]


        logger.info(
            f"Final prompt characters: {len(prompt)}"
        )


        try:

            response = (
                self.client.chat.completions.create(

                    model=self.model,

                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],

                    temperature=0.2,

                    max_tokens=1500,

                )
            )


            if not response.choices:

                logger.error(
                    "Groq returned no choices."
                )

                return (
                    "No response generated."
                )


            answer = (
                response
                .choices[0]
                .message
                .content
            )


            if answer is None:

                return (
                    "No response generated."
                )


            logger.info(
                "Groq response generated."
            )


            return answer



        except Exception as e:

            logger.exception(
                f"Groq generation failed: {e}"
            )

            raise e