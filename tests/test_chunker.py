from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import RAW_PDF_DIR
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.preprocessing.chunker import Chunker


def main():

    loader = PDFLoader(RAW_PDF_DIR)

    document = loader.process_directory()[0]

    chunker = Chunker()

    chunks = chunker.chunk_document(document)

    print("=" * 70)
    print("TOTAL CHUNKS")
    print("=" * 70)
    print(len(chunks))

    print()

    print("=" * 70)
    print("FIRST CHUNK")
    print("=" * 70)

    print("Chunk ID :", chunks[0].chunk_id)
    print("Page     :", chunks[0].page_number)
    print("Length   :", chunks[0].character_count)

    print()
    print(chunks[0].text)

    print()

    print("=" * 70)
    print("LAST CHUNK")
    print("=" * 70)

    print("Chunk ID :", chunks[-1].chunk_id)
    print("Page     :", chunks[-1].page_number)
    print("Length   :", chunks[-1].character_count)

    print()
    print(chunks[-1].text)


if __name__ == "__main__":
    main()