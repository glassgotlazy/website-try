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

st.set_page_config(page_title="Question PDF Generator Pro", page_icon="📄", layout="wide", initial_sidebar_state="expanded")

st.title("📄 Question PDF Generator Pro")
st.markdown("**Create professional PDFs with one question per page + screenshots**")
st.markdown("---")

st.sidebar.header("⚙️ PDF Settings")

st.sidebar.subheader("📏 Page Layout")
page_size_option = st.sidebar.selectbox("Page Size", ["A4", "Letter", "Legal"])
if page_size_option == "A4":
    page_size = A4
elif page_size_option == "Letter":
    page_size = letter
else:
    from reportlab.lib.pagesizes import LEGAL
    page_size = LEGAL

orientation = st.sidebar.radio("Orientation", ["Portrait", "Landscape"])
if orientation == "Landscape":
    page_size = (page_size[1], page_size[0])

st.sidebar.subheader("✍️ Typography")
font_size = st.sidebar.slider("Question Font Size", 10, 20, 12)
font_family = st.sidebar.selectbox("Font Family", ["Helvetica", "Times-Roman", "Courier"])
question_color = st.sidebar.color_picker("Question Color", "#000000")

st.sidebar.subheader("📐 Spacing")
top_margin = st.sidebar.slider("Top Margin (inches)", 0.25, 2.0, 0.75, 0.25)
side_margin = st.sidebar.slider("Side Margin (inches)", 0.25, 2.0, 0.5, 0.25)

st.sidebar.subheader("📋 Header & Footer")
show_page_numbers = st.sidebar.checkbox("Page Numbers", value=True)
page_num_position = st.sidebar.selectbox("Page Number Position", ["Center", "Left", "Right"])
show_header = st.sidebar.checkbox("Add Header", value=False)
if show_header:
    header_text = st.sidebar.text_input("He
