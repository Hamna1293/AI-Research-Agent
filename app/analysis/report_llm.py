"""
report_llm.py

Dedicated Groq LLM wrapper for research report generation.

IMPORTANT:
- Independent from the existing RAG/Chat LLM.
- Used only by ReportGenerator.
- Does not modify Chat or Insights.
"""

import time

from groq import Groq

from app.core.config import GROQ_API_KEY
from app.core.logger import logger


class ReportLLM:
    """
    Dedicated Groq LLM wrapper for research reports.
    """

    MODEL = "openai/gpt-oss-120b"

    # Keep the request safely bounded.
    MAX_PROMPT_CHARS = 7500

    # Enough room for a useful educational report.
    MAX_OUTPUT_TOKENS = 2048

    MAX_RETRIES = 2

    def __init__(self) -> None:

        if not GROQ_API_KEY:

            raise ValueError(
                "GROQ_API_KEY is missing or empty."
            )

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

        logger.info(
            f"ReportLLM initialized with model: "
            f"{self.MODEL}"
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a report response.

        The caller is responsible for constructing a
        safe prompt. This class performs only a final
        defensive size check.
        """

        if not prompt or not prompt.strip():

            raise ValueError(
                "ReportLLM received an empty prompt."
            )

        prompt = prompt.strip()

        if len(prompt) > self.MAX_PROMPT_CHARS:

            logger.warning(
                f"Report prompt too large "
                f"({len(prompt)} chars). "
                f"Keeping the first "
                f"{self.MAX_PROMPT_CHARS} characters."
            )

            prompt = prompt[
                :self.MAX_PROMPT_CHARS
            ]

        logger.info(
            f"ReportLLM prompt characters: "
            f"{len(prompt)}"
        )

        for attempt in range(
            1,
            self.MAX_RETRIES + 1,
        ):

            try:

                logger.info(
                    f"ReportLLM request "
                    f"{attempt}/{self.MAX_RETRIES}"
                )

                response = (
                    self.client.chat.completions.create(

                        model=self.MODEL,

                        messages=[
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],

                        temperature=0.2,

                        max_tokens=self.MAX_OUTPUT_TOKENS,
                    )
                )

                if not response.choices:

                    raise RuntimeError(
                        "Groq returned no choices."
                    )

                answer = (
                    response
                    .choices[0]
                    .message
                    .content
                )

                if not answer:

                    raise RuntimeError(
                        "Groq returned an empty response."
                    )

                answer = answer.strip()

                logger.info(
                    "ReportLLM response generated successfully."
                )

                return answer

            except Exception as e:

                logger.error(
                    f"ReportLLM request failed "
                    f"(attempt {attempt}): {e}"
                )

                if attempt >= self.MAX_RETRIES:

                    raise

                wait_seconds = 5 * attempt

                logger.info(
                    f"Waiting {wait_seconds} seconds "
                    f"before retry..."
                )

                time.sleep(
                    wait_seconds
                )

        raise RuntimeError(
            "ReportLLM failed unexpectedly."
        )