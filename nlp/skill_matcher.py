from spacy.matcher import PhraseMatcher

from nlp.skills import SKILLS


class SkillMatcher:
    def __init__(self, nlp):
        self.nlp = nlp
        self.matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp.make_doc(skill) for skill in SKILLS]
        self.matcher.add("SKILL", patterns)

    def extract(self, text: str):
        doc = self.nlp(text)
        matches = self.matcher(doc)

        skills = []
        for _, start, end in matches:
            skills.append(doc[start:end].text)

        return list(dict.fromkeys(skills))
