import streamlit as st
import pandas as pd
import spacy
from resume_parser import (
    extract_text_from_pdf, extract_name_smart, extract_name_nlp,
    extract_location, extract_designation, extract_email,
    extract_phone, extract_education, extract_skills_fuzzy,
    compare_resume_to_jd
)
import json
import tempfile

# Load spaCy and skills.csv
nlp = spacy.load("en_core_web_sm")
skills_df = pd.read_csv("skills.csv")
skill_list = skills_df['Skill'].dropna().str.lower().tolist()
skill_set = list(set(skill_list))

st.title("🤖 A28 AI Lab – SkillScope: Resume Analyzer + JD Matcher")

# File uploader
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job Description Input
jd_text = st.text_area("Paste Job Description")

if resume_file and jd_text:
    if st.button("🔍 Analyze & Match"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(resume_file.read())
            resume_path = tmp.name

        extracted_text = extract_text_from_pdf(resume_path)

        name = extract_name_smart(resume_path)
        if name == "Not Found":
            name = extract_name_nlp(extracted_text)

        skills = extract_skills_fuzzy(extracted_text, skill_set)

        comparison_result = compare_resume_to_jd(skills, jd_text, skill_set)

        st.subheader("📌 Resume Details")
        st.write(f"**Name:** {name}")
        st.write(f"**Location:** {extract_location(extracted_text)}")
        st.write(f"**Designation:** {extract_designation(extracted_text)}")
        st.write(f"**Email:** {extract_email(extracted_text)}")
        st.write(f"**Phone:** {extract_phone(extracted_text)}")
        st.write(f"**Education:** {extract_education(extracted_text)}")
        st.write(f"**Extracted Skills:** {', '.join(sorted(skills))}")

        st.subheader("📊 Resume vs JD Matching")
        st.write(f"**Match Percentage:** {comparison_result['match_percent']}%")
        st.write(f"✅ Matched Skills: {', '.join(comparison_result['matched_skills'])}")
        st.write(f"❌ Missing Skills: {', '.join(comparison_result['missing_skills'])}")

        resume_data = {
            "Name": name,
            "Location": extract_location(extracted_text),
            "Designation": extract_designation(extracted_text),
            "Email": extract_email(extracted_text),
            "Phone": extract_phone(extracted_text),
            "Education": extract_education(extracted_text),
            "Skills": sorted(skills)
        }

        json_data = json.dumps(resume_data, indent=4)
        st.download_button("📥 Download Extracted JSON", data=json_data, file_name="resume_data.json",
                           mime="application/json")