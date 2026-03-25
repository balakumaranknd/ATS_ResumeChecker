import re
# from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# def extract_keywords(text: str):
#     words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

#     keywords = [
#         word for word in words
#         if word not in ENGLISH_STOP_WORDS and len(word) > 2
#     ]

#     return list(set(keywords))

from sklearn.feature_extraction.text import CountVectorizer

def extract_keywords(text: str):
    vectorizer = CountVectorizer(
        stop_words='english',
        ngram_range=(1, 2),  # 👈 KEY CHANGE
        max_features=50
    )

    vectorizer.fit([text])
    return vectorizer.get_feature_names_out().tolist()