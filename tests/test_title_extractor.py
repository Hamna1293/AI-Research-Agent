from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import RAW_PDF_DIR
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.preprocessing.metadata.title_extractor import TitleExtractor


def main():

    print("=" * 70)
    print("LOADING PDF")
    print("=" * 70)

    loader = PDFLoader(RAW_PDF_DIR)

    documents = loader.process_directory()

    document = documents[0]

    first_page = document.pages[0].text

    extractor = TitleExtractor()

    title = extractor.extract(first_page)

    print()
    print("=" * 70)
    print("EXTRACTED TITLE")
    print("=" * 70)

    print(title)

    print()
    print("=" * 70)
    print("FIRST 500 CHARACTERS")
    print("=" * 70)

    print(first_page[:500])


if __name__ == "__main__":
    main()