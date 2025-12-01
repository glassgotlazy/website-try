import streamlit as st
import tempfile
import os
import subprocess
import re
import io
import base64
from datetime import datetime
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from PIL import Image as PILImage

st.set_page_config(page_title="PDF Generator", page_icon="📄", layout="wide")
st.title("Question PDF Generator")
st.markdown("---")

st.sidebar.header("Settings")
page_size = st.sidebar.selectbox("Page Size", ["A4", "Letter"])
if page_size == "A4":
    page_size = A4
else:
    page_size = letter

font_size = st.sidebar.slider("Font Size", 10, 20, 12)
show_page_numbers = st.sidebar.checkbox("Page Numbers", value=True)
filename_prefix = st.sidebar.text_input("Filename", "questions")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Word Document")
    word_file = st.file_uploader("Word file", type=["docx"])

with col2:
    st.subheader("Upload Screenshots")
    screenshot_files = st.file_uploader("Screenshots", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

questions = []

if word_file:
    st.markdown("---")
    with st.spinner("Reading..."):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        tmp.write(word_file.getvalue())
        tmp.close()
        path = tmp.name

        try:
            doc = Document(path)

            for p in doc.paragraphs:
                txt = p.text.strip()
                if txt and len(txt) > 5:
                    questions.append(txt)

            for tbl in doc.tables:
                for row in tbl.rows:
                    for cell in row.cells:
                        txt = cell.text.strip()
                        if txt and len(txt) > 5:
                            if txt not in questions:
                              
