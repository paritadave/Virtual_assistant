import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(text, tone):
    """Summarize text with a given tone."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a summarization assistant. Produce a {tone.lower()} summary."},
                {"role": "user", "content": text}
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

def show_summary_tab():
    st.subheader("🧾 Text Summarizer")
    st.markdown("Summarize long text, articles, or reports with an AI-powered assistant.")

    text = st.text_area("📄 Paste your text", height=250)
    tone = st.selectbox("🎯 Summary Style", ["Formal", "Neutral", "Casual", "Bullet Points"])

    if st.button("✨ Generate Summary"):
        if text.strip():
            with st.spinner("Generating summary..."):
                summary = generate_summary(text, tone)
            st.success("✅ Summary Ready!")
            st.text_area("📘 Summary", summary, height=250)
        else:
            st.warning("Please enter text to summarize.")
