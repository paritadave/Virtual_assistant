import streamlit as st
import docx2txt
from PyPDF2 import PdfReader

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


# --- Simple summarization logic ---
def summarize_text(text, length_option):
    """Generate a basic extractive summary based on desired length."""
    sentences = text.split(". ")
    if not sentences:
        return "⚠️ No content to summarize."

    if length_option == "Very short (1–2 lines)":
        summary = ". ".join(sentences[:2])
    elif length_option == "Short (3–5 lines)":
        summary = ". ".join(sentences[:5])
    else:  # Detailed paragraph
        summary = ". ".join(sentences[:10])

    return summary.strip() + ("..." if len(sentences) > len(summary.split(". ")) else "")


# --- Download helper ---
def get_text_download_link(text, filename):
    """Generate a Streamlit download button for text content."""
    st.download_button("📥 Download Summary", text, file_name=filename)


# --- Streamlit UI ---
def show_summary_tab():
    st.subheader("📄 Document Summarization")
    st.markdown("Upload a file or paste text to generate a concise summary.")

    uploaded_file = st.file_uploader(
        "📎 Upload a file (.txt, .pdf, .docx)",
        type=["txt", "pdf", "docx"],
        key="summary_upload"
    )

    # Extract text from uploaded file
    default_text = ""
    if uploaded_file:
        with st.spinner("📖 Extracting text..."):
            default_text = extract_uploaded_text(uploaded_file)

    # Input text area
    text_input = st.text_area(
        "📝 Paste long text or report",
        value=default_text,
        height=250,
        key="summary_text"
    )

    # Summary length options
    length = st.selectbox(
        "🧠 Choose summary length",
        ["Very short (1–2 lines)", "Short (3–5 lines)", "Detailed paragraph"],
        key="summary_length"
    )

    # Summarize button
    if st.button("✨ Summarize Document", key="summarize_doc"):
        if text_input.strip():
            with st.spinner("Summarizing..."):
                summary = summarize_text(text_input, length)
            st.success("✅ Summary generated!")
            st.text_area("🧾 Summary Output", summary, height=250)
            get_text_download_link(summary, "summary.txt")
        else:
            st.warning("⚠️ Please provide text to summarize.")
