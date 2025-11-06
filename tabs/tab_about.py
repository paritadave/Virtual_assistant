import streamlit as st

def show_about_tab():
    st.subheader("ℹ️ About This Assistant")

    st.markdown("""
### 🤖 AI Virtual Assistant v1.0
Developed to automate everyday tasks like:
- ✉️ Drafting emails  
- 📄 Summarizing long documents  
- ✍️ Improving writing style  
- 🖼️ Extracting text from images  

### 💡 Tech Stack
- **Frontend:** Streamlit  
- **Backend:** Python  
- **Libraries:** OpenAI, Pytesseract, EasyOCR, Numpy, Pandas  

Built for convenience, efficiency, and creativity.
""")
