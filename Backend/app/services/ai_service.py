from openai import OpenAI

client = OpenAI(
    base_url="https://api.x.ai/v1",
    api_key=""
)

def analyze_resume(resume_text, job_description):
    prompt = f"""
You are an expert ATS resume optimizer.

Resume:
{resume_text}

Job Description:
{job_description}

Return JSON:
{{
 "matched_skills": [],
 "missing_skills": [],
 "ats_score": "",
 "suggestions": [],
 "improved_points": []
}}
"""

    response = client.chat.completions.create(
        model="grok-4",
        messages=[
            {"role": "system", "content": "You are an AI expert"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content