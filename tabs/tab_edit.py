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


# --- Text refinement logic ---
def editorial_support(text, goal):
    """Apply basic editing based on selected goal."""
    improved = text.strip()

    if goal == "Make it concise":
        words = improved.split()
        improved = " ".join(words[:100]) + ("..." if len(words) > 100 else "")

    elif goal == "Improve grammar":
        # Simple grammar placeholder — can be replaced with AI later
        improved = improved.replace("i ", "I ").replace(" dont ", " don't ").replace(" cant ", " can't ")

    elif goal == "Enhance tone":
        improved = improved.replace("sorry", "I apologize").replace("please", "kindly")

    elif goal == "Make it persuasive":
        improved = improved + "\n\nI truly believe this will make a positive impact!"

    return improved


# --- Download helper ---
def get_text_download_link(text, filename):
    """Generate a Streamlit download button for text content."""
    st.download_button("📥 Download Enhanced Text", text, file_name=filename)


# --- Streamlit UI ---
def show_edit_tab():
    st.subheader("✍️ Editorial Support")
    st.markdown("Refine your writing — make it concise, polished, and impactful.")

    uploaded_edit = st.file_uploader(
        "📎 Upload a file (.txt, .pdf, .docx)",
        type=["txt", "pdf", "docx"],
        key="edit_upload"
    )

    default_edit_text = ""
    if uploaded_edit:
        with st.spinner("📖 Extracting text..."):
            default_edit_text = extract_uploaded_text(uploaded_edit)

    raw_text = st.text_area(
        "📝 Enter or paste your text (blog, proposal, email, etc.)",
        value=default_edit_text,
        height=250,
        key="edit_text"
    )

    goal = st.selectbox(
        "🎯 Editing Goal",
        ["Make it concise", "Improve grammar", "Enhance tone", "Make it persuasive","Simplify Language"],
        key="edit_goal"
    )

    if st.button("✨ Enhance Text", key="enhance_text"):
        if raw_text.strip():
            with st.spinner("Improving text..."):
                improved = editorial_support(raw_text, goal)
            st.success("✅ Enhanced Text Ready!")
            st.text_area("📘 Refined Output", improved, height=300)
            get_text_download_link(improved, "edited_text.txt")
        else:
            st.warning("⚠️ Please provide text for editing.")
