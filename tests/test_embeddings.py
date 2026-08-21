from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import RAW_PDF_DIR

from app.ingestion.loaders.pdf_loader import PDFLoader

from app.preprocessing.chunker import Chunker

from app.embeddings.embedding_generator import (
    EmbeddingGenerator,
)


def main():

    loader = PDFLoader(RAW_PDF_DIR)

    document = loader.process_directory()[0]

    chunker = Chunker()

    chunks = chunker.chunk_document(document)

    generator = EmbeddingGenerator()

    embedded_chunks = generator.generate(chunks)

    print("=" * 70)
    print("TOTAL EMBEDDED CHUNKS")
    print("=" * 70)

    print(len(embedded_chunks))

    print()

    first = embedded_chunks[0]

    print("=" * 70)
    print("FIRST CHUNK")
    print("=" * 70)

    print(first.chunk.chunk_id)

    print()

    print(first.chunk.text[:300])

    print()

    print("=" * 70)
    print("Embedding Length")
    print("=" * 70)

    print(len(first.embedding))

    print()

    print("=" * 70)
    print("First 10 Values")
    print("=" * 70)

    print(first.embedding[:10])


if __name__ == "__main__":
    main()