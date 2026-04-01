import json
import os
import re
from dotenv import load_dotenv
import pdfplumber
from docx import Document
from openai import OpenAI

load_dotenv(dotenv_path=".env")

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment")
    
    return OpenAI(api_key=api_key)

client = get_client()


# -------------------------------
# TEXT EXTRACTION
# -------------------------------

def extract_text(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        raise ValueError("Unsupported file format")


# -------------------------------
# CLEAN TEXT
# -------------------------------

def clean_text(text: str) -> str:
    text = re.sub(r'(\w)\n(\w)', r'\1\2', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# -------------------------------
# PROMPT
# -------------------------------

def build_prompt(text: str) -> str:
    return f"""
You are an expert resume parser.

Extract structured information from the resume below.

Return ONLY valid JSON in this format:

{{
  "name": "",
  "phone": "",
  "email": "",
  "summary": "",
  "experience": [
    {{
      "company": "",
      "role": "",
      "duration": "",
      "achievements": []
    }}
  ],
  "skills": [],
  "education": []
}}

Rules:
- Do not hallucinate
- Extract exact information only
- If missing, return empty string
- Keep achievements as bullet points

Resume:
{text}
"""


# -------------------------------
# SAFE JSON LOAD
# -------------------------------

def safe_json_load(content: str):
    try:
        # Remove markdown ```json ``` wrappers
        content = re.sub(r"```json", "", content)
        content = re.sub(r"```", "", content)

        content = content.strip()

        return json.loads(content)

    except Exception as e:
        return {
            "error": "Invalid JSON from LLM",
            "exception": str(e),
            "cleaned_output": content
        }

# -------------------------------
# LLM CALL
# -------------------------------

def parse_with_llm(text: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": build_prompt(text)}],
        temperature=0
    )

    content = response.choices[0].message.content
    return safe_json_load(content)
    

# -------------------------------   
# MAIN PIPELINE FUNCTION
# -------------------------------

def parse_resume_with_llm(file_path: str) -> dict:
    raw_text = extract_text(file_path)

    if not raw_text or len(raw_text.strip()) < 50:
        return {"error": "Empty or invalid resume content"}

    cleaned_text = clean_text(raw_text)

    return parse_with_llm(cleaned_text)