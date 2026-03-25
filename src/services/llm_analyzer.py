from dotenv import load_dotenv
import os
import json
from openai import OpenAI
import re
import json

# 👇 FORCE PATH (VERY IMPORTANT)
load_dotenv(dotenv_path=".env")

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment")
    
    return OpenAI(api_key=api_key)


def extract_json(text):
    try:
        if not text or text.strip() == "":
            return {
                "error": "Empty response from LLM",
                "raw_output": text
            }

        # Extract JSON block
        match = re.search(r'\{.*\}', text, re.DOTALL)
        
        if match:
            json_str = match.group()
            return json.loads(json_str)
        else:
            return {
                "error": "No JSON found in response",
                "raw_output": text
            }

    except Exception as e:
        return {
            "error": str(e),
            "raw_output": text
        }


def analyze_with_llm(resume_text, jd_text, retries=2):

    client = get_client()

    prompt = f"""
You are an ATS system.

Analyze the resume against the job description.

Return ONLY valid JSON. Do NOT add any explanation.

Rules:
- match_score must be a number between 0 and 100
- missing_skills must be categorized into:
    - must_have (critical skills missing)
    - Only include TOP 5 most critical missing skills in must_have.
    - Prioritize skills explicitly mentioned in the job description.
    - Avoid generic or optional skills.
    - good_to_have (optional but beneficial)
    - Limit weaknesses to top 5 most impactful gaps.
    - Generate "improved_experience": Rewrite 2 bullet points from the resume to better match the job.

JSON format:

{{
  "match_score": 0,
  "missing_skills": {{
    "must_have": [],
    "good_to_have": []
  }},
  "strengths": [],
  "weaknesses": [],
  "improvement_suggestions": [],
  "improved_experience": []
}}

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    for attempt in range(retries):

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=800
            )

            content = response.choices[0].message.content

            result = extract_json(content)

            if "error" not in result:
                return result

        except Exception as e:
            print(f"Attempt {attempt+1} failed:", e)

    return {"error": "LLM failed after retries"}

    # return json.loads(content)