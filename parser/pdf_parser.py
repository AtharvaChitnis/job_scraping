from pathlib import Path

import pymupdf


def extract_pdf_text(pdf_path: str | Path) -> str:
    text_parts = []

    with pymupdf.open(pdf_path) as pdf:
        if len(pdf) == 0:
            raise ValueError("The PDF contains no pages.")

        for page in pdf:
            page_text = page.get_text("text")
            if page_text.strip():
                text_parts.append(page_text)

    return "\n".join(text_parts)
