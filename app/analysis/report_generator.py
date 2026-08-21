"""
report_generator.py

Generates educational research reports from research papers.

IMPORTANT:
- Only affects the research-report pipeline.
- Does NOT modify Chat.
- Does NOT modify Insights.
- Uses the dedicated ReportLLM.
- Keeps the actual research information inside
  the final prompt.
"""

import time

from app.analysis.report_llm import ReportLLM
from app.core.logger import logger


class ReportGenerator:
    """
    Safe multi-stage research report generator.

    Pipeline:

        Paper
          ↓
        Local chunks
          ↓
        Chunk analysis
          ↓
        Local combination
          ↓
        Final report
    """

    # ==========================================================
    # LIMITS
    # ==========================================================

    CHUNK_SIZE = 6000

    MAX_CHUNK_RESULT_CHARS = 2200

    MAX_FINAL_CONTEXT_CHARS = 4800

    MAX_FINAL_PROMPT_CHARS = 7400

    REQUEST_DELAY_SECONDS = 4

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self) -> None:

        self.llm = ReportLLM()

        logger.info(
            "ReportGenerator initialized."
        )

    # ==========================================================
    # DEFAULT FAILURE REPORT
    # ==========================================================

    def _failure_report(
        self,
        message: str,
    ) -> str:

        return (
            "# Report Generation Failed\n\n"
            f"{message}"
        )

    # ==========================================================
    # SPLIT PAPER
    # ==========================================================

    def _split_into_chunks(
        self,
        paper_text: str,
    ) -> list[str]:

        if not paper_text:
            return []

        chunks = []

        start = 0

        while start < len(paper_text):

            end = start + self.CHUNK_SIZE

            chunk = paper_text[
                start:end
            ].strip()

            if chunk:

                chunks.append(
                    chunk
                )

            start = end

        logger.info(
            f"Paper split into "
            f"{len(chunks)} local report chunk(s)."
        )

        return chunks

    # ==========================================================
    # ANALYZE CHUNK
    # ==========================================================

    def _analyze_chunk(
        self,
        chunk: str,
        chunk_number: int,
        total_chunks: int,
    ) -> str:

        logger.info(
            f"Analyzing report chunk "
            f"{chunk_number}/{total_chunks}..."
        )

        prompt = f"""
You are an expert research paper analyst.

Analyze section {chunk_number} of {total_chunks}
of a research paper.

Extract ONLY information explicitly present
in this section.

Do NOT invent facts.

Return a dense research summary.

Preserve:

- title
- authors
- research problem
- motivation
- objectives
- previous work
- proposed method
- architecture
- algorithms
- equations
- datasets
- preprocessing
- experiments
- hyperparameters
- evaluation metrics
- numerical results
- comparisons
- tables
- figures
- limitations
- conclusions
- future work

If something is not present, simply omit it.

Do not write generic explanations.

SECTION {chunk_number}/{total_chunks}

================ PAPER SECTION ================

{chunk}

================ END SECTION ================
"""

        logger.info(
            f"Report analysis prompt characters: "
            f"{len(prompt)}"
        )

        try:

            result = self.llm.generate(
                prompt
            )

            if not result:

                logger.warning(
                    f"Empty analysis result for "
                    f"chunk {chunk_number}."
                )

                return ""

            result = result.strip()

            if len(result) > self.MAX_CHUNK_RESULT_CHARS:

                logger.warning(
                    f"Analysis result for chunk "
                    f"{chunk_number} exceeded "
                    f"{self.MAX_CHUNK_RESULT_CHARS} "
                    f"characters."
                )

                result = result[
                    :self.MAX_CHUNK_RESULT_CHARS
                ]

            logger.info(
                f"Finished report analysis chunk "
                f"{chunk_number}/{total_chunks}."
            )

            return result

        except Exception as e:

            logger.exception(
                f"Failed to analyze report chunk "
                f"{chunk_number}/{total_chunks}: {e}"
            )

            return ""

    # ==========================================================
    # BUILD FINAL CONTEXT LOCALLY
    # ==========================================================

    def _build_final_context(
        self,
        summaries: list[str],
    ) -> str:
        """
        Combine chunk summaries locally.

        No LLM call is used here.

        The context is bounded so that the final report
        request stays within the Groq limit.
        """

        if not summaries:

            return ""

        context_parts = []

        remaining = self.MAX_FINAL_CONTEXT_CHARS

        for index, summary in enumerate(
            summaries,
            start=1,
        ):

            if remaining <= 0:
                break

            section = (
                f"\n\n### Extracted Section {index}\n"
                f"{summary}"
            )

            if len(section) <= remaining:

                context_parts.append(
                    section
                )

                remaining -= len(section)

            else:

                context_parts.append(
                    section[:remaining]
                )

                remaining = 0

        context = "".join(
            context_parts
        ).strip()

        logger.info(
            f"Final report context characters: "
            f"{len(context)}"
        )

        return context

    # ==========================================================
    # FINAL REPORT PROMPT
    # ==========================================================

    def _build_final_prompt(
        self,
        context: str,
    ) -> str:
        """
        Build a compact final prompt.

        IMPORTANT:

        The research context is placed FIRST and the
        instructions AFTER it.

        This means even if a defensive truncation
        occurs, the actual research information is
        not lost.
        """

        instructions = """
You are an expert AI research analyst and university professor.

Using ONLY the extracted research information below,
write a high-quality educational report.

Do NOT invent facts.

If information is unavailable, write:
"Not specified in the paper."

Focus on the actual evidence contained in the material.

Create this structure:

# AI Research Report

## 1. Paper at a Glance
- Title
- Research area
- Main problem
- Proposed solution
- Main result
- Main contribution

## 2. Executive Summary

Explain the paper's central idea, motivation,
approach and most important findings.

## 3. Research Problem and Motivation

Explain the problem, motivation, research gap
and objective.

## 4. Previous Work / Background

Explain only important previous approaches
actually mentioned in the paper.

## 5. Proposed Approach

Explain the proposed method, architecture,
components, algorithms and workflow.

## 6. How the Method Works

Explain important technical mechanisms,
equations and algorithms when present.

## 7. Dataset and Experimental Setup

Include dataset, preprocessing, splits,
models, hyperparameters, training setup,
hardware, software and evaluation metrics
when available.

## 8. Results — The Most Important Findings

Report actual numerical results and comparisons.
Use a Markdown table when useful.

## 9. Important Tables and Figures

Explain important tables and figures
when their information is available.

## 10. Ablation Studies and Additional Experiments

Include them when present.

## 11. Main Contributions

List the contributions explicitly supported
by the paper.

## 12. Strengths

Identify strengths supported by the paper.

## 13. Limitations

Report limitations stated by the authors.
Do not invent limitations.

## 14. Conclusion

Explain what the researchers demonstrated.

## 15. Future Work

Include future work explicitly mentioned
in the paper.

## 16. Key Technical Concepts

Explain the important technical concepts
needed to understand the paper.

## 17. Paper Workflow

Show the actual end-to-end workflow.

## 18. Beginner-Friendly Explanation

Explain the paper in simple language for
a first-year computer science student.

## 19. Final Takeaways

Give 5–10 concise takeaways.

IMPORTANT:

- Use only the supplied research material.
- Preserve actual numbers.
- Preserve model and dataset names.
- Do not fabricate missing information.
- Do not repeatedly say "the summary says".
- Do not write generic filler.
- Make the report information-dense.
- Return Markdown only.

================ RESEARCH MATERIAL ================

"""

        ending = """

================ END RESEARCH MATERIAL ================

Now generate the final AI Research Report.
"""

        # Calculate available space for research context.
        fixed_length = len(
            instructions
        ) + len(ending)

        available_context = (
            self.MAX_FINAL_PROMPT_CHARS
            - fixed_length
        )

        if available_context < 1000:

            available_context = 1000

        context = context[
            :available_context
        ]

        final_prompt = (
            instructions
            + context
            + ending
        )

        logger.info(
            f"Final report prompt characters: "
            f"{len(final_prompt)}"
        )

        return final_prompt

    # ==========================================================
    # GENERATE FINAL REPORT
    # ==========================================================

    def _generate_final_report(
        self,
        context: str,
    ) -> str:

        if not context:

            return self._failure_report(
                "No research information was available "
                "for report generation."
            )

        logger.info(
            "Generating final research report."
        )

        prompt = self._build_final_prompt(
            context
        )

        try:

            report = self.llm.generate(
                prompt
            )

            if not report:

                logger.warning(
                    "ReportLLM returned an empty "
                    "final report."
                )

                return self._failure_report(
                    "The language model returned "
                    "an empty report."
                )

            logger.info(
                "Final research report generated successfully."
            )

            return report.strip()

        except Exception as e:

            logger.exception(
                f"Final report generation failed: {e}"
            )

            return self._failure_report(
                "The document was uploaded successfully, "
                "but the final AI report could not be generated."
            )

    # ==========================================================
    # MAIN GENERATION
    # ==========================================================

    def generate(
        self,
        paper_text: str,
    ) -> str:

        logger.info(
            "Generating research report..."
        )

        if not paper_text or not paper_text.strip():

            logger.warning(
                "Empty paper text received."
            )

            return self._failure_report(
                "The research paper contains "
                "no readable text."
            )

        paper_text = paper_text.strip()

        logger.info(
            f"Report input characters: "
            f"{len(paper_text)}"
        )

        # ------------------------------------------------------
        # SPLIT
        # ------------------------------------------------------

        chunks = self._split_into_chunks(
            paper_text
        )

        if not chunks:

            return self._failure_report(
                "The research paper could not "
                "be divided into readable sections."
            )

        # ------------------------------------------------------
        # ANALYZE
        # ------------------------------------------------------

        summaries = []

        total_chunks = len(chunks)

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):

            summary = self._analyze_chunk(
                chunk=chunk,
                chunk_number=index,
                total_chunks=total_chunks,
            )

            if summary:

                summaries.append(
                    summary
                )

            if index < total_chunks:

                logger.info(
                    f"Waiting "
                    f"{self.REQUEST_DELAY_SECONDS} "
                    f"seconds before next report request..."
                )

                time.sleep(
                    self.REQUEST_DELAY_SECONDS
                )

        logger.info(
            f"Completed report analysis: "
            f"{len(summaries)}/{total_chunks} chunks."
        )

        if not summaries:

            return self._failure_report(
                "The paper could not be analyzed "
                "by the language model."
            )

        # ------------------------------------------------------
        # FINAL CONTEXT
        # ------------------------------------------------------

        final_context = self._build_final_context(
            summaries
        )

        if not final_context:

            return self._failure_report(
                "No usable research information "
                "was extracted from the paper."
            )

        # ------------------------------------------------------
        # FINAL REPORT
        # ------------------------------------------------------

        logger.info(
            "Waiting before final report generation..."
        )

        time.sleep(
            self.REQUEST_DELAY_SECONDS
        )

        report = self._generate_final_report(
            final_context
        )

        if not report:

            return self._failure_report(
                "The language model did not "
                "return a report."
            )

        logger.info(
            "Research report generation completed."
        )

        return report