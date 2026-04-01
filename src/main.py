from fastapi import FastAPI, UploadFile, File, Form
from dotenv import load_dotenv
import os

from requests import post
from src.services.ats_service import process_resume
from src.parser.resume_parser import parse_resume
from src.utils.coherent_resume_parsing import build_structured_resume
from src.utils.llm_resume_parser import parse_resume_with_llm

import tempfile

load_dotenv()


app = FastAPI()

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    result = await process_resume(resume, job_description)
    return result



@app.post("/parsed_resume")
async def get_parsed_resume(resume: UploadFile = File(...)):
    suffix = os.path.splitext(resume.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await resume.read()
        tmp.write(contents)
        tmp_path = tmp.name

    raw_text = parse_resume(tmp_path)
    structured_data = build_structured_resume(raw_text)

    return structured_data

@app.post("/llm_parsed_resume")
async def get_llm_parsed_resume(resume: UploadFile = File(...)):
    suffix = os.path.splitext(resume.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await resume.read()
        tmp.write(contents)
        tmp_path = tmp.name

    structured_data = parse_resume_with_llm(tmp_path)
    return structured_data