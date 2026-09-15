import re


EXCLUDED_NAME_HEADINGS = {
    "resume",
    "curriculum vitae",
    "cv",
    "profile",
    "summary",
    "objective",
    "contact",
}


def extract_name(text: str, spacy_persons: list[str] | None = None) -> str | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines[:8]:
        if not _looks_like_name_line(line):
            continue

        normalized = line.lower()
        if normalized not in EXCLUDED_NAME_HEADINGS:
            return line

    if spacy_persons:
        for person in spacy_persons:
            cleaned = re.sub(r"\s+", " ", person).strip()
            if _looks_like_name_line(cleaned):
                return cleaned

    return None


def _looks_like_name_line(line: str) -> bool:
    if len(line.split()) < 2 or len(line) > 60:
        return False
    if re.search(r"[@|:/\\]", line):
        return False
    if re.search(r"\d", line):
        return False
    if line.isupper() and len(line.split()) > 4:
        return False
    return True
