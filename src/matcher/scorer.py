def calculate_score(similarity_score):
    return round(similarity_score * 100, 2)

def find_missing_keywords(jd_keywords, resume_keywords):
    return list(set(jd_keywords) - set(resume_keywords))

def remove_redundant_keywords(keywords):
    keywords = sorted(keywords, key=len, reverse=True)

    final = []
    for kw in keywords:
        if not any(kw in longer for longer in final):
            final.append(kw)

    return final