import spacy


class SpacyParser:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def parse(self, text: str):
        doc = self.nlp(text)

        persons = []
        organizations = []
        locations = []

        for entity in doc.ents:

            if entity.label_ == "PERSON":
                persons.append(entity.text)

            elif entity.label_ == "ORG":
                organizations.append(entity.text)

            elif entity.label_ in {"GPE", "LOC", "FAC"}:
                locations.append(entity.text)

        return {
            "persons": list(dict.fromkeys(persons)),
            "organizations": list(dict.fromkeys(organizations)),
            "locations": list(dict.fromkeys(locations)),
        }