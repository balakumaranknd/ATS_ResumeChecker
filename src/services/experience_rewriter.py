from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import re

load_dotenv()

def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_json(text):
    try:
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    return []


def rewrite_experience(bullets, skills_to_add):

    client = get_client()

    prompt = f"""
    You are a resume optimizer.

    You will be given resume bullet points.

    Task:
    - Improve EACH bullet point
    - Keep original meaning
    - Only slightly enhance wording
    - Inject relevant skills if applicable

    STRICT RULES:
    - Do NOT create new bullets
    - Do NOT summarize
    - Do NOT merge bullets
    - Keep same number of bullets
    - Keep structure similar

    Return ONLY a JSON list.

    Bullets:
    {bullets}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=500
    )

    content = response.choices[0].message.content

    return extract_json(content)