import re

from nlp.skills import SKILLS_LOWER

ACRONYM_BLOCKLIST = {
    "bpo",
    "dsa",
    "dbms",
    "cms",
    "qa",
    "seo",
    "ml",
    "csv",
    "pim",
    "smb",
    "csat",
    "ai",
    "nlp",
    "oop",
    "sdlc",
    "crm",
    "js",
    "sql",
    "git",
    "api",
    "it",
    "us",
    "uk",
    "created",
    "projects",
    "python/js",
    "focus technologies",
    "product information management",
}

JOB_ORG_PATTERN = re.compile(
    r"(?:Executive|Writer|Associate|Engineer|Developer|Manager|Analyst|Intern|Consultant|Specialist)"
    r"\s*[-–]\s*([^|\n(]+?)\s*(?:\||\(|$)",
    re.IGNORECASE | re.MULTILINE,
)

EDU_ORG_PATTERNS = [
    re.compile(r"University of [A-Za-z\s]+?(?=,|\||\n|$)", re.IGNORECASE),
    re.compile(
        r"[A-Z][A-Za-z\s&.'-]*College of [A-Za-z\s&.'-]+?(?=,|\||\n|$)",
        re.IGNORECASE,
    ),
]

KNOWN_ORG_PATTERNS = [
    r"Prime Focus Technologies?",
    r"Iksula(?:\s*\([^)]+\))?",
    r"Teleperformance",
    r"Business Promoted",
    r"Capita",
    r"University of Mumbai",
    r"Thakur College of Science and Commerce",
]


def extract_organizations(
    text: str,
    spacy_orgs: list[str] | None = None,
) -> list[str]:
    del spacy_orgs  # spaCy ORG labels are too noisy for resumes.

    organizations: list[str] = []

    for match in JOB_ORG_PATTERN.finditer(text):
        organizations.append(_normalize_org(match.group(1)))

    for pattern in EDU_ORG_PATTERNS:
        for match in pattern.finditer(text):
            organizations.append(_normalize_org(match.group(0)))

    for pattern in KNOWN_ORG_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            organizations.append(_normalize_org(match.group(0)))

    return _dedupe_valid_orgs(organizations)


def _normalize_org(name: str) -> str:
    name = re.sub(r"\s+", " ", name)
    name = name.strip(" -|,;\n")
    name = re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()
    return name


def _is_valid_org(name: str) -> bool:
    normalized = name.lower().strip()

    if len(normalized) < 3 or len(normalized) > 60:
        return False
    if normalized in ACRONYM_BLOCKLIST:
        return False
    if normalized in SKILLS_LOWER:
        return False
    if re.search(r"\n|\d|/|\\|@", name):
        return False
    if re.search(
        r"(expected|information technology|customer support|content writer|projects ml|with bsc|with msc)",
        normalized,
    ):
        return False

    words = normalized.split()
    if len(words) == 1 and len(words[0]) <= 4:
        return False

    return True


def _org_key(name: str) -> str:
    key = name.lower()
    key = re.sub(r"technologies\b", "technology", key)
    return key


def _dedupe_valid_orgs(organizations: list[str]) -> list[str]:
    org_by_key: dict[str, str] = {}

    for org in organizations:
        cleaned = _normalize_org(org)
        key = _org_key(cleaned)

        if not cleaned or not _is_valid_org(cleaned):
            continue

        existing = org_by_key.get(key)
        if not existing or len(cleaned) > len(existing):
            org_by_key[key] = cleaned

    return list(org_by_key.values())
