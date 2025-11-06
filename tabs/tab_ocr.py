import streamlit as st
import cv2
import numpy as np
import re
from PIL import Image, ImageEnhance

import streamlit as st
import easyocr

@st.cache_resource  # ✅ only loads once per app session
def get_easyocr_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = get_easyocr_reader()

# =============================
# ✅ Load EasyOCR
# =============================
#try:
 #   import easyocr
  #  reader = easyocr.Reader(['en'], gpu=False)  # Force CPU mode to avoid CUDA issues
   # EASY_AVAILABLE = True
    #print("✅ EasyOCR loaded successfully.")
#except Exception as e:
 #   EASY_AVAILABLE = False
  #  print(f"⚠️ EasyOCR failed to load: {e}")

# =============================
# 🔧 Preprocessing Function
# =============================
def preprocess_image(image):
    """Enhance image for better OCR accuracy on receipts/invoices."""
    img = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Slight brightness & contrast boost
    pil_img = Image.fromarray(gray)
    pil_img = ImageEnhance.Brightness(pil_img).enhance(1.1)
    pil_img = ImageEnhance.Contrast(pil_img).enhance(1.5)
    gray = np.array(pil_img)

    # Light noise reduction (helps EasyOCR focus)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    return gray

def clean_ocr_text(text):
    # Fix common OCR mistakes
    replacements = {
        "Toial": "Total",
        "S": "$",
        "Am": "",
        "EXPIRES": "",
        "PAYMENT": "",
        "CAED": "CARD",
        "GIei": "GIFT",
        "CASUNNGE": "CASH"
    }
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    
    # Remove lines that are only numbers, dates, or empty
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    filtered_lines = []
    for l in lines:
        if re.match(r'^[\d\s/.,$]+$', l):  # skip lines with only numbers/symbols
            continue
        filtered_lines.append(l)
    
    return "\n".join(filtered_lines)
    

# =============================
# 🔍 OCR Extraction
# =============================
def extract_text(image):
    """Extract text using EasyOCR."""
    try:
        processed = preprocess_image(image)
        result = reader.readtext(processed, detail=0, paragraph=True)
        text = "\n".join(result)
        return text.strip()
    except Exception as e:
        return f"⚠️ OCR failed: {e}"


# =============================
# 🧾 Parse Text for Useful Info
# =============================
def parse_text(text):
    """Clean and extract structured data."""
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = text.replace("  ", " ")

    # More flexible patterns
    store_pattern = r'(?i)(store|shop|market|mart|supermarket|inc|co|ltd|llc|receipt|invoice)\s?.{0,60}'
    date_pattern = r'(\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b)'
    total_pattern = r'(?i)(total|amount\s+due|balance\s+due|grand\s+total)[^\d]*(\d+[.,]\d{2})'

    store = re.search(store_pattern, text)
    date = re.search(date_pattern, text)
    total = re.search(total_pattern, text)

    # Lines with prices
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    items = [l for l in lines if re.search(r'[A-Za-z]{2,}.*\d+[.,]\d{2}', l)]

    readable = []
    if store:
        readable.append(f"🛒 Store: {store.group(0)}")
    if date:
        readable.append(f"📅 Date: {date.group(1)}")
    if total:
        readable.append(f"💰 Total: ${total.group(2)}")

    readable.append("\n🧾 Detected Items:")
    if items:
        readable.extend([f"{i+1}. {item}" for i, item in enumerate(items)])
    else:
        readable.append("No items detected.")

    return "\n".join(readable), {
        "store": store.group(0) if store else None,
        "date": date.group(1) if date else None,
        "total": total.group(2) if total else None,
        "items": items,
    }


# =============================
# 🎨 Streamlit Tab UI
# =============================
def show_ocr_tab():
    st.subheader("🖼️ Image → Text Conversion (EasyOCR)")

    uploaded = st.file_uploader(
        "Upload invoice, receipt, or note",
        type=["png", "jpg", "jpeg", "tiff", "bmp", "webp"]
    )

    if uploaded:
        img = Image.open(uploaded)
        st.image(img, caption="Uploaded Image", use_container_width=True)

        if st.button("Extract Text"):
            with st.spinner("🔍 Extracting text using EasyOCR..."):
                text = extract_text(img)
                readable, structured = parse_text(text)

            st.success("✅ Extraction Complete!")
            st.text_area("🧾 Cleaned Text", value=readable, height=400)
            st.download_button("📥 Download Extracted Text", readable, file_name="ocr_extracted.txt")

            with st.expander("🔍 Structured Output"):
                st.json(structured)
