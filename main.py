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

# Page configuration
st.set_page_config(
    page_title="Question PDF Generator",
    page_icon="📄",
    layout="wide"
)

# Title and description
st.title("📄 Question PDF Generator")
st.markdown("**Create professional PDFs with one question per page + optional screenshots**")

# Sidebar settings
st.sidebar.header("⚙️ PDF Settings")
page_size_option = st.sidebar.selectbox(
    "Page Size",
    ["A4", "Letter"],
    help="Select your preferred page size"
)
page_size = A4 if page_size_option == "A4" else letter

font_size = st.sidebar.slider(
    "Question Font Size",
    min_value=10,
    max_value=18,
    value=12,
    help="Adjust the font size for questions"
)

show_page_numbers = st.sidebar.checkbox(
    "Show page numbers",
    value=True,
    help="Add page numbers at the bottom of each page"
)

# Main layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Step 1: Upload Word Document")
    word_file = st.file_uploader(
        "Choose your Word file",
        type=["doc", "docx"],
        help="Upload a .doc or .docx file containing your questions"
    )

with col2:
    st.subheader("🖼️ Step 2: Upload Screenshots (Optional)")
    screenshot_files = st.file_uploader(
        "Choose screenshot files",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help="Name files as: 1.png, 2.png, 3.png, etc. for correct ordering"
    )

# Function to convert .doc to .docx
def convert_doc_to_docx(doc_path):
    """
    Convert .doc file to .docx format using LibreOffice
    Returns the path to the converted file or None i
