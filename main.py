port tempfile
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

def convert_doc(path):
    try:
        outdir = tempfile.gettempdir()
        subprocess.run(["libreoffice", "--headless", "--convert-to", "docx", "--outdir", outdir, path], capture_output=True, timeout=30)
        base = os.path.splitext(os.path.basename(path))[0]
        converted = os.path.join(outdir, base + ".docx")
        if os.path.exists(converted):
            return converted
        return None
    except Exception:
        return None

questions = []

if word_file:
    st.markdown("---")
    with st.spinner("Reading document..."):
        try:
            ext = ".docx" if word_file.name.endswith(".docx") else ".doc"
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
            tmp.write(word_file.getvalue())
            tmp.close
