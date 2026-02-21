import streamlit as st
import pdfplumber
from docx import Document

# ------------------ Page Config ------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("AI Resume Analyzer")
st.write("Upload your resume (PDF or DOCX)")

# ------------------ Helper Functions ------------------
def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text

def read_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_skills(text):
    skills_db = [
        "python", "java", "c++", "html", "css", "javascript",
        "react", "sql", "machine learning", "data analysis",
        "power bi", "excel", "azure", "aws"
    ]

    found_skills = []
    text_lower = text.lower()

    for skill in skills_db:
        if skill in text_lower:
            found_skills.append(skill.capitalize())

    return list(set(found_skills))

def resume_score(skills):
    return min(len(skills) * 10, 100)

def recommended_role(skills):
    if "React" in skills or "Javascript" in skills:
        return "Frontend Developer"
    elif "Python" in skills and "Machine learning" in skills:
        return "AI / ML Engineer"
    elif "Sql" in skills or "Power bi" in skills:
        return "Data Analyst"
    else:
        return "Software Developer"

# ------------------ File Upload ------------------
uploaded_file = st.file_uploader(
    "Choose a resume",
    type=["pdf", "docx"]
)

if uploaded_file:
    # Read resume
    if uploaded_file.name.endswith(".pdf"):
        resume_text = read_pdf(uploaded_file)
    else:
        resume_text = read_docx(uploaded_file)

    # ------------------ Resume Text ------------------
    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content", resume_text, height=300)

    # ------------------ Skill Extraction ------------------
    skills = extract_skills(resume_text)

    st.subheader("Detected Skills")

    if skills:
        cols = st.columns(len(skills))
        for col, skill in zip(cols, skills):
            col.markdown(
                f"""
                <div style="
                    background-color:#e0f2fe;
                    padding:8px 12px;
                    border-radius:20px;
                    text-align:center;
                    font-weight:600;
                    color:#0369a1;
                    ">
                    {skill}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("No skills detected")

    # ------------------ Resume Score ------------------
    score = resume_score(skills)

    st.subheader("Resume Score")
    st.progress(score / 100)
    st.write(f"**{score} / 100**")
    st.caption("💡 Improve your score by adding more relevant technical skills")

    # ------------------ Suggestions ------------------
    st.subheader("Suggestions to Improve Resume")

    recommended_skills = ["Python", "SQL", "Azure", "Machine learning", "Power bi"]
    missing_skills = [s for s in recommended_skills if s not in skills]

    if missing_skills:
        for skill in missing_skills:
            st.write(f"• Add **{skill}** to strengthen your resume")
    else:
        st.success("Your resume already contains strong technical skills!")

    # ------------------ Job Role ------------------
    st.subheader("Recommended Job Role")
    role = recommended_role(skills)
    st.success(role)