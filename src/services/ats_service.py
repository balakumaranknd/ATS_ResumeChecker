import os
from src.parser.resume_parser import parse_resume
from src.parser.jd_parser import parse_job_description
from src.utils.text_cleaner import clean_text
from src.matcher.keyword_matcher import compute_similarity
from src.matcher.scorer import calculate_score, find_missing_keywords, remove_redundant_keywords
from src.matcher.keyword_extractor import extract_keywords
from src.matcher.keyword_filter import filter_keywords
from src.services.llm_analyzer import analyze_with_llm


UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def remove_contradictions(missing_keywords, strengths):
    strengths_text = " ".join(strengths).lower()

    return [
        kw for kw in missing_keywords
        if kw.lower() not in strengths_text
    ]


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

    

    llm_result = analyze_with_llm(resume_text, jd_text)

    llm_result = analyze_with_llm(resume_text, jd_text)

    missing_keywords = remove_contradictions(missing_keywords, llm_result.get("strengths", []))

    if "error" in llm_result:
        llm_result = {
        "match_score": 0,
        "missing_skills": {"must_have": [], "good_to_have": []},
        "strengths": [],
        "weaknesses": ["LLM failed to analyze"],
        "improvement_suggestions": []
        }

    final_score = round(
    0.4 * score + 0.6 * llm_result.get("match_score", 0), 2
    )

    # return {
    # "match_score": score,
    # "missing_keywords": missing_keywords[:15]  # limit for readability
    # }

    return {
    "final_score": final_score,
    "baseline_score": score,
    "llm_score": llm_result.get("match_score"),
    "missing_keywords": missing_keywords,
    "llm_analysis": llm_result
            }