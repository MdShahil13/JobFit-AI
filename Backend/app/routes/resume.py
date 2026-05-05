from fastapi import APIRouter, UploadFile, File, Form
from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import analyze_resume

router = APIRouter()

@router.post("/tailor-resume")
async def tailor_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Step 1: Extract text
    resume_text = extract_text_from_pdf(file)

    # Step 2: Call AI (IMPORTANT 🔥)
    ai_output = analyze_resume(resume_text, job_description)

    return {
        "ai_output": ai_output
    }