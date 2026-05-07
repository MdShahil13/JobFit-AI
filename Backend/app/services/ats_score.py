import re
from collections import Counter

# Common useless words
STOPWORDS = {
    "the", "and", "is", "in", "to", "of", "a", "for", "on",
    "with", "as", "by", "an", "be", "this", "that", "are",
    "will", "or", "from", "at", "your", "our", "you", "we",
    "their", "they", "have", "has", "had", "using"
}

# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return text.split()

# Extract keywords dynamically from JD
def extract_keywords(job_desc):
    words = clean_text(job_desc)

    keywords = [
        word for word in words
        if word not in STOPWORDS and len(word) > 2
    ]

    return Counter(keywords)

# ATS Score
def calculate_ats_score(resume, job_desc):
    resume_words = clean_text(resume)
    resume_text = " ".join(resume_words)

    jd_keywords = extract_keywords(job_desc)

    if not jd_keywords:
        return 0

    matched_weight = 0
    total_weight = 0

    for keyword, freq in jd_keywords.items():

        # important repeated words get more weight
        weight = min(freq, 5)

        total_weight += weight

        if keyword in resume_text:
            matched_weight += weight

    score = (matched_weight / total_weight) * 100

    return round(score, 2)

# Matched keywords (Skills found in both)
def get_matched_skills(resume, job_desc):
    resume_words = clean_text(resume)
    resume_text = " ".join(resume_words)

    jd_keywords = extract_keywords(job_desc)

    matched = []
    for keyword in jd_keywords:
        if keyword in resume_text:
            matched.append(keyword)

    return matched[:20]

# Missing keywords
def get_missing_keywords(resume, job_desc):
    resume_words = clean_text(resume)
    resume_text = " ".join(resume_words)

    jd_keywords = extract_keywords(job_desc)

    missing = []

    for keyword in jd_keywords:
        if keyword not in resume_text:
            missing.append(keyword)

    return missing[:20]

# Resume Suggestions
def generate_suggestions(score):
    suggestions = []

    if score < 40:
        suggestions.append("Add more relevant keywords from the job description.")
        suggestions.append("Improve project descriptions with technical terms.")
        suggestions.append("Include tools, technologies, and frameworks.")

    elif score < 70:
        suggestions.append("Resume matches partially. Add more domain-specific skills.")
        suggestions.append("Improve experience/project impact statements.")

    else:
        suggestions.append("Resume is well optimized for this job.")
        suggestions.append("Minor keyword improvements can increase score further.")

    return suggestions