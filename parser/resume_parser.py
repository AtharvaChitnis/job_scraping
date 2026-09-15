from pathlib import Path

from extractors.contact_extractors import extract_email, extract_phone
from extractors.location_extractor import extract_locations
from extractors.name_extractor import extract_name
from extractors.organization_extractor import extract_organizations
from models.candidate import CandidateProfile
from nlp.skill_matcher import SkillMatcher
from nlp.spacy_parser import SpacyParser
from parser.pdf_parser import extract_pdf_text
from parser.text_cleaner import clean_text


class ResumeParser:
    def __init__(self):
        self.spacy_parser = SpacyParser()
        self.skill_matcher = SkillMatcher(self.spacy_parser.nlp)

    def parse(self, pdf_path: str) -> CandidateProfile:
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"File not found: {pdf_path}")

        if pdf_path.suffix.lower() != ".pdf":
            raise ValueError("The input file must be a PDF.")

        text = clean_text(extract_pdf_text(pdf_path))
        entities = self.spacy_parser.parse(text)

        return CandidateProfile(
            name=extract_name(text, entities["persons"]),
            email=extract_email(text),
            phone=extract_phone(text),
            organizations=extract_organizations(text, entities["organizations"]),
            locations=extract_locations(text, entities["locations"]),
            skills=self.skill_matcher.extract(text),
        )
