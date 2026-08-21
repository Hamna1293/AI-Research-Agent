"""
Test PromptBuilder.
"""

from app.rag.prompt_builder import PromptBuilder


def main():

    builder = PromptBuilder()

    chunks = [
        {
            "text": "Self-attention allows every token to attend to every other token.",
            "document": "Attention_Research_Paper.pdf",
            "page": 2,
            "chunk_index": 14,
            "score": 0.61,
        },
        {
            "text": "Transformers replace recurrence using attention mechanisms.",
            "document": "Attention_Research_Paper.pdf",
            "page": 5,
            "chunk_index": 33,
            "score": 0.91,
        },
    ]

    prompt = builder.build(
        query="What is self attention?",
        retrieved_chunks=chunks,
    )

    print("=" * 80)
    print("PROMPT")
    print("=" * 80)
    print(prompt)


if __name__ == "__main__":
    main()