import streamlit as st
import docx2txt
from PyPDF2 import PdfReader
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# --- Helper: extract text from uploaded files ---
def extract_uploaded_text(uploaded_file):
    """Extract text from .txt, .pdf, or .docx files."""
    text = ""
    if uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        pdf = PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif uploaded_file.name.endswith(".docx"):
        text = docx2txt.process(uploaded_file)
    return text.strip()


# --- OpenAI-powered summarization ---
def openai_summarize_text(text, length_option):
    """Use OpenAI model to summarize text based on the chosen length."""
    length_prompt = {
        "Very short (1–2 lines)": "Summarize this text in 1–2 concise lines.",
        "Short (3–5 lines)": "Summarize this text in 3–5 bullet points.",
        "Detailed paragraph": "Summarize this text in a detailed paragraph."
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional text summarizer."},
                {"role": "user", "content": f"{length_prompt[length_option]}\n\nText:\n{text}"}
            ],
            temperature=0.5,
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"⚠️ Error during summarization: {e}"


# --- Download helper ---
def get_text_download_link(text, filename):
    """Generate a Streamlit download button for text content."""
    st.download_button("📥 Download Summary", text, file_name=filename)


# --- Streamlit UI ---
def show_summary_tab():
    st.subheader("📄 Document Summarization")
    st.markdown("Upload a document or paste text to generate a concise summary.")

    uploaded_file = st.file_uploader(
        "📎 Upload a file (.txt, .pdf, .docx)",
        type=["txt", "pdf", "docx"],
        key="summary_upload"
    )
    # Extract text when file is uploaded
    extracted_text = ""
    if uploaded_file is not None:
        with st.spinner("📖 Extracting text..."):
            extracted_text = extract_uploaded_text(uploaded_file)

# Show a text area either way:
# - If file is uploaded: pre-fill with extracted text
# - If no file: show empty box for manual pasting
    text_input = st.text_area(
        "📝 Paste long text or report (optional if a file is uploaded)",
        value=extracted_text,
        height=250,
        key="summary_text"
    )

# Final text to use (either uploaded OR typed)
    final_text = text_input.strip()
    
    if not final_text:
        st.warning("Please upload a file or paste text to summarize.")
    else:
        # Proceed with summarization
        st.success("Text detected. Ready to summarize!")
        # Extract text from uploaded file
        default_text = ""
        if uploaded_file:
            with st.spinner("📖 Extracting text..."):
                default_text = extract_uploaded_text(uploaded_file)

    # Summary length options
    length = st.selectbox(
        "🧠 Choose summary length",
        ["Very short (1–2 lines)", "Short (3–5 lines)", "Detailed paragraph"],
        key="summary_length"
    )

    # Summarize button
    if st.button("✨ Summarize Document", key="summarize_doc"):
        if text_input.strip():
            with st.spinner("🤖 Generating AI summary..."):
                summary = openai_summarize_text(text_input, length)
            st.success("✅ Summary generated successfully!")
            st.text_area("🧾 Summary Output", summary, height=250)
            get_text_download_link(summary, "summary.txt")
        else:
            st.warning("⚠️ Please provide text to summarize.")


