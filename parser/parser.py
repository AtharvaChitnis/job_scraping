from pathlib import Path
from typing import Dict, List
import re

from extractors.contact_extractors import extract_email, extract_phone
from parser.pdf_parser import extract_pdf_text
from parser.text_cleaner import clean_text


class ResumePDFParser:
    """Extract and structure text from a PDF resume."""

    SECTION_NAMES = [
        "summary",
        "profile",
        "objective",
        "education",
        "experience",
        "work experience",
        "professional experience",
        "projects",
        "skills",
        "technical skills",
        "certifications",
        "certificates",
        "achievements",
        "awards",
        "internships",
        "languages",
        "interests",
    ]

    def __init__(self, pdf_path: str | Path):
        self.pdf_path = Path(pdf_path)

        if not self.pdf_path.exists():
            raise FileNotFoundError(f"Resume not found: {self.pdf_path}")

        if self.pdf_path.suffix.lower() != ".pdf":
            raise ValueError("The input file must be a PDF.")

    def extract_text(self) -> str:
        """Extract all text from the PDF."""
        try:
            return clean_text(extract_pdf_text(self.pdf_path))
        except Exception as exc:
            raise RuntimeError(f"Could not read PDF: {exc}") from exc

    @staticmethod
    def normalize_heading(line: str) -> str:
        """Normalize a potential section heading."""
        line = line.strip().lower()
        line = re.sub(r"[:\-]+$", "", line)
        line = re.sub(r"\s+", " ", line)
        return line

    def extract_sections(self, text: str) -> Dict[str, List[str]]:
        """Split the resume into sections based on common resume headings."""
        sections: Dict[str, List[str]] = {"general": []}
        current_section = "general"

        for line in text.splitlines():
            line = line.strip()

            if not line:
                continue

            normalized = self.normalize_heading(line)

            if normalized in self.SECTION_NAMES:
                current_section = normalized
                sections.setdefault(current_section, [])
            else:
                sections.setdefault(current_section, []).append(line)

        return sections

    @staticmethod
    def extract_name(text: str) -> str | None:
        """
        Basic name extraction.

        Assumes the candidate's name is usually near the beginning
        of the resume.
        """
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        for line in lines[:10]:
            if (
                len(line.split()) >= 2
                and len(line) <= 60
                and not re.search(r"[@|:/\\]", line)
                and not re.search(r"\d", line)
            ):
                normalized = line.lower()

                excluded = {
                    "resume",
                    "curriculum vitae",
                    "cv",
                    "profile",
                    "summary",
                    "objective",
                    "contact",
                }

                if normalized not in excluded:
                    return line

        return None

    def parse(self) -> Dict:
        """Parse the resume into a structured dictionary."""
        text = self.extract_text()
        sections = self.extract_sections(text)

        return {
            "name": self.extract_name(text),
            "email": extract_email(text),
            "phone": extract_phone(text),
            "sections": sections,
            "raw_text": text,
        }
