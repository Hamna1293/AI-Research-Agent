from pathlib import Path

from app.ingestion.document_loader_factory import DocumentLoaderFactory


DATA_DIR = Path("tests/test_files")


files = [
    "sample.txt",
    "sample.html",
    "sample.csv",
]


for file_name in files:

    print("\n====================")

    file_path = DATA_DIR / file_name

    print("Testing:", file_name)

    loader = DocumentLoaderFactory.get_loader(
        file_path
    )

    document = loader.load(
        file_path
    )

    print(
        "Filename:",
        document.filename
    )

    print(
        "Pages:",
        len(document.pages)
    )

    print(
        "Preview:"
    )

    print(
        document.pages[0].text[:200]
    )