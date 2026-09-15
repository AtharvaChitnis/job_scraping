import re


def clean_text(text: str) -> str:
    # Convert Windows line endings
    text = text.replace("\r", "\n")

    # Remove unnecessary spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()