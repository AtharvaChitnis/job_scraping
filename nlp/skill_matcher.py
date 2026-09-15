import re

from spacy.matcher import PhraseMatcher

from nlp.skills import SKILL_LOOKUP, SKILLS

SKILLS_SECTION_PATTERN = re.compile(
    r"TECHNICAL SKILLS\s*(.*?)(?:PROFESSIONAL EXPERIENCE|WORK EXPERIENCE|EXPERIENCE|PROJECTS|EDUCATION|$)",
    re.IGNORECASE | re.DOTALL,
)


class SkillMatcher:
    def __init__(self, nlp):
        self.nlp = nlp
        self.skill_lookup = SKILL_LOOKUP
        self.matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

        sorted_skills = sorted(SKILLS, key=len, reverse=True)
        patterns = [nlp.make_doc(skill) for skill in sorted_skills]
        self.matcher.add("SKILL", patterns)

    def extract(self, text: str) -> list[str]:
        search_texts = []
        section_match = SKILLS_SECTION_PATTERN.search(text)
        if section_match:
            search_texts.append(section_match.group(1))
        search_texts.append(text)

        found: list[str] = []
        seen: set[str] = set()

        for search_text in search_texts:
            doc = self.nlp(search_text)
            for _, start, end in self.matcher(doc):
                matched = doc[start:end].text.lower().strip()
                canonical = self.skill_lookup.get(matched)
                if canonical and canonical.lower() not in seen:
                    seen.add(canonical.lower())
                    found.append(canonical)

        return found
