"""
Test the complete RAG pipeline.
"""

from app.rag.rag_pipeline import RAGPipeline


def main():

    rag = RAGPipeline()

    question = "What is self attention?"

    answer = rag.answer(question)

    print("=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(question)

    print()

    print("=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(answer)


if __name__ == "__main__":
    main()