import streamlit as st
import tempfile
import os
import subprocess
import re
import io
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from PIL import Image as PILImage

st.set_page_config(page_title="Question PDF Generator", page_icon="📄", layout="wide")

st.title("📄 Question PDF Generator")
st.markdown("Create professional PDFs with one question per page")

st.sidebar.header("⚙️ Settings")
page_size_option = st.sidebar.selectbox("Page Size", ["A4", "Letter"])
page_size = A4 if page_size_option == "A4" else letter
font_size = st.sidebar.slider("Font Size", 10, 18, 12)
show_page_numbers = st.sidebar.checkbox("Page numbers", value=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Upload Word Document")
    word_file = st.file_uploader("Choose Word file", type=["doc", "docx"])

with col2:
    st.subheader("🖼️ Upload Screenshots")
    screenshot_files = st.file_uploader("Choose screenshots", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

def convert_doc_to_docx(doc_path):
    try:
        output_dir = tempfile.gettempdir()
        result = subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "docx", "--outdir", output_dir, doc_path],
            capture_output=True,
            timeout=30
        )
        base_name = os.path.splitext(os.path.basename(doc_path))[0]
        converted = os.path.join(output_dir, base_name + ".docx")
        return converted if os.path.exists(converted) else None
    except:
        return None

questions = []

if word_file:
    st.markdown("---")

    with st.spinner("Reading document..."):
        try:
            file_ext = ".docx" if word_file.name.endswith(".docx") else ".doc"

            temp_file = tempfile.NamedTemporaryFile(delete=False,
