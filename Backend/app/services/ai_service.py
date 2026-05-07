import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "tinyllama"   # change to llama3 later

def extract_json(text):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return None


def clean_skills(skills):
    cleaned = []
    for skill in skills:
        if "@" in skill:
            continue
        if len(skill) > 25:
            continue
        cleaned.append(skill)
    return cleaned


def calculate_ats(matched, missing):
    if len(matched) + len(missing) == 0:
        return 0
    return int((len(matched) / (len(matched) + len(missing))) * 100)


def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an ATS resume analyzer.

STRICT RULES:
- Extract ONLY technical skills
- Ignore email, phone, names
- Use only English
- Suggestions must be simple strings

Resume:
{resume_text}

Job Description:
{job_description}

Return ONLY JSON:
{{
 "matched_skills": [],
 "missing_skills": [],
 "ats_score": 0,
 "suggestions": [],
 "improved_points": []
}}
"""

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })

    raw_output = response.json().get("response", "")

    data = extract_json(raw_output)

    if not data:
        return {
            "error": "Invalid AI response",
            "matched_skills": [],
            "missing_skills": [],
            "ats_score": 0,
            "suggestions": [],
            "improved_points": []
        }

    # Clean data
    data["matched_skills"] = clean_skills(data.get("matched_skills", []))
    data["missing_skills"] = clean_skills(data.get("missing_skills", []))

    # Fix ATS score
    data["ats_score"] = calculate_ats(
        data["matched_skills"],
        data["missing_skills"]
    )

    return data