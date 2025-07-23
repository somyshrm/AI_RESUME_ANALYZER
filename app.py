import streamlit as st
import PyPDF2
import requests


from dotenv import load_dotenv
import os

load_dotenv()  # Loads the .env file

# Access the variables
api_key = os.getenv("API_KEY")
API_KEY_2 = os.getenv("API_KEY_2")
MODEL_ID = os.getenv("MODEL_ID")
debug = os.getenv("DEBUG") == "True"

# Hugging Face API Setup
HF_API_TOKEN = {API_KEY_2} # 🔁 Replace with your token
MODEL_ID = {MODEL_ID}

API_URL =  f"{api_key}"
HEADERS = {"Authorization": f"Bearer {API_KEY_2}"}


def query_llm(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 512, "temperature": 0.7},
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"❌ Error from model: {response.text}"


def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# Streamlit UI
st.set_page_config(page_title="Resume Analyzer AI", layout="centered")
st.title("✅ AI-Powered Resume Insights")

uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF)", type="pdf")

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Analyzing your resume with AI..."):
        prompt = f"""You are a professional resume evaluator. Analyze the following resume text and generate:

1. 📝 Resume Summary: A short summary about the candidate (in 2-4 lines).
2. 💼 Recommended Job Roles: Suggest 3 job roles suitable for this candidate.
3. 📌 Resume Improvement Tips: Give 3 tips to improve the resume.

Resume:
\"\"\"
{resume_text}
\"\"\"
"""

        output = query_llm(prompt)

    st.markdown("---")
    st.markdown("### 🧠 AI Response")
    st.markdown(output)
