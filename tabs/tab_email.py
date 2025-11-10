import streamlit as st
import os
from openai import OpenAI

# Load key from Streamlit secrets if available
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_text_download_link(text, filename):
    st.download_button("📥 Download Email", text, file_name=filename)


# --- AI Email Generation Logic ---
def draft_email_with_ai(subject, recipient, tone, details, email_type, length):
    """Generate well-written, human-like email based on user inputs."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert business communication assistant. "
                        "Your job is to write clear, polite, and natural emails that feel human. "
                        "You expand short bullet points into full, well-phrased sentences. "
                        "Structure the email with a greeting, purpose, main message, and polite closing. "
                        "Avoid repetition and keep tone consistent."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Write a {email_type.lower()} email.\n"
                        f"Subject: {subject}\n"
                        f"Recipient: {recipient}\n"
                        f"Tone: {tone}\n"
                        f"Length: {length}\n"
                        f"Key points: {details}\n\n"
                        f"Make it engaging, coherent, and properly formatted as an email body with greeting and signature. "
                        f"Do NOT just list or rephrase the key points — turn them into complete sentences that sound natural."
                    ),
                },
            ],
            temperature=0.75,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Error generating email: {e}"


def show_email_tab():
    st.subheader("✉️ Smart Email Assistant")
    st.markdown("Generate context-aware, natural-sounding emails.")

    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("📌 Subject", placeholder="e.g., Follow up on proposal discussion")
    with col2:
        recipient = st.text_input("👤 Recipient", placeholder="e.g., Client, Manager, Vendor")

    tone = st.selectbox(
        "🎯 Select Tone",
        ["Professional", "Friendly", "Apologetic", "Persuasive", "Formal", "Casual", "Appreciative"],
    )

    email_type = st.selectbox(
        "📂 Email Type",
        ["Follow-up", "Apology", "Introduction", "Marketing", "Internal Update", "Thank You", "Request/Inquiry"],
    )

    length = st.radio(
        "🧾 Email Length",
        ["Short (3–4 lines)", "Medium (1 paragraph)", "Detailed (2–3 paragraphs)"],
        horizontal=True,
    )

    details = st.text_area(
        "🪶 Key Points (What do you want to say?)",
        placeholder="e.g., Thank them for their time, mention next steps, confirm meeting time...",
        height=150,
    )

    if st.button("🪄 Generate Email"):
        if not subject or not recipient or not details:
            st.warning("⚠️ Please fill in all required fields.")
            return

        with st.spinner("📧 Crafting your email..."):
            email_output = draft_email_with_ai(subject, recipient, tone, details, email_type, length)

        st.success("✅ Email draft generated!")
        st.text_area("📧 Email Preview", email_output, height=300)
        get_text_download_link(email_output, "email_draft.txt")

        with st.expander("📋 Copy Email"):
            st.code(email_output, language="markdown")


