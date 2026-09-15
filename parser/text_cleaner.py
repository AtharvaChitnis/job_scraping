import re
import unicodedata

ZERO_WIDTH_CHARS = re.compile(r"[\u200b-\u200d\ufeff]")
BULLET_CHARS = re.compile(r"[\u2022\u25cf\u2043\u2219\u00b7]")
CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = ZERO_WIDTH_CHARS.sub("", text)
    text = BULLET_CHARS.sub("", text)
    text = CONTROL_CHARS.sub("", text)
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
