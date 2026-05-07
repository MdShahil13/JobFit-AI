from fastapi import APIRouter, UploadFile, File, Form

from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import analyze_resume

from app.services.ats_score import (
    calculate_ats_score,
    get_missing_keywords,
    generate_suggestions
)

router = APIRouter()

@router.post("/tailor-resume")
async def tailor_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # Extract Resume Text
    resume_text = extract_text_from_pdf(file)

    # ATS Score
    ats_score = calculate_ats_score(
        resume_text,
        job_description
    )

    # Missing Keywords
    missing_keywords = get_missing_keywords(
        resume_text,
        job_description
    )

    # Suggestions
    suggestions = generate_suggestions(
        ats_score
    )

    # AI Analysis
    ai_result = analyze_resume(
        resume_text,
        job_description
    )

    # Final Response
    return {
        "ats_score": ats_score,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions,
        "ai_analysis": ai_result,
        "resume_text": resume_text[:1500]
    }