import re

from nlp.skills import SKILLS_LOWER

LOCATION_BLOCKLIST = SKILLS_LOWER | {
    "ai",
    "it",
    "api",
    "js",
    "us",
    "uk",
    "ml",
    "sql",
    "bpo",
    "crm",
    "cms",
    "qa",
    "seo",
    "oop",
    "nlp",
}

CITY_PATTERN = re.compile(
    r"\b(Mumbai|Delhi|Bangalore|Bengaluru|Hyderabad|Pune|Chennai|Kolkata|Remote)\b\s*\|",
    re.IGNORECASE,
)


def extract_locations(
    text: str,
    spacy_locations: list[str] | None = None,
) -> list[str]:
    locations: list[str] = []
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if len(lines) >= 2:
        contact_line = lines[1]
        city_match = re.match(r"^([A-Za-z][A-Za-z\s.-]{1,40}?)\s*\|", contact_line)
        if city_match:
            city = city_match.group(1).strip()
            if _is_valid_location(city):
                locations.append(city)

    for match in CITY_PATTERN.finditer(text):
        locations.append(match.group(1).title())

    if spacy_locations:
        for location in spacy_locations:
            cleaned = re.sub(r"\s+", " ", location).strip()
            if _is_valid_location(cleaned):
                locations.append(cleaned)

    return _dedupe_locations(locations)


def _is_valid_location(location: str) -> bool:
    normalized = location.lower().strip()

    if len(normalized) < 3 or len(normalized) > 40:
        return False
    if normalized in LOCATION_BLOCKLIST:
        return False
    if re.search(r"\d", location):
        return False
    if re.search(r"[@/\\]", location):
        return False

    return True


def _dedupe_locations(locations: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []

    for location in locations:
        cleaned = re.sub(r"\s+", " ", location).strip()
        key = cleaned.lower()

        if not cleaned or key in seen or not _is_valid_location(cleaned):
            continue

        seen.add(key)
        result.append(cleaned)

    return result
