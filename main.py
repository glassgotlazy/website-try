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

st.set_page_config(page_title="Question PDF Generator", page_icon="📄", layout="wide")

st.title("Question PDF Generator Pro")
st.markdown("Create professional PDFs with one question per page")
st.markdown("---")

st.sidebar.header("Settings")
page_size_option = st.sidebar.selectbox("Page Size", ["A4", "Letter"])
page_size = A4 if page_size_option == "A4" else letter

orientation = st.sidebar.radio("Orientation", ["Portrait", "Landscape"])
if orientation == "Landscape":
    page_size = (page_size[1], page_size[0])

font_size = st.sidebar.slider("Font Size", 10, 20, 12)
font_family = st.sidebar.selectbox("Font", ["Helvetica", "Times-Roman", "Courier"])
top_margin = st.sidebar.slider("Top Margin", 0.5, 2.0, 0.75, 0.25)
side_margin = st.sidebar.slider("Side Margin", 0.5, 2.0, 0.5, 0.25)
show_page_numbers = st.sidebar.checkbox("Page Numbers", value=True)
page_num_position = st.sidebar.selectbox("Page Number Position", ["Center", "Left", "Right"])
number_style = st.sidebar.selectbox("Question Style", ["Q1:", "Question 1:", "1.", "[1]"])
max_img_width = st.sidebar.slider("Max Image Width", 3, 7, 6, 1)
filename_prefix = st.sidebar.text_input("Filename Prefix", "questions")
add_timestamp = st.sidebar.checkbox("Add Timestamp", value=False)

tab1, tab2, tab3 = st.tabs(["Upload Files", "Statistics", "Help"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Upload Word Document")
        word_file = st.file_uploader("Choose Word file", type=["doc", "docx"])

        if word_file:
            
