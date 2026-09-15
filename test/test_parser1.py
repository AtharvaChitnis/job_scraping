import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from parser.resume_parser import ResumeParser


def main():
    candidate = ResumeParser().parse(PROJECT_ROOT / "resume.pdf")

    print("\nNAME:")
    print(candidate.name)

    print("\nEMAIL:")
    print(candidate.email)

    print("\nPHONE:")
    print(candidate.phone)

    print("\nORGANIZATIONS:")
    for organization in candidate.organizations:
        print("-", organization)

    print("\nLOCATIONS:")
    for location in candidate.locations:
        print("-", location)

    print("\nSKILLS:")
    for skill in candidate.skills:
        print("-", skill)


if __name__ == "__main__":
    main()
