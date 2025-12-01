import streamlit as st
from docx import Document
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import os
import tempfile
from PIL import Image as PILImage

st.set_page_config(page_title="Question PDF Generator", layout="wide")

st.title("📄 Question PDF Generator")
st.markdown("Convert your questions + screenshots into a professional PDF (one question per page)")

# Sidebar for settings
st.sidebar.header("⚙️ Settings")
page_size_option = st.sidebar.selectbox(
    "Page Size",
    ["A4", "Letter"],
    help="Choose your preferred page size"
)
page_size = A4 if page_size_option == "A4" else letter

font_size = st.sidebar.slider("Question Font Size", 10, 18, 14)
include_page_numbers = st.sidebar.checkbox("Add page numbers", value=True)

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Upload Word Document")
    word_file = st.file_uploader(
        "Select your Word file with 40 questions",
        type=["docx"],
        help="One question per paragraph (Must be .docx format)"
    )

with col2:
    st.subheader("🖼️ Upload Screenshots")
    screenshot_files = st.file_uploader(
        "Upload screenshots (in order)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help="Name them: 1.png, 2.png, etc. or upload in correct order"
    )

# Extract questions from Word document
questions = []
if word_file:
    try:
        # Save uploaded file to a temporary location with proper handling
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            tmp_file.write(word_file.getvalue())
            tmp_path = tmp_file.name

        # Read the document
        doc = Document(tmp_path)

        for para in doc.paragraphs:
            text = para.text.strip()
            if text:  # Only add non-empty paragraphs
                questions.append(text)

        # Clean up temp file
        os.unlink(tmp_path)

        st.success(f"✅ Found {len(questions)} questions in the document")

        with st.expander("👀 Preview Questions"):
            for i, q in enumerate(questions[:5], 1):
                st.write(f"**Q{i}:** {q[:100]}...")
            if len(questions) > 5:
                st.write(f"... and {len(questions) - 5} more questions")

    except Exception as e:
        st.error(f"❌ Error reading Word document: {str(e)}")
        st.info("💡 Make sure you uploaded a valid .docx file (Word 2007 or later)")
        questions = []

# Process screenshots
screenshots_dict = {}
if screenshot_files:
    st.info(f"📸 {len(screenshot_files)} screenshot(s) uploaded")

    # Organize screenshots by number in filename
    import re
    for idx, file in enumerate(screenshot_files):
        try:
            # Try to extract number from filename
            filename = file.name
            question_num = None

            # Look for number patterns like "1.", "1-", "q1", etc.
            numbers = re.findall(r'\d+', filename)
            if numbers:
                question_num = int(numbers[0])
            else:
                question_num = idx + 1

            screenshots_dict[question_num] = file

        except Exception as e:
            st.warning(f"⚠️ Could not process {file.name}: {str(e)}")

# Display screenshot mapping
if screenshots_dict and questions:
    with st.expander("🔗 Screenshot Mapping"):
        for q_num in sorted(screenshots_dict.keys()):
            if q_num <= len(questions):
                st.caption(f"Q{q_num}: {screenshots_dict[q_num].name}")

# Generate PDF button
if questions:
    st.markdown("---")

    if st.button("✨ Generate PDF", type="primary", use_container_width=True):
        try:
            with st.spinner("Generating your PDF..."):
                # Create PDF in memory
                pdf_buffer = io.BytesIO()

                doc = SimpleDocTemplate(
                    pdf_buffer,
                    pagesize=page_size,
                    rightMargin=0.5*inch,
                    leftMargin=0.5*inch,
                    topMargin=0.75*inch,
                    bottomMargin=0.75*inch
                )

                # Create styles
                styles = getSampleStyleSheet()
                question_style = ParagraphStyle(
                    'CustomQuestion',
                    parent=styles['Normal'],
                    fontSize=font_size,
                    textColor=colors.HexColor("#1a1a1a"),
                    spaceAfter=0.3*inch,
                    alignment=0,  # Left align
                    leading=1.4*font_size,
                    fontName='Helvetica-Bold'
                )

                # Build PDF content
                story = []

                for q_num, question in enumerate(questions, 1):
                    # Add question number and text
                    question_text = f"<b>Question {q_num}:</b><br/>{question}"
                    question_para = Paragraph(question_text, question_style)
                    story.append(question_para)

                    # Add screenshot if available
                    if q_num in screenshots_dict:
                        try:
                            screenshot_file = screenshots_dict[q_num]

                            # Reset file pointer
                            screenshot_file.seek(0)

                            # Create temporary file for image
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_img:
                                tmp_img.write(screenshot_file.read())
                                tmp_img_path = tmp_img.name

                            # Get image dimensions
                            img_pil = PILImage.open(tmp_img_path)
                            img_width, img_height = img_pil.size

                            # Calculate scaling
                            max_width = page_size[0] - 1*inch
                            max_height = page_size[1] - 2.5*inch  # Leave room for question

                            aspect_ratio = img_height / img_width
                            img_width_scaled = min(max_width, 6*inch)
                            img_height_scaled = img_width_scaled * aspect_ratio

                            # If height is too large, scale down
                            if img_height_scaled > max_height:
                                img_height_scaled = max_height
                                img_width_scaled = img_height_scaled / aspect_ratio

                            # Add spacing
                            story.append(Spacer(1, 0.2*inch))

                            # Add screenshot
                            img = Image(
                                tmp_img_path,
                                width=img_width_scaled,
                                height=img_height_scaled
                            )
                            story.append(img)

                            # Clean up temp image file
                            os.unlink(tmp_img_path)

                        except Exception as e:
                            st.warning(f"⚠️ Could not embed screenshot for Q{q_num}: {str(e)}")

                    # Add page break after each question (except the last one)
                    if q_num < len(questions):
                        story.append(PageBreak())

                # Add page numbers if selected
                if include_page_numbers:
                    def add_page_number(canvas_obj, doc_obj):
                        canvas_obj.saveState()
                        canvas_obj.setFont("Helvetica", 9)
                        canvas_obj.setFillColor(colors.grey)
                        page_num = doc_obj.page
                        text = f"Page {page_num}"
                        canvas_obj.drawCentredString(
                            page_size[0]/2,
                            0.4*inch,
                            text
                        )
                        canvas_obj.restoreState()

                    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
                else:
                    doc.build(story)

                # Get PDF bytes
                pdf_bytes = pdf_buffer.getvalue()

                # Display success message
                st.success(f"✅ PDF generated successfully!")

                # Stats
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("Total Questions", len(questions))
                with col_stat2:
                    st.metric("Screenshots Embedded", len(screenshots_dict))
                with col_stat3:
                    st.metric("Total Pages", len(questions))

                # Download button
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_bytes,
                    file_name="questions_with_screenshots.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"❌ Error generating PDF: {str(e)}")
            st.exception(e)
else:
    st.info("👆 Please upload a Word document with your questions to get started")

# Instructions
with st.expander("📚 How to use this app"):
    st.markdown("""
### Step-by-Step Guide:

1. **Prepare Your Word Document**
   - Create a .docx file (Word 2007 or later)
   - Each question should be a separate paragraph
   - Save the file

2. **Upload Word Document**
   - Click the uploader in the left column
   - Select your .docx file
   - The app will extract all questions automatically

3. **Prepare Screenshots (Optional)**
   - Name them like: 1.png, 2.png, 3.png etc.
   - Or use any naming scheme with numbers
   - Upload them in the right column

4. **Configure Settings** (Sidebar)
   - Choose page size (A4 or Letter)
   - Adjust font size
   - Enable/disable page numbers

5. **Generate PDF**
   - Click "Generate PDF" button
   - Wait for processing
   - Download your PDF

### Features:
- One question per page
- Screenshots embedded below questions
- Auto-scaling images
- Page numbers (optional)
- Professional formatting
    """)

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
