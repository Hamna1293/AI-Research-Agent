from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.preprocessing.text_cleaner import TextCleaner


def main():

    cleaner = TextCleaner()

    sample_text = """
    
    
    This      is      a     sample     text.


    It contains      multiple spaces.


    It also has trailing spaces.       
    
    
    """

    cleaned = cleaner.clean_text(sample_text)

    print("=" * 60)
    print(cleaned)
    print("=" * 60)


if __name__ == "__main__":
    main()