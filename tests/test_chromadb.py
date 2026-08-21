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

from app.vectorstore.chroma_manager import (
    ChromaManager,
)


def main():

    loader = PDFLoader(RAW_PDF_DIR)

    document = loader.process_directory()[0]

    chunker = Chunker()

    chunks = chunker.chunk_document(document)

    generator = EmbeddingGenerator()

    embedded = generator.generate(chunks)

    chroma = ChromaManager()
    
    chroma.clear()
    chroma.add_documents(embedded)

    print("=" * 70)
    print("DOCUMENTS IN DATABASE")
    print("=" * 70)

    print(chroma.count())


if __name__ == "__main__":
    main()