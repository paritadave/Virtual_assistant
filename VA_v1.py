
import sys, os
# Add the directory containing VA_v1.py to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#import os, sys
print("Current working directory:", os.getcwd())
print("Python search paths:", sys.path)
import streamlit as st
import base64
from pathlib import Path



# Import tab modules
from tabs.tab_email import show_email_tab
from tabs.tab_summary import show_summary_tab
from tabs.tab_edit import show_edit_tab
#from tabs.tab_ocr import show_ocr_tab
from tabs.tab_about import show_about_tab

# ---------- Streamlit Page Setup ----------
st.set_page_config(
    page_title="AI Virtual Assistant",
    layout="centered",
    page_icon="🤖",
    initial_sidebar_state="expanded"
)

# ==========================================================
# 🌙 Dark Theme + Styling
# ==========================================================
st.markdown(
    """
    <style>
    .main, .block-container {
        background-color: #121212;
        color: #e0e0e0;
    }
    .main-header {
        background: linear-gradient(90deg, #1f2937 0%, #111827 100%);
        padding: 1.8rem;
        border-radius: 16px;
        text-align: center;
        color: #ffffff;
        margin-bottom: 0.5rem;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.5);
    }
    .main-header h1 {
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    [data-testid="stSidebar"] {
        background-color: #1f2937;
        color: #e0e0e0;
    }
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 0.5rem;
    }
    .sidebar-text {
        font-size: 1rem;
        line-height: 1.8;
        color: #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# 🌟 Header with Logo + Title + Subtitle
# ==========================================================
logo_path = Path("ML Logo 1.png")

def render_header():
    logo_html = ""
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode("utf-8")
            logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="90" style="border-radius:12px; margin-bottom:10px;">'

    st.markdown(
        f"""
        <div class="main-header">
            {logo_html}
            <h1>AI Assistant</h1>
            <p style="color:#38bdf8; font-size:18px; margin-top:0;">
                Your intelligent virtual assistant for daily automation 🤖
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

render_header()

# ==========================================================
# 🌟 Animated greeting outside header
# ==========================================================
st.markdown(
    "<p style='color:#38bdf8;font-size:16px;'>🚀 Ready to simplify your workday? Let's automate your emails, documents, and more!</p>",
    unsafe_allow_html=True
)

# ==========================================================
# Sidebar
# ==========================================================
st.sidebar.markdown("<div class='sidebar-title'>🧠 What this Assistant Does</div>", unsafe_allow_html=True)
st.sidebar.markdown(
    """
    <div class='sidebar-text'>
    • ✉️ Email Drafting – Streamline customer and supplier communication<br>
    • 📄 Document Summarization – Speed up reviews of contracts, reports, and long documents<br>
    • ✍️ Editorial Support – Improve written content (blogs, proposals, marketing)<br>
    </div>
    """, 
    unsafe_allow_html=True
) #• 🖼️ Image-to-Text Conversion – Digitize invoices, notes, and receipts
st.sidebar.markdown("---")
st.sidebar.success("💡 Tip: Upload a document or paste it to see the assistant in action!") #Upload a document or image to see the assistant in action!

# ---------- TABS ----------
tabs = st.tabs([
    "Email Drafting",
    "Summarization",
    "Editorial Support",
    #"Image → Text (OCR)",
    "About"
])

with tabs[0]:
    show_email_tab()

with tabs[1]:
    show_summary_tab()

with tabs[2]:
    show_edit_tab()

#with tabs[3]:
 #   show_ocr_tab()

with tabs[3]:
    show_about_tab()
