from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import RAW_PDF_DIR
from app.ingestion.loaders.pdf_loader import PDFLoader


def main():

    loader = PDFLoader(RAW_PDF_DIR)

    documents = loader.process_directory()

    print("=" * 70)
    print(f"Documents Loaded : {len(documents)}")
    print("=" * 70)

    document = documents[0]

    print(f"Filename : {document.filename}")
    print(f"Title    : {document.metadata.title}")
    print(f"Author   : {document.metadata.author}")
    print(f"Pages    : {len(document.pages)}")

    print("\nFirst 500 characters:\n")

    print(document.pages[0].text[:500])


if __name__ == "__main__":
    main()