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
from PIL import Image

st.set_page_config(page_title="SkillScope by A28 AI Lab", layout="centered")

# Load logo image
logo = Image.open("A28_logo.jpeg")
st.image(logo, width=150)



# Load spaCy and skills.csv
nlp = spacy.load("en_core_web_sm")
skills_df = pd.read_csv("skills.csv")
skill_list = skills_df['Skill'].dropna().str.lower().str.strip().tolist()
skill_set = list(set(skill_list))

st.title("🤖 A28 AI Lab – SkillScope (ATS-Lite): Resume Analyzer + JD Matcher")
st.markdown("""
### 👇 How to Use SkillScope

1. **Upload your Resume (PDF only)**
2. **Paste the Job Description** you're targeting
3. Click the **"Analyze & Match"** button
4. View the **extracted details** and your **matching percentage**
5. Click **Download JSON** if you want to save your results.

*Note: Currently optimized for English-Tech resumes only.*
""")

# File uploader
resume_file = st.file_uploader("Upload One or More Resumes (PDF)", type=["pdf"], accept_multiple_files= True)

# Job Description Input
jd_text = st.text_area("Paste Job Description")

analyze_clicked =  st.button("🔍 Analyze & Match")
if analyze_clicked:
    if not resume_file:
        st.warning("⚠️ Please upload at least one resume PDF.")
    elif not jd_text:
        st.warning("⚠️ Please paste a Job Description before analyzing.")
    else:
# Now both inputs are valid → proceed

        ranked_results = []
        for idx, resume in enumerate(resume_file):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(resume.read())
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
            st.download_button(f"📥 Download JSON For {resume.name}", data=json_data, file_name=f"{resume.name}_resume_data.json",
                               mime="application/json", key=f"download_json_{idx}") #Unique key per resume


            ranked_results.append({"File": resume.name, "Name": name, "Match %": comparison_result["match_percent"]
                })

            # Show table of ranking once outside the loop
        if ranked_results:
            df = pd.DataFrame(ranked_results).sort_values(by="Match %", ascending=False)
            st.subheader("📈 Ranked Resumes")
            st.dataframe(df)



with st.expander("📄 Terms of Use & Privacy Notice"):
    st.markdown("""
            **SkillScope** is a free resume analysis tool developed by **A28 AI Lab** for educational purposes.

            - We do not collect or store any uploaded resumes or job descriptions.
            - All processing happens in-memory during your session and is not logged.
            - Users are responsible for the accuracy and sensitivity of the data they upload.
            - This tool should not be used for any legally binding evaluations or decisions.
            *Disclaimer*  
             This is a resume analysis tool and does not guarantee job placement or outcomes.  
             Results should be interpreted with human judgment.

            **By using this tool, you agree to these terms.**
                """)