import streamlit as st
import pandas as pd
from jd_parser import read_job_description
from resume_extractor import extract_resume_text, extract_candidate_details
from match_score import calculate_match_score
from shortlist_agent import save_to_db
from email_generator import generate_email

st.set_page_config(page_title="Recruiter Screening Tool", layout="centered")
st.title("📄 RecruitAI – Multi-Agent Job Screening System")

# Step 1: Upload JD
st.header("1️⃣ Upload Job Description CSV")
jd_file = st.file_uploader("Upload job_description.csv", type=["csv"])
jd_data = None

if jd_file is not None:
    jd_data = read_job_description(jd_file)
    st.success("✅ Job Description Loaded!")
    st.write("**Job Title**:", jd_data['title'])
    st.write("**Skills Needed**:", jd_data['skills'])
    st.write("**Certifications**:", jd_data['certifications'])

# Step 2: Upload Resumes
st.header("2️⃣ Upload Resumes (Max 5 PDFs)")
uploaded_files = st.file_uploader("Upload PDF resumes", type=["pdf"], accept_multiple_files=True)

# Step 3: Matching Logic
if jd_data and uploaded_files:
    if len(uploaded_files) > 5:
        st.warning("⚠️ Upload only up to 5 resumes.")
    else:
        if st.button("🚀 Find Matches"):
            st.info("🧠 Processing resumes...")

            match_results = []

            for pdf in uploaded_files:
                try:
                    st.write(f"🔍 Reading {pdf.name}...")
                    resume_text = extract_resume_text(pdf)
                    candidate = extract_candidate_details(resume_text)

                    st.write("🧪 Candidate:", candidate)

                    score, skills, certs = calculate_match_score(jd_data, candidate)
                    is_shortlisted = score >= 60.0

                    save_to_db(candidate, score, is_shortlisted)

                    email = generate_email(candidate['name'], candidate['email'], jd_data['title']) if is_shortlisted else "Not shortlisted"

                    match_results.append({
                        "Name": candidate['name'].title(),
                        "Email": candidate['email'],
                        "Score": score,
                        "Shortlisted": "✅ Yes" if is_shortlisted else "❌ No",
                        "Email Invite": email if is_shortlisted else "—"
                    })

                except Exception as e:
                    st.error(f"❌ Error processing {pdf.name}: {e}")

            if match_results:
                st.success("✅ Matching complete!")
                df = pd.DataFrame(match_results).drop(columns=["Email Invite"])
                st.dataframe(df)

                for result in match_results:
                    if result["Shortlisted"] == "✅ Yes":
                        with st.expander(f"📨 Email for {result['Name']}"):
                            st.code(result["Email Invite"])
