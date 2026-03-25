from fastapi import FastAPI, UploadFile, File, Form
from src.services.ats_service import process_resume

app = FastAPI()

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    result = await process_resume(resume, job_description)
    return result