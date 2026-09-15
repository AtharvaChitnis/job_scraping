from pathlib import Path
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from parser.resume_parser import ResumeParser


PROJECT_ROOT = Path(__file__).resolve().parent


def main():
    parser = ResumeParser()
    candidate = parser.parse(PROJECT_ROOT / "resume.pdf")

    print("\nNAME:")
    print(candidate.name)

    print("\nEMAIL:")
    print(candidate.email)

    print("\nPHONE:")
    print(candidate.phone)

    print("\nORGANIZATIONS:")
    for org in candidate.organizations:
        print("-", org)

    print("\nLOCATIONS:")
    for location in candidate.locations:
        print("-", location)

    print("\nSKILLS:")
    for skill in candidate.skills:
        print("-", skill)


if __name__ == "__main__":
    main()
