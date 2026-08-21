from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.retrieval.retriever import Retriever


def main():

    retriever = Retriever()

    query = "What is self attention?"

    from typing import Any, cast

    results = cast(
    dict[str, Any],
    retriever.search(
        query=query,
        top_k=5,
    ),
)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print("=" * 80)
    print("QUERY")
    print("=" * 80)
    print(query)

    print()

    print("=" * 80)
    print("TOP SEARCH RESULTS")
    print("=" * 80)

    for index in range(len(documents)):

        print(f"\nResult {index + 1}")

        print("-" * 60)

        print(
            f"Distance : {distances[index]:.4f}"
        )

        print(
            f"Metadata : {metadatas[index]}"
        )

        print()

        print(documents[index][:500])

        print()


if __name__ == "__main__":
    main()