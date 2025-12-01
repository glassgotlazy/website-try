import streamlit as st
import tempfile
import os
import re
import io
import base64
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from PIL import Image as PILImage

st.set_page_config(page_title="PDF Generator", layout="wide")
st.title("Question PDF Generator")

st.sidebar.header("Settings")
page_opt = st.sidebar.selectbox("Page Size", ["A4", "Letter"])
if page_opt == "A4":
    psize = A4
else:
    psize = letter

fname = st.sidebar.text_input("Filename", "questions")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Word Document")
    word_file = st.file_uploader("Upload docx", type=["docx"])

with col2:
    st.subheader("Screenshots")
    screens = st.file_uploader("Upload images", type=["png", "jpg"], accept_multiple_files=True)

questions = []

if word_file:
    with st.spinner("Reading..."):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        tmp.write(word_file.getvalue())
        tmp.close()

        try:
            doc = Document(tmp.name)
            for p in doc.paragraphs:
                txt = p.text.strip()
                if len(txt) > 5:
                    questions.append(txt)

            os.unlink(tmp.name)
            st.success(f"Found {len(questions)} questions")
        except Exception as e:
            st.error(str(e))

screenshots = {}
if screens:
    for f in screens:
        nums = re.findall(r"\d+", f.name)
        if nums:
            idx = int(nums[0])
            f.seek(0)
            screenshots[idx] = f.read()
    st.success(f"Loaded {len(screenshots)} screenshots")

def make_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=psize)
    styles = getSampleStyleSheet()
    story = []

    for i, q in enumerate(questions, 1):
        txt = f"<b>Q{i}:</b><br/><br/>{q}"
        stor
