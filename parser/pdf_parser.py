from pathlib import Path
from typing import Dict, List
import re

import pymupdf  # PyMuPDF


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

    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)

        if not self.pdf_path.exists():
            raise FileNotFoundError(
                f"Resume not found: {self.pdf_path}"
            )

        if self.pdf_path.suffix.lower() != ".pdf":
            raise ValueError("The input file must be a PDF.")

    def extract_text(self) -> str:
        """Extract all text from the PDF."""
        text_parts: List[str] = []

        try:
            with pymupdf.open(self.pdf_path) as document:
                if len(document) == 0:
                    raise ValueError("The PDF contains no pages.")

                for page in document:
                    page_text = page.get_text("text")

                    if page_text.strip():
                        text_parts.append(page_text)

        except Exception as exc:
            raise RuntimeError(
                f"Could not read PDF: {exc}"
            ) from exc

        text = "\n".join(text_parts)
        return self.clean_text(text)

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean extracted PDF text while preserving line structure."""
        text = text.replace("\r", "\n")

        # Normalize spaces/tabs
        text = re.sub(r"[ \t]+", " ", text)

        # Remove excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    @staticmethod
    def normalize_heading(line: str) -> str:
        """Normalize a potential section heading."""
        line = line.strip().lower()
        line = re.sub(r"[:\-]+$", "", line)
        line = re.sub(r"\s+", " ", line)
        return line

    def extract_sections(self, text: str) -> Dict[str, List[str]]:
        """
        Split the resume into sections based on common resume headings.
        """
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
    def extract_email(text: str) -> str | None:
        """Extract the first email address."""
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        match = re.search(pattern, text)

        return match.group(0) if match else None

    @staticmethod
    def extract_phone(text: str) -> str | None:
        """Extract a likely phone number."""
        pattern = r"(?<!\d)(?:\+?\d[\d\s().-]{8,}\d)(?!\d)"
        match = re.search(pattern, text)

        return match.group(0).strip() if match else None

    @staticmethod
    def extract_name(text: str) -> str | None:
        """
        Basic name extraction.

        Assumes the candidate's name is usually near the beginning
        of the resume.
        """
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        # Check the first few lines for a likely name.
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
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "sections": sections,
            "raw_text": text,
        }