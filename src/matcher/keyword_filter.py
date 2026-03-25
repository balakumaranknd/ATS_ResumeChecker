COMMON_TECH_SKILLS = [
    "python", "sql", "machine learning", "deep learning",
    "nlp", "data science", "pandas", "numpy",
    "tensorflow", "pytorch", "tableau", "power bi",
    "excel", "aws", "docker", "kubernetes"
]


def filter_keywords(keywords):
    clean_keywords = []

    for kw in keywords:
        kw = kw.strip()

        # Keep only meaningful keywords
        if len(kw.split()) <= 3:  # avoid long garbage phrases
            if not any(x in kw for x in ["looking", "experience", "role"]):
                clean_keywords.append(kw)

    # Remove duplicates + prioritize known skills
    final_keywords = []

    for kw in clean_keywords:
        if kw in COMMON_TECH_SKILLS:
            final_keywords.append(kw)

    # fallback: if nothing matched, return top cleaned ones
    return list(set(final_keywords or clean_keywords))