import re

def clean_text(text: str):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return text


def normalize_text(text):
    # Fix broken spacing
    text = re.sub(r'\s+', ' ', text)

    # Fix sentence breaks (basic)
    text = re.sub(r'\.\s+', '.\n', text)

    return text