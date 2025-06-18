import os
from dotenv import load_dotenv
import streamlit as st
from fpdf import FPDF
import tempfile
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")

st.set_page_config(page_title="SmartResume Generator", layout="centered")
st.title("🧠 SmartResume Generator")
st.write("Fill out the details below to generate a customized resume!")

# Input fields
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
summary = st.text_area("Professional Summary", height=100)
education = st.text_area("Education", height=100)
experience = st.text_area("Work Experience", height=150)
skills = st.text_area("Skills", height=100)
projects = st.text_area("Projects", height=100)

def create_prompt():
    return f"""
Generate a professional resume using the following user details:

Name: {name}
Email: {email}
Phone: {phone}

Summary:
{summary}

Education:
{education}

Work Experience:
{experience}

Skills:
{skills}

Projects:
{projects}

Format the resume cleanly with clear headings and bullet points where necessary.
"""

def create_pdf(resume_text, filename="resume.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in resume_text.split('\n'):
        pdf.multi_cell(0, 10, line)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

if st.button("Generate Resume"):
    with st.spinner("Generating your resume..."):
        prompt = create_prompt()
        try:
            response = model.generate_content(prompt)
            resume_text = response.text
            st.success("✅ Resume generated successfully!")
            st.text_area("📄 Your Generated Resume", value=resume_text, height=400)

            # PDF download section
            pdf_path = create_pdf(resume_text)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download Resume as PDF",
                    data=f,
                    file_name="resume.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"Error: {e}")
