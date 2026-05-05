import streamlit as st
import requests

# ✅ Correct API URL (NO /api if not using prefix)
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

                # 🔍 DEBUG (IMPORTANT)
                st.write("🔍 Raw Response:", response.json())

                if response.status_code == 200:
                    result = response.json().get("ai_output")

                    st.success("✅ Resume Tailored Successfully!")

                    # ❌ If no result
                    if not result:
                        st.error("❌ No AI output received")
                    else:
                        st.subheader("✨ Tailored Resume")
                        st.markdown(result)   # ✅ Better formatting

                else:
                    st.error(f"❌ Error: {response.text}")

            except Exception as e:
                st.error(f"⚠️ Backend not running or error: {e}")

    else:
        st.warning("⚠️ Please upload resume and enter job description")