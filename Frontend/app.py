import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/tailor-resume"

st.set_page_config(page_title="AI Resume Tailor", layout="centered")

st.title("📄 AI Resume Tailoring App")
st.write("Upload your resume and paste job description")

# ---- Upload Resume ----
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# ---- Job Description ----
job_desc = st.text_area("Paste Job Description Here", height=200)

# ---- Button ----
if st.button("🚀 Tailor Resume"):
    if uploaded_file is not None and job_desc:

        with st.spinner("Processing..."):

            files = {
                "file": (uploaded_file.name, uploaded_file, "application/pdf")
            }
            data = {
                "job_description": job_desc
            }

            try:
                response = requests.post(API_URL, files=files, data=data)

                if response.status_code == 200:
                    result = response.json()   # ✅ direct response (no ai_output)

                    st.success("✅ Resume Tailored Successfully!")

                    # ---- Display Results ----
                    st.subheader("✨ Tailored Resume")

                    # Matched Skills
                    st.markdown("### ✅ Matched Skills")
                    st.write(", ".join(result.get("matched_skills", [])))

                    # Missing Skills
                    st.markdown("### ❌ Missing Skills")
                    st.write(", ".join(result.get("missing_skills", [])))

                    # ATS Score
                    st.markdown("### 📊 ATS Score")
                    st.progress(result.get("ats_score", 0) / 100)
                    st.write(f"{result.get('ats_score', 0)}%")

                    # Suggestions
                    st.markdown("### 💡 Suggestions")
                    for s in result.get("suggestions", []):
                        st.write(f"- {s}")

                    # Improved Points
                    st.markdown("### ✨ Improved Resume Points")
                    for p in result.get("improved_points", []):
                        st.write(f"- {p}")

                else:
                    st.error(f"❌ Error: {response.text}")

            except Exception as e:
                st.error(f"⚠️ Backend not running or error: {e}")

    else:
        st.warning("⚠️ Please upload resume and enter job description")