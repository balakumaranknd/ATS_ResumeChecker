import os
from src.parser.resume_parser import parse_resume
from src.parser.jd_parser import parse_job_description
from src.utils.text_cleaner import clean_text
from src.matcher.keyword_matcher import compute_similarity
from src.matcher.scorer import calculate_score, find_missing_keywords, remove_redundant_keywords
from src.matcher.keyword_extractor import extract_keywords
from src.matcher.keyword_filter import filter_keywords


UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def process_resume(uploaded_file, jd_text):

    # Save file
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
    with open(file_path, "wb") as f:
        f.write(await uploaded_file.read())

    # Parse
    resume_text = parse_resume(file_path)
    jd_text = parse_job_description(jd_text)

    # Clean
    resume_text = clean_text(resume_text)
    jd_text = clean_text(jd_text)

    # Similarity
    similarity = compute_similarity(resume_text, jd_text)
    score = calculate_score(similarity)

    # Extract
    jd_keywords = extract_keywords(jd_text)
    resume_keywords = extract_keywords(resume_text)

    # Filter
    jd_keywords = filter_keywords(jd_keywords)
    resume_keywords = filter_keywords(resume_keywords)

    # Missing
    missing_keywords = find_missing_keywords(jd_keywords, resume_keywords)

    # Remove redundancy
    missing_keywords = remove_redundant_keywords(missing_keywords)

    return {
    "match_score": score,
    "missing_keywords": missing_keywords[:15]  # limit for readability
    }