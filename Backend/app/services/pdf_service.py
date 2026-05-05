import pdfplumber
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# 📥 Extract Resume Text
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text[:3000]


# 📤 Generate Tailored Resume PDF
def generate_resume_pdf(data, filename="tailored_resume.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    content = []

    # Title
    content.append(Paragraph("TAILORED RESUME", styles["Title"]))
    content.append(Spacer(1, 10))

    # Summary
    content.append(Paragraph("SUMMARY", styles["Heading2"]))
    content.append(Paragraph(data.get("summary", ""), styles["BodyText"]))
    content.append(Spacer(1, 10))

    # Skills
    content.append(Paragraph("SKILLS", styles["Heading2"]))
    for skill in data.get("matched_skills", []):
        content.append(Paragraph(f"• {skill}", styles["BodyText"]))

    content.append(Spacer(1, 10))

    # Experience
    content.append(Paragraph("EXPERIENCE", styles["Heading2"]))
    for point in data.get("improved_points", []):
        content.append(Paragraph(f"• {point}", styles["BodyText"]))

    content.append(Spacer(1, 10))

    # ATS
    content.append(Paragraph("ATS SCORE", styles["Heading2"]))
    content.append(Paragraph(str(data.get("ats_score", "")), styles["BodyText"]))

    doc.build(content)

    return filename