"""
topic_extractor.py

Identifies the most important topics a user should understand
from an uploaded research paper.
"""

import json

from app.core.logger import logger
from app.rag.llm import LLM


class TopicExtractor:
    """
    Extracts important learning topics from a research paper.
    """

    MAX_INPUT_CHARS = 30000

    def __init__(self) -> None:
        self.llm = LLM()

        logger.info(
            "TopicExtractor initialized."
        )

    def _default_response(self) -> dict:
        return {
            "topics": []
        }

    def _clean_json_response(
        self,
        response: str,
    ) -> str:
        response = response.strip()

        if response.startswith("```json"):
            response = response.replace(
                "```json",
                "",
                1,
            )

            response = response.replace(
                "```",
                "",
            )

        elif response.startswith("```"):
            response = response.replace(
                "```",
                "",
            )

        return response.strip()

    def extract(
        self,
        paper_text: str,
    ) -> dict:
        """
        Identify the most important topics a learner
        should understand from the paper.
        """

        logger.info(
            "Extracting important learning topics..."
        )

        if not paper_text or not paper_text.strip():
            logger.warning(
                "Empty paper text received."
            )

            return self._default_response()

        if len(paper_text) > self.MAX_INPUT_CHARS:

            logger.warning(
                f"Paper text too large "
                f"({len(paper_text)} chars). "
                f"Truncating to "
                f"{self.MAX_INPUT_CHARS} chars."
            )

            paper_text = paper_text[
                :self.MAX_INPUT_CHARS
            ]

        prompt = f"""
You are an expert research learning assistant.

Read the research paper below and identify the most
important topics that a student should understand
to properly understand this paper.

Do NOT summarize the entire paper.

Focus on concepts, methods, architectures,
techniques, theories, algorithms, datasets,
or other important subjects discussed in the paper.

Rank the topics by learning importance.

Use exactly these importance levels:

- "Must Know"
- "Important"
- "Good to Know"

Return ONLY valid JSON.
No markdown.
No explanations outside JSON.

Return exactly this structure:

{{
    "topics": [
        {{
            "topic": "",
            "importance": "Must Know",
            "description": ""
        }}
    ]
}}

Rules:

1. Generate 6 to 10 topics.
2. Only include topics supported by the paper.
3. Do not invent information.
4. "Must Know" should contain the core concepts required
   to understand the paper.
5. "Important" should contain concepts that significantly
   help understand the paper.
6. "Good to Know" should contain useful secondary concepts.
7. Keep each description to 1-2 sentences.
8. Avoid duplicate or overlapping topics.

Research Paper:

==================================================

{paper_text}

==================================================
"""

        logger.info(
            f"Topic extraction prompt characters: "
            f"{len(prompt)}"
        )

        try:

            response = self.llm.generate(
                prompt
            )

            response = self._clean_json_response(
                response
            )

            result = json.loads(
                response
            )

            if not isinstance(result, dict):
                raise ValueError(
                    "Topic extractor returned invalid structure."
                )

            topics = result.get(
                "topics",
                []
            )

            if not isinstance(topics, list):
                raise ValueError(
                    "Topics must be a list."
                )

            logger.info(
                f"Generated {len(topics)} learning topic(s)."
            )

            return {
                "topics": topics
            }

        except json.JSONDecodeError:

            logger.warning(
                "Groq returned invalid JSON for topic extraction."
            )

            return self._default_response()

        except Exception:

            logger.exception(
                "Topic extraction failed."
            )

            return self._default_response()