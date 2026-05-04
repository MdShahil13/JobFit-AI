from fastapi import FastAPI, UploadFile, File, Form
import pdfplumber

app = FastAPI()

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

@app.post("/tailor-resume")
async def tailor_resume(file: UploadFile = File(...), job_description: str = Form(...)):
    resume_text = extract_text_from_pdf(file)

    return {
        "resume_text": resume_text[:500],
        "job_description": job_description
    }