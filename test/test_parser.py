import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from parser.pdf_parser import ResumePDFParser


def main():
    parser = ResumePDFParser(PROJECT_ROOT / "resume.pdf")

    result = parser.parse()

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()