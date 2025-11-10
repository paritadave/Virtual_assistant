import streamlit as st
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Optional helper: generates download link ---
def get_text_download_link(text, filename):
    """Generate a Streamlit download button for text content."""
    st.download_button("📥 Download Email", text, file_name=filename)


# --- Email generation logic (AI version) ---
def draft_email_with_ai(subject, recipient, tone, details):
    """Use OpenAI to generate a polished email draft."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert email-writing assistant. "
                        "Write clear, natural, and professional emails with the given context. "
                        "Keep the message tone consistent and human-like."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Write an email with the following details:\n\n"
                        f"Subject: {subject}\n"
                        f"Recipient: {recipient}\n"
                        f"Tone: {tone}\n\n"
                        f"Details: {details}\n\n"
                        f"Include a proper greeting and closing."
                    ),
                },
            ],
            temperature=0.6,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error generating email: {e}"


# --- Streamlit UI ---
def show_email_tab():
    st.subheader("✉️ Email Drafting Assistant")
    st.markdown("Generate professional, personalized emails using AI.")

    subject = st.text_input("📌 Subject", "Follow up on order status", key="email_subject")
    recipient = st.text_input("👤 Recipient", "Customer or Supplier", key="email_recipient")
    tone = st.selectbox(
        "🎯 Tone",
        ["Professional", "Friendly", "Apologetic", "Persuasive", "Formal", "Casual"],
        key="email_tone",
    )
    details = st.text_area(
        "🧾 Key Details",
        "Thank them for their time, confirm shipment, request feedback.",
        key="email_details",
    )

    if st.button("🪄 Generate Email", key="generate_email"):
        if not subject or not recipient or not details:
            st.warning("⚠️ Please fill in all required fields.")
            return

        with st.spinner("✉️ Drafting your AI-powered email..."):
            email_output = draft_email_with_ai(subject, recipient, tone, details)

        st.success("✅ Email draft generated!")
        st.text_area("📧 Draft Preview", email_output, height=300)
        get_text_download_link(email_output, "email_draft.txt")
