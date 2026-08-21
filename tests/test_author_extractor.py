from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import RAW_PDF_DIR
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.preprocessing.metadata.author_extractor import AuthorExtractor


def main():

    loader = PDFLoader(RAW_PDF_DIR)

    document = loader.process_directory()[0]

    first_page = document.pages[0].text

    extractor = AuthorExtractor()

    authors = extractor.extract(first_page)

    print("=" * 70)
    print("AUTHORS")
    print("=" * 70)

    for i, author in enumerate(authors, start=1):
        print(f"{i}. {author}")


if __name__ == "__main__":
    main()