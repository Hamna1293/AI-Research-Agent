"""
insight_service.py

Generates Active Insights from an uploaded research paper.

The service reads indexed chunks belonging to the selected paper
and uses the existing RAG LLM to identify the most important
topics/concepts that a reader should understand.
"""

import json
from typing import Any

from app.core.logger import logger
from app.rag.llm import LLM
from app.vectorstore.chroma_manager import ChromaManager


class InsightService:
    """
    Generates learning insights from a selected research paper.
    """

    # Keep the prompt comfortably below Groq's
    # 8000 tokens-per-minute limit.
    MAX_CONTEXT_CHARS = 18000

    def __init__(self) -> None:

        self.vector_store = ChromaManager()

        self.llm = LLM()

        logger.info(
            "InsightService initialized."
        )

    def get_insights(
        self,
        filename: str,
        top_k: int = 8,
    ) -> list[dict[str, Any]]:
        """
        Analyze the selected paper and identify the most
        important concepts/topics a reader should learn.
        """

        logger.info(
            f"Generating active insights for: {filename}"
        )

        # ==================================================
        # 1. GET ALL CHUNKS FOR THE SELECTED PAPER
        # ==================================================

        try:

            paper_data = self.vector_store.collection.get(
                where={
                    "document": filename,
                }
            )

        except Exception:

            logger.exception(
                f"Failed to retrieve chunks for: {filename}"
            )

            return []

        documents = paper_data.get(
            "documents",
            [],
        )

        if not documents:

            logger.warning(
                f"No indexed chunks found for: {filename}"
            )

            return []

        logger.info(
            f"Found {len(documents)} indexed chunks "
            f"for {filename}."
        )

        # ==================================================
        # 2. REMOVE EMPTY CHUNKS
        # ==================================================

        valid_chunks = [
            chunk.strip()
            for chunk in documents
            if chunk and chunk.strip()
        ]

        if not valid_chunks:

            logger.warning(
                f"No usable text found for: {filename}"
            )

            return []

        # ==================================================
        # 3. SELECT REPRESENTATIVE CHUNKS
        # ==================================================
        #
        # Instead of sending every chunk to Groq,
        # sample chunks from across the entire paper.
        #
        # This allows the LLM to see:
        #
        # - Introduction
        # - Methodology
        # - Architecture / technical sections
        # - Experiments
        # - Results
        # - Conclusion
        #
        # without exceeding the token limit.
        # ==================================================

        max_chunks = 18

        if len(valid_chunks) <= max_chunks:

            selected_chunks = valid_chunks

        else:

            step = (
                len(valid_chunks) - 1
            ) / (max_chunks - 1)

            selected_indices = [
                round(index * step)
                for index in range(max_chunks)
            ]

            selected_chunks = [
                valid_chunks[index]
                for index in selected_indices
            ]

        logger.info(
            f"Selected {len(selected_chunks)} "
            f"representative chunks from "
            f"{len(valid_chunks)} total chunks."
        )

        # ==================================================
        # 4. BUILD COMPACT PAPER CONTEXT
        # ==================================================

        context_parts: list[str] = []

        current_chars = 0

        for index, chunk in enumerate(
            selected_chunks,
            start=1,
        ):

            remaining = (
                self.MAX_CONTEXT_CHARS
                - current_chars
            )

            if remaining <= 0:
                break

            # Prevent a single large chunk from
            # consuming the whole prompt.
            chunk_limit = min(
                1400,
                remaining,
            )

            chunk_text = chunk[:chunk_limit]

            context_parts.append(
                f"[Paper Section {index}]\n"
                f"{chunk_text}"
            )

            current_chars += len(chunk_text)

        paper_context = "\n\n".join(
            context_parts
        )

        if not paper_context.strip():

            logger.warning(
                f"Paper context is empty: {filename}"
            )

            return []

        logger.info(
            f"Final insight context size: "
            f"{len(paper_context)} characters."
        )

        # ==================================================
        # 5. BUILD LLM PROMPT
        # ==================================================

        prompt = f"""
You are the Active Insights component of an AI Research Assistant.

Analyze ONLY the research paper content provided below.

Your task is to help a student understand what they should learn
from this research paper.

DO NOT:

- search for other papers
- recommend unrelated topics
- invent information
- write a general summary
- explain the entire paper

Instead, identify the most important concepts, techniques,
architectures, algorithms, mechanisms, and background knowledge
that a reader should understand.

Select up to {top_k} important learning topics.

Prioritize:

1. Core concepts introduced by the paper.
2. Important technical mechanisms.
3. Models, architectures, algorithms, or frameworks.
4. Important mathematical or theoretical ideas.
5. Background concepts required to understand the paper.
6. Ideas that are repeatedly emphasized or central to the paper.

For each topic provide:

- topic
- importance
- description

The description should explain what the student should understand.

Allowed importance values:

"Core concept"
"Important"
"Background"

Return ONLY valid JSON.

Use exactly this format:

[
  {{
    "topic": "Topic name",
    "importance": "Core concept",
    "description": "What the student should understand about this topic."
  }}
]

RESEARCH PAPER:

{paper_context}
"""

        # ==================================================
        # 6. CALL LLM
        # ==================================================

        try:

            response = self.llm.generate(
                prompt
            )

        except Exception:

            logger.exception(
                "Failed to generate active insights."
            )

            return []

        if not response or not response.strip():

            logger.warning(
                "LLM returned an empty insight response."
            )

            return []

        # ==================================================
        # 7. CLEAN LLM RESPONSE
        # ==================================================

        cleaned_response = response.strip()

        if cleaned_response.startswith(
            "```json"
        ):

            cleaned_response = (
                cleaned_response[7:]
            )

        elif cleaned_response.startswith(
            "```"
        ):

            cleaned_response = (
                cleaned_response[3:]
            )

        if cleaned_response.endswith(
            "```"
        ):

            cleaned_response = (
                cleaned_response[:-3]
            )

        cleaned_response = (
            cleaned_response.strip()
        )

        # ==================================================
        # 8. PARSE JSON
        # ==================================================

        try:

            parsed = json.loads(
                cleaned_response
            )

        except json.JSONDecodeError:

            logger.error(
                "LLM returned invalid JSON "
                "for active insights."
            )

            logger.error(
                f"Raw response: {response}"
            )

            return []

        # ==================================================
        # 9. VALIDATE RESPONSE
        # ==================================================

        if not isinstance(
            parsed,
            list,
        ):

            logger.warning(
                "Insight response is not a list."
            )

            return []

        insights: list[
            dict[str, Any]
        ] = []

        allowed_importance = {
            "Core concept",
            "Important",
            "Background",
        }

        for item in parsed:

            if not isinstance(
                item,
                dict,
            ):
                continue

            topic = item.get(
                "topic"
            )

            importance = item.get(
                "importance"
            )

            description = item.get(
                "description"
            )

            if not topic or not description:
                continue

            if importance not in allowed_importance:

                importance = "Important"

            insights.append(
                {
                    "topic": str(
                        topic
                    ).strip(),

                    "importance": str(
                        importance
                    ).strip(),

                    "description": str(
                        description
                    ).strip(),
                }
            )

        # ==================================================
        # 10. REMOVE DUPLICATE TOPICS
        # ==================================================

        unique_insights = []

        seen_topics = set()

        for insight in insights:

            topic_key = (
                insight["topic"]
                .lower()
                .strip()
            )

            if topic_key in seen_topics:
                continue

            seen_topics.add(
                topic_key
            )

            unique_insights.append(
                insight
            )

        # ==================================================
        # 11. LIMIT RESULTS
        # ==================================================

        unique_insights = (
            unique_insights[:top_k]
        )

        logger.info(
            f"Generated "
            f"{len(unique_insights)} "
            f"active insight(s)."
        )

        return unique_insights