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

st.set_page_config(page_title="Question PDF Generator Pro", page_icon="📄", layout="wide")

st.title("📄 Question PDF Generator Pro")
st.markdown("Create professional PDFs with one question per page")
st.markdown("---")

st.sidebar.header("⚙️ Settings")

st.sidebar.subheader("Page Layout")
page_size_option = st.sidebar.selectbox("Page Size", ["A4", "Letter"])
page_size = A4 if page_size_option == "A4" else letter

orientation = st.sidebar.radio("Orientation", ["Portrait", "Landscape"])
if orientation == "Landscape":
    page_size = (page_size[1], page_size[0])

st.sidebar.subheader("Typography")
font_size = st.sidebar.slider("Font Size", 10, 20, 12)
font_family = st.sidebar.selectbox("Font", ["Helvetica", "Times-Roman", "Courier"])

st.sidebar.subheader("Spacing")
top_margin = st.sidebar.slider("Top Margin", 0.5, 2.0, 0.75, 0.25)
side_margin = st.sidebar.slider("Side Margin", 0.5, 2.0, 0.5, 0.25)

st.sidebar.subheader("Options")
show_page_numbers = st.sidebar.checkbox("Page Numbers", value=True)
page_num_position = st.sidebar.selectbox("Page Number Position", ["Center", "Left", "Right"])
number_style = st.sidebar.selectbox("Question Style", ["Q1:", "Question 1:", "1.", "[1]"])
max_img_width = st.sidebar.slider("Max Image Width", 3, 7, 6, 1)

st.sidebar.subheader("Export")
filename_prefix = st.sidebar.text_input("Filename Prefix", "questions")
add_timestamp = st.sidebar.checkbox("Add Timestamp", value=False)

st.sidebar.markdown("---")
st.sidebar.info("Adjust settings as needed")

tab1, tab2, tab3 = st.tabs(["📤 Up
