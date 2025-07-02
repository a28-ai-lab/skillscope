import pandas as pd
import spacy
from rapidfuzz import fuzz
import fitz
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    print("Trying to open:", pdf_path)
    with fitz.open(pdf_path) as doc:
        print("Opened pdf with:", len(doc), "pages")
        for page in doc:
            text += page.get_text()
    return text



    # ... rest of the code


def extract_location(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text
    return "Not Found"


# Example list of common job titles
job_titles = [
    'Software Engineer', 'Data Analyst', 'Business Analyst', 'Machine Learning Engineer',
    'Product Manager', 'DevOps Engineer', 'QA Engineer', 'Automation Tester', 'SDET',
    'Backend Developer', 'Frontend Developer', 'Project Manager'
]

def extract_designation(text, titles=job_titles):
    for title in titles:
        if title.lower() in text.lower():
            return title
    return "Not Found"


def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+',text)

    if match:
        return match.group(0)
    else:
        return "Not Found"


def extract_phone(text):
    match = re.search(r'\+?\d[\d\s\-]{8,15}',text)
    if match:
        phone = match.group(0).strip()
        #removes \n, spaces, etc.
        return re.sub(r'[^\d+]','',phone)
        #optinal: removes unwanted characters
    else:
        return "Not Found"


def extract_education(text):
    degrees = {
        'B.Tech': ['b.tech', 'b tech', 'bachelor of technology'],
        'M.Tech': ['m.tech', 'm tech', 'master of technology'],
        'MBA': ['mba', 'master of business administration'],
        'BCA': ['bca', 'bachelor of computer applications'],
        'MCA': ['mca', 'master of computer applications'],
        'BSC': ['bsc', 'b.sc', 'bachelor of science'],
        'BBA': ['bba', 'bachelor of business administration'],
        'BA': ['ba', 'bachelor of arts'],
        'MA': ['ma', 'master of arts'],
        'BCom': ['bcom', 'b.com', 'bachelor of commerce']
    }

    text_lower = text.lower()

    for degree, variations in degrees.items():
        for variant in variations:
            if variant in text_lower:
                return degree

    return "Not Found"


def extract_name_smart(pdf_path):
    tech_keywords = {
        "java", "python", "sql", "c++", "c#", "html", "css", "javascript",
        "data", "developer", "engineer", "visualization", "analysis", "insight"
    }

    doc = fitz.open(pdf_path)
    page = doc[0]
    blocks = page.get_text("dict")["blocks"]

    # Find max font size (usually name has the biggest)
    all_sizes = [span["size"] for block in blocks for line in block.get("lines", []) for span in line["spans"]]
    max_size = max(all_sizes) if all_sizes else 0

    for block in blocks:
        for line in block.get("lines", []):
            for span in line["spans"]:
                text = span["text"].strip()
                font_size = span["size"]

                if (
                    text and
                    len(text.split()) <= 4 and
                    font_size >= max_size - 1 and
                    text.lower() not in tech_keywords and
                    re.match(r'^[A-Z][A-Z\s]{2,}$', text)  # Full uppercase name
                ):
                    return text.title()  # Return in proper case

    return "Not Found"


def extract_name_nlp(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and 2 <= len(ent.text.split()) <= 3:
            return ent.text
    return "Not Found"


# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load skill list from CSV
skills_df = pd.read_csv("skills.csv")
skill_list = skills_df['Skill'].dropna().str.lower().tolist()

# Clean duplicates
skill_set = list(set(skill_list))




def extract_skills_fuzzy(resume_text, skill_list, threshold=92):
    doc = nlp(resume_text.lower())

    #create a blocklist of generic and non-skill words
    blocklist = {"computer vision","Hindi","stakeholder management","teamwork","hypothesis testing", "Teamwork","time management","feature engineering", "hindi", "English","marketing automation", "english","developer","data lake", "campaign management", "lead generation","", "engineer", "project", "experience", "knowledge", "team", "solution","solutions", "skills", "data studio"}


    # Collect meaningful phrases only
    tokens = {
        token.text.lower().strip()
        for token in doc
        if not token.is_stop and not token.is_punct and len(token.text.strip()) > 2
    }
    chunks = {
        chunk.text.lower().strip()
        for chunk in doc.noun_chunks
        if len(chunk.text.strip()) > 2
    }

    all_phrases = tokens.union(chunks)
    extracted_skills = set()

    for phrase in all_phrases:
        #skip phrases in blocklist
        if phrase in blocklist:
            continue
        for skill in skill_list:
            score = fuzz.token_set_ratio(phrase, skill.strip())
            if score >= threshold:
                extracted_skills.add(skill)

        extracted_skills = extracted_skills - blocklist

    return list(extracted_skills)


def extract_skills_strict(text, skill_list):
    found_skills = set()
    text_lower = text.lower()
    for skill in skill_list:
        # Optional: stricter match using word boundaries
        if re.search(rf'\b{re.escape(skill)}\b', text_lower):
            found_skills.add(skill)
    return found_skills


# Example usage
#resume_text = """Experienced in Python, machine learning, SQL, and dashboard tools like Tableau and PowerBI. Worked on Flask apps and pandas pipelines."""

def compare_resume_to_jd(resume_skills, jd_text, skill_list):
    jd_skills = extract_skills_strict(jd_text, skill_list)
    matched = sorted(set(resume_skills) & jd_skills)
    missing = sorted(jd_skills - set(resume_skills))
    match_percent = int((len(matched) / len(jd_skills)) * 100) if jd_skills else 0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percent": match_percent
    }

# Extract structured data

if __name__ == "__main__":
    pdf_file = "sample_resume.pdf"
    extracted_text = extract_text_from_pdf(pdf_file)

    name = extract_name_smart(pdf_file)
    if name == "Not Found":
            name = extract_name_nlp(extracted_text)
    print("Name:", name)
    print("Location: ", extract_location(extracted_text))
    print("Designation: ", extract_designation(extracted_text))
    print("Email: ", extract_email(extracted_text))
    print("Phone: ", extract_phone(extracted_text))
    print("Education: ", extract_education(extracted_text))

    # Extract skills
    skills = extract_skills_fuzzy(extracted_text, skill_set)
    print("Extracted Skills:", sorted(skills))

    jd_text = input("\nPaste Job Description:\n")

    comparison_result = compare_resume_to_jd(skills, jd_text, skill_set)

    print("\n--- Resume vs Job Description Match ---")
    print("Matched Skills:", comparison_result["matched_skills"])
    print("Missing Skills:", comparison_result["missing_skills"])
    print("Match Percentage:", comparison_result["match_percent"], "%")

    resume_data = {
        "Name":  name,
        "Location":  extract_location(extracted_text),
        "Designation":  extract_designation(extracted_text),
        "Email": extract_email(extracted_text),
        "Phone": extract_phone(extracted_text),
        "Education": extract_education(extracted_text),
        "Skills": sorted(skills)
    }

    import json
    print(json.dumps(resume_data, indent=4))


#import json
#with open("parsed_resume.json", "w") as f:
#    json.dump(resume_data, f, indent=4)




