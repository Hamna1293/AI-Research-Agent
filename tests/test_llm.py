from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.rag.llm import LLM


def main():

    llm = LLM()

    response = llm.generate(
        "Explain self-attention in one paragraph."
    )

    print("=" * 80)
    print("LLM RESPONSE")
    print("=" * 80)
    print(response)


if __name__ == "__main__":
    main()