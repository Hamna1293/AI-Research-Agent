"""
research_extractor.py

Extracts structured research information from papers.

This extractor uses small sequential requests so that
large research papers do not exceed the Groq TPM limit.

Only this file handles chunking for research extraction.
"""

import json
import time

from app.core.logger import logger
from app.rag.llm import LLM


class ResearchExtractor:
    """
    Extracts important research paper information
    into structured JSON format.

    Large papers are processed in multiple small
    requests instead of sending the complete paper
    to Groq at once.
    """

    # ==========================================================
    # CHUNK SETTINGS
    # ==========================================================

    # Keep each paper section small enough for the
    # organization's 8000 TPM Groq limit.
    CHUNK_SIZE = 6000

    # Wait between requests so multiple requests do
    # not immediately consume the TPM window.
    REQUEST_DELAY = 4

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self) -> None:

        self.llm = LLM()

        logger.info(
            "ResearchExtractor initialized."
        )

    # ==========================================================
    # DEFAULT RESPONSE
    # ==========================================================

    def _default_response(self) -> dict:
        """
        Return empty analysis structure
        when extraction fails.
        """

        return {
            "title": "",
            "authors": [],
            "research_problem": "",
            "main_contribution": "",
            "methodology": [],
            "datasets": [],
            "models": [],
            "evaluation_metrics": [],
            "results": "",
            "limitations": [],
            "future_work": [],
        }

    # ==========================================================
    # SPLIT PAPER
    # ==========================================================

    def _split_into_chunks(
        self,
        paper_text: str,
    ) -> list[str]:
        """
        Split a large research paper into small
        sections suitable for Groq requests.
        """

        if not paper_text:

            return []

        chunks = []

        start = 0

        paper_length = len(
            paper_text
        )

        while start < paper_length:

            end = start + self.CHUNK_SIZE

            chunk = paper_text[
                start:end
            ]

            if chunk.strip():

                chunks.append(
                    chunk
                )

            start = end

        logger.info(
            f"Research paper split into "
            f"{len(chunks)} extraction chunk(s)."
        )

        return chunks

    # ==========================================================
    # CLEAN JSON
    # ==========================================================

    def _clean_json_response(
        self,
        response: str,
    ) -> str:
        """
        Remove markdown formatting from
        LLM JSON responses.
        """

        if not response:

            return ""

        response = response.strip()

        if response.startswith(
            "```json"
        ):

            response = response.replace(
                "```json",
                "",
                1,
            )

            response = response.replace(
                "```",
                "",
            )

        elif response.startswith(
            "```"
        ):

            response = response.replace(
                "```",
                "",
            )

        return response.strip()

    # ==========================================================
    # EXTRACT ONE CHUNK
    # ==========================================================

    def _extract_chunk(
        self,
        chunk: str,
        chunk_number: int,
        total_chunks: int,
    ) -> dict:
        """
        Extract structured information from
        one paper section.
        """

        logger.info(
            f"Analyzing research extraction chunk "
            f"{chunk_number}/{total_chunks}..."
        )

        prompt = f"""
You are an expert AI research analyst.

You are analyzing section {chunk_number}
of {total_chunks} of a research paper.

Extract ONLY information explicitly present
in THIS section.

Do not invent information.

Return ONLY valid JSON.
No markdown.
No explanations.

Use exactly this format:

{{
    "title": "",
    "authors": [],
    "research_problem": "",
    "main_contribution": "",
    "methodology": [],
    "datasets": [],
    "models": [],
    "evaluation_metrics": [],
    "results": "",
    "limitations": [],
    "future_work": []
}}

Important:

- If a field is not present in this section,
  return an empty value.
- Preserve technical terminology.
- Preserve important numerical results.
- Preserve dataset names.
- Preserve model names.
- Preserve evaluation metrics.
- Preserve methodology details.
- Preserve limitations and future work.
- Do not guess missing information.

Research paper section {chunk_number}/{total_chunks}:

==================================================

{chunk}

==================================================
"""

        logger.info(
            f"Research extraction prompt characters: "
            f"{len(prompt)}"
        )

        try:

            response = self.llm.generate(
                prompt
            )

            response = (
                self._clean_json_response(
                    response
                )
            )

            analysis = json.loads(
                response
            )

            if not isinstance(
                analysis,
                dict,
            ):

                logger.warning(
                    f"Chunk {chunk_number} returned "
                    f"non-dictionary JSON."
                )

                return self._default_response()

            logger.info(
                f"Research extraction chunk "
                f"{chunk_number}/{total_chunks} "
                f"completed successfully."
            )

            return analysis

        except json.JSONDecodeError:

            logger.warning(
                f"Chunk {chunk_number} returned "
                f"invalid JSON."
            )

            return self._default_response()

        except Exception as e:

            logger.exception(
                f"Research extraction chunk "
                f"{chunk_number}/{total_chunks} failed: {e}"
            )

            return self._default_response()

    # ==========================================================
    # MERGE CHUNK RESULTS
    # ==========================================================

    def _merge_results(
        self,
        results: list[dict],
    ) -> dict:
        """
        Merge structured information extracted
        from multiple paper sections.

        This merge happens locally and does NOT
        require another LLM request.
        """

        merged = self._default_response()

        for result in results:

            if not result:
                continue

            # --------------------------------------------------
            # SINGLE-VALUE FIELDS
            # --------------------------------------------------

            if not merged["title"]:

                title = result.get(
                    "title",
                    "",
                )

                if title:

                    merged["title"] = title

            # --------------------------------------------------

            if not merged["research_problem"]:

                problem = result.get(
                    "research_problem",
                    "",
                )

                if problem:

                    merged[
                        "research_problem"
                    ] = problem

            # --------------------------------------------------

            if not merged["main_contribution"]:

                contribution = result.get(
                    "main_contribution",
                    "",
                )

                if contribution:

                    merged[
                        "main_contribution"
                    ] = contribution

            # --------------------------------------------------

            result_text = result.get(
                "results",
                "",
            )

            if result_text:

                if merged["results"]:

                    merged["results"] += (
                        "\n\n"
                        + result_text
                    )

                else:

                    merged["results"] = result_text

            # --------------------------------------------------
            # LIST FIELDS
            # --------------------------------------------------

            list_fields = [
                "authors",
                "methodology",
                "datasets",
                "models",
                "evaluation_metrics",
                "limitations",
                "future_work",
            ]

            for field in list_fields:

                values = result.get(
                    field,
                    [],
                )

                if not isinstance(
                    values,
                    list,
                ):

                    continue

                for value in values:

                    if value not in merged[field]:

                        merged[field].append(
                            value
                        )

        return merged

    # ==========================================================
    # MAIN EXTRACTION
    # ==========================================================

    def extract(
        self,
        paper_text: str,
    ) -> dict:
        """
        Extract structured information from
        a research paper.

        Small papers:
            one LLM request

        Large papers:
            multiple small LLM requests

        No final LLM synthesis request is used.
        Results are merged locally.
        """

        logger.info(
            "Extracting research information..."
        )

        # ------------------------------------------------------
        # VALIDATE INPUT
        # ------------------------------------------------------

        if not paper_text or not paper_text.strip():

            logger.warning(
                "Empty paper text received."
            )

            return self._default_response()

        paper_text = paper_text.strip()

        logger.info(
            f"Analysis input size: "
            f"{len(paper_text)} characters"
        )

        # ------------------------------------------------------
        # SPLIT PAPER
        # ------------------------------------------------------

        chunks = self._split_into_chunks(
            paper_text
        )

        if not chunks:

            logger.warning(
                "No readable research chunks found."
            )

            return self._default_response()

        total_chunks = len(
            chunks
        )

        chunk_results = []

        # ------------------------------------------------------
        # PROCESS CHUNKS SEQUENTIALLY
        # ------------------------------------------------------

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):

            result = self._extract_chunk(
                chunk=chunk,
                chunk_number=index,
                total_chunks=total_chunks,
            )

            if result:

                chunk_results.append(
                    result
                )

            # --------------------------------------------------
            # RATE-LIMIT PROTECTION
            # --------------------------------------------------

            if index < total_chunks:

                logger.info(
                    f"Waiting {self.REQUEST_DELAY} "
                    f"seconds before next extraction request..."
                )

                time.sleep(
                    self.REQUEST_DELAY
                )

        # ------------------------------------------------------
        # MERGE
        # ------------------------------------------------------

        logger.info(
            f"Completed research extraction of "
            f"{len(chunk_results)}/{total_chunks} chunks."
        )

        if not chunk_results:

            logger.error(
                "No research extraction results were produced."
            )

            return self._default_response()

        analysis = self._merge_results(
            chunk_results
        )

        logger.info(
            "Research information extracted successfully."
        )

        return analysis