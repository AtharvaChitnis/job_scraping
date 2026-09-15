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
            cleaned = " ".join(entity.text.split())

            if entity.label_ == "PERSON":
                persons.append(cleaned)
            elif entity.label_ == "ORG":
                organizations.append(cleaned)
            elif entity.label_ in {"GPE", "LOC", "FAC"}:
                locations.append(cleaned)

        return {
            "persons": _dedupe_preserve_order(persons),
            "organizations": _dedupe_preserve_order(organizations),
            "locations": _dedupe_preserve_order(locations),
        }


def _dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []

    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(item)

    return result
