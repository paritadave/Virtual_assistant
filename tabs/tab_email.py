import streamlit as st

# --- Optional helper: generates download link ---
def get_text_download_link(text, filename):
    """Generate a Streamlit download button for text content."""
    st.download_button("📥 Download Email", text, file_name=filename)


# --- Email generation logic ---
def draft_email(subject, recipient, tone, details):
    """Generate an email draft based on user inputs."""
    tone_styles = {
        "Professional": "I hope this message finds you well.",
        "Friendly": "I hope you're having a great day!",
        "Apologetic": "Please accept my sincere apologies for any inconvenience caused.",
        "Persuasive": "I truly believe this could be a great opportunity for you.",
        "Formal": "I am writing to you regarding the following matter.",
        "Casual": "Just wanted to quickly reach out about this."
    }

    tone_opening = tone_styles.get(tone, "I hope this message finds you well.")

    email = f"""\
Subject: {subject}

Dear {recipient},

{tone_opening}

{details}

Best regards,  
[Your Name]
"""
    return email


# --- Streamlit UI ---
def show_email_tab():
    st.subheader("✉️ Email Drafting Assistant")
    st.markdown("This tool helps you generate professional and personalized email drafts using AI.")

    subject = st.text_input("📌 Subject", "Follow up on order status", key="email_subject")
    recipient = st.text_input("👤 Recipient", "Customer or Supplier", key="email_recipient")
    tone = st.selectbox(
        "🎯 Tone",
        ["Professional", "Friendly", "Apologetic", "Persuasive", "Formal", "Casual"],
        key="email_tone"
    )
    details = st.text_area(
        "🧾 Key Details",
        "Thank them for their time, confirm shipment, request feedback.",
        key="email_details"
    )

    if st.button("🪄 Generate Email", key="generate_email"):
        if not subject or not recipient or not details:
            st.warning("⚠️ Please fill in all required fields.")
            return

        with st.spinner("✉️ Drafting your email..."):
            email_output = draft_email(subject, recipient, tone, details)

        st.success("✅ Email draft generated!")
        st.text_area("📧 Draft Preview", email_output, height=300)
        get_text_download_link(email_output, "email_draft.txt")
