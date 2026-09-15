import re


def extract_email(text: str):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    match = re.search(pattern, text)

    return match.group(0) if match else None


def extract_phone(text: str):
    pattern = r"(?<!\d)(?:\+?\d[\d\s().-]{8,}\d)(?!\d)"

    match = re.search(pattern, text)

    return match.group(0).strip() if match else None