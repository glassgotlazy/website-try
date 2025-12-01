import streamlit as st
import tempfile
import os
import subprocess
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from PIL import Image as PILImage
import io
import re

# ---- Streamlit page config ----
st.set_page_config(page_title="Question PDF Generator", layout="wide")
st.title("📄 Question PDF Generator")
st.markdown("Convert your questions and optional screenshots into a pro PDF (one question per page)")

# ---- Sidebar ----
st.sidebar.header('⚙️ Settings')
page_size_option = st.sidebar.selectbox("Page Size", ["A4", "Letter"])
page_size = A4 if page_size_option == "A4" else letter
font_size = st.sidebar.slider("Question Font Size", 10, 18, 14)
show_page_numbers = st.sidebar.checkbox("Page numbers", value=True)

# ---- File uploaders ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Upload Word Document")
    word_file = st.file_uploader(
        "Select .doc or .docx file with questions",
        type=["doc", "docx"]
    )

with col2:
    st.subheader("🖼️ Upload Screenshots")
    screenshot_files = st.file_uploader(
        "Upload screenshots (in order, optional)",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True
    )

# ---- Helper for doc -> docx conversion ----
def convert_doc_to_docx(in_path):
    try:
        output_dir = tempfile.gettempdir()
        subprocess.run(
            [
                'libreoffice', '--headless', '--convert-to', 'docx',
                '--outdir', output_dir, in_path
            ],
            check=True,
            capture_output=True
        )
        return os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(in_path))[0] + '.docx'
        )
    except Exception:
        st.error("Failed to convert .doc to .docx. Please save as .docx manually if this persists.")
        return None

# ---- Extract questions from Word file ----
questions = []
if word_file:
    is_docx = word_file.name.lower().endswith(".docx")
    with tempfile.NamedTemporaryFile(delete=False, suffix=('.docx' if is_docx else '.doc')) as tmp_file:
        tmp_file.write(word_file.read())
        tmp_path = tmp_file.name

    if not is_docx:
        st.info("Attempting to convert .doc to .docx format...")
        tmp_path_conv = convert_doc_to_docx(tmp_path)
        if tmp_path_conv:
            tmp_path = tmp_path_conv
        else:
            st.stop()

    from docx import Document
    try:
        doc = Document(tmp_path)

        # Paragraphs:
        for para in doc.paragraphs:
            text = para.text.strip()
            if text and len(text) > 5:
                questions.append(text)

        # Tables:
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text = cell.text.strip()
                    if text and len(text) > 5 and text not in questions:
                        questions.append(text)

        if not questions:
            st.error("No questions detected in file.")
        else:
            st.success(f"Detected {len(questions)} questions (or tasks).")
            with st.expander("Preview Questions"):
                for idx, q in enumerate(questions[:10]):
                    st.write(f"Q{idx+1}: {q[:100]}{'...' if len(q) > 100 else ''}")
                if len(questions) > 10:
                    st.write(f"...plus {len(questions) - 10} more.")
    except Exception as e:
        st.error(f"Problem reading Word document: {e}")

# ---- Screenshot mapping (question number -> UploadedFile) ----
screenshots_dict = {}
if screenshot_files:
    for idx, file in enumerate(screenshot_files):
        # Try to extract first number from filename; else fallback to index+1
        numbers = re.findall(r'\d+', file.name)
        num = int(numbers[0]) if numbers else idx + 1
        screenshots_dict[num] = file

# ---- PDF Generation ----
if questions:
    if st.button("✨ Generate PDF"):
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=page_size,
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch
        )

        styles = getSampleStyleSheet()
        qstyle = ParagraphStyle(
            "Question",
            parent=styles["Normal"],
            fontSize=font_size,
            alignment=0,  # left
            spaceAfter=0.4 * inch,
            textColor=colors.HexColor("#1a1a1a"),
        )

        story = []

        for q_num, question in enumerate(questions, 1):
            # Add question text
            story.append(Paragraph(f"Q{q_num}: {question}", qstyle))

            # Add screenshot if available
            if q_num in screenshots_dict:
                try:
                    uploaded_file = screenshots_dict[q_num]
                    uploaded_file.seek(0)
                    img_bytes = uploaded_file.read()

                    # Use PIL to get image size
                    pil_img = PILImage.open(io.BytesIO(img_bytes))
                    img_width, img_height = pil_img.size

                    # Calculate target size for PDF
                    max_width = page_size[0] - inch  # 0.5" margin each side
                    target_width = min(max_width, 5.5 * inch)
                    aspect = img_height / img_width
                    target_height = target_width * aspect

                    # BytesIO buffer for reportlab Image
                    img_buffer = io.BytesIO(img_bytes)

                    story.append(Spacer(1, 0.15 * inch))
                    story.append(
                        Image(img_buffer, width=target_width, height=target_height)
                    )
                except Exception as e:
                    st.warning(f"Could not embed screenshot for Q{q_num}: {e}")

            # Page break between questions
            if q_num < len(questions):
                story.append(PageBreak())

        # ---- Page numbers ----
        def add_page_number(canvas, doc_obj):
            if show_page_numbers:
                canvas.saveState()
                canvas.setFont("Helvetica", 8)
                canvas.setFillColor(colors.grey)
                canvas.drawCentredString(
                    page_size[0] / 2, 0.40 * inch, f"Page {doc_obj.page}"
                )
                canvas.restoreState()

        # Build the PDF
        doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
        pdf_bytes = pdf_buffer.getvalue()

        st.success(f"PDF generated: {len(questions)} pages!")
        st.download_button(
            label="📥 Download PDF",
            data=pdf_bytes,
            file_name="questions_with_screenshots.pdf",
            mime="application/pdf"
        )

# ---- Info and requirements ----
with st.expander("How to use this app"):
    st.markdown(
        """
1. Upload your `.doc` or `.docx` file listing questions or tasks.
2. Optionally upload screenshots, numbered to match question order (e.g. `Q1.png` → 1, `2_question.png` → 2).
3. Click **Generate PDF**. Each page = one question + matching screenshot (if provided).
4. Download and print or share your PDF.

- **For `.doc` files, LibreOffice must be installed.**
- On Streamlit Cloud, add `libreoffice` to `packages.txt`.
        """
    )

st.caption("Made with Streamlit · Supports .doc and .docx · Professional multipage PDF")
