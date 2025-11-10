import streamlit as st
import os
from openai import OpenAI
from PyPDF2 import PdfReader
import docx2txt

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_uploaded_text(uploaded_file):
    text = ""
    if uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        pdf = PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif uploaded_file.name.endswith(".docx"):
        text = docx2txt.process(uploaded_file)
    return text.strip()

def editorial_support(text, goal):
    """Use GPT to improve the text."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert writing assistant."},
                {"role": "user", "content": f"Improve this text with the goal: {goal}.\n\n{text}"}
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

def show_edit_tab():
    st.subheader("✍️ Editorial Support")
    st.markdown("Refine and polish your writing.")

    uploaded_edit = st.file_uploader("📎 Upload a file (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])
    default_edit_text = ""

    if uploaded_edit:
        with st.spinner("📖 Extracting text..."):
            default_edit_text = extract_uploaded_text(uploaded_edit)

    raw_text = st.text_area("📝 Enter or paste your text", value=default_edit_text, height=250)
    goal = st.selectbox("🎯 Editing Goal", [
        "Make it concise",
        "Improve grammar",
        "Enhance tone",
        "Make it persuasive",
        "Simplify language"
    ])

    if st.button("✨ Enhance Text"):
        if raw_text.strip():
            with st.spinner("Improving text..."):
                improved = editorial_support(raw_text, goal)
            st.success("✅ Enhanced Text Ready!")
            st.text_area("📘 Refined Output", improved, height=300)
        else:
            st.warning("⚠️ Please provide text for editing.")

