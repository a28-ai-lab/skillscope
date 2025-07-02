# 📄 SkillScope - Resume Analyzer & JD Matcher

SkillScope is an AI-powered resume parser and job description matcher. Built with Python and Streamlit, it extracts structured data from resumes and compares them against job descriptions to identify skill match, gaps, and fit percentage.

> 👨‍💻 Built and maintained by [A28 AI Lab](https://github.com/a28-ai-lab)

---

## 🔍 Features

- Upload and parse PDF resumes
- Extract:
  - Name
  - Location
  - Designation
  - Email
  - Phone
  - Education
  - Technical Skills
- Paste job descriptions and match with extracted skills
- Display:
  - Matched Skills ✅
  - Missing Skills ❌
  - Match Percentage 📊
- Download structured resume data as JSON

---

## 🚀 Live Demo

[Streamlit App](https://share.streamlit.io/your-streamlit-url-here)  
(Replace with actual deployed link once live)

---

## 🛠 Tech Stack

- Python
- spaCy (for NLP)
- pandas
- rapidfuzz (for fuzzy matching)
- PyMuPDF (resume PDF parsing)
- Streamlit (UI)

---
 
## 📂 Project Structure

skillscope 
│

├── app.py                  # Streamlit app main file

├── resume_parser.py        # Core logic for extracting and comparing resume data

├── requirements.txt        # List of Python dependencies

├── skills.csv              # Master list of skills used for matching

├── sample_resume9.pdf      # Sample resume file (for testing/demo)

├── parsed_resume.json      # Output JSON from parsed resume

├── README.md               # Project documentation

---

## 🔧 Installation

```bash
git clone https://github.com/a28-ai-lab/skillscope
cd skillscope
pip install -r requirements.txt
streamlit run app.py


---

👤 Author

Ashish S. — Founder, A28 AI Lab
Reach me on LinkedIn or GitHub


---

🧠 License

This project is proprietary and closed-source.
All rights reserved © 2025 [A28 AI Lab].
Unauthorized copying or distribution of the source code is strictly prohibited.


---

✨ Future Plans

Resume vs JD match report (PDF export)

Support for DOCX files

Skill suggestions based on gaps

User accounts and dashboards