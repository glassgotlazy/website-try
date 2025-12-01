 import streamlit as st
from docx import Document
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
import os
from pathlib import Path
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
        type=["docx", "doc"],
        help="One question per paragraph"
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
        doc = Document(word_file)
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:  # Only add non-empty paragraphs
                questions.append(text)
        
        st.success(f"✅ Found {len(questions)} questions in the document")
        
        with st.expander("👀 Preview Questions"):
            for i, q in enumerate(questions[:5], 1):
                st.write(f"**Q{i}:** {q[:100]}...")
            if len(questions) > 5:
                st.write(f"... and {len(questions) - 5} more questions")
    
    except Exception as e:
        st.error(f"❌ Error reading Word document: {str(e)}")
        questions = []

# Process screenshots
screenshots_dict = {}
if screenshot_files:
    st.info(f"📸 {len(screenshot_files)} screenshot(s) uploaded")
    
    # Try to organize screenshots by number in filename
    for idx, file in enumerate(screenshot_files):
        try:
            img = PILImage.open(file)
            # Try to extract number from filename
            filename = file.name
            question_num = None
            
            # Look for number patterns like "1.", "1-", etc.
            import re
            numbers = re.findall(r'\d+', filename)
            if numbers:
                question_num = int(numbers[0])
            else:
                question_num = idx + 1
            
            screenshots_dict[question_num] = file
            st.caption(f"Screenshot for Q{question_num}: {file.name}")
        except Exception as e:
            st.warning(f"⚠️ Could not process {file.name}: {str(e)}")

# Generate PDF button
if questions:
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        if st.button("✨ Generate PDF", key="generate", use_container_width=True):
            try:
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
                    textColor=colors.HexColor("#134252"),
                    spaceAfter=0.3*inch,
                    alignment=4,  # Left align
                    leading=1.4*font_size,
                    fontName='Helvetica-Bold'
                )
                
                page_num_style = ParagraphStyle(
                    'PageNum',
                    parent=styles['Normal'],
                    fontSize=9,
                    textColor=colors.grey,
                    alignment=1  # Center
                )
                
                # Build PDF content
                story = []
                
                for q_num, question in enumerate(questions, 1):
                    # Add question
                    question_para = Paragraph(f"<b>Q{q_num}:</b> {question}", question_style)
                    story.append(question_para)
                    
                    # Add screenshot if available
                    if q_num in screenshots_dict:
                        try:
                            screenshot_file = screenshots_dict[q_num]
                            
                            # Convert file to PIL Image to get dimensions
                            img_pil = PILImage.open(screenshot_file)
                            img_width, img_height = img_pil.size
                            
                            # Calculate max width (page width - margins)
                            max_width = page_size[0] - 1*inch
                            
                            # Scale image to fit page
                            aspect_ratio = img_height / img_width
                            img_width_scaled = min(max_width, 5*inch)
                            img_height_scaled = img_width_scaled * aspect_ratio
                            
                            # Add some spacing
                            story.append(Spacer(1, 0.2*inch))
                            
                            # Add screenshot
                            img = Image(
                                screenshot_file,
                                width=img_width_scaled,
                                height=img_height_scaled
                            )
                            story.append(img)
                            
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
                        canvas_obj.drawString(
                            page_size[0]/2,
                            0.4*inch,
                            f"Page {page_num}"
                        )
                        canvas_obj.restoreState()
                    
                    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
                else:
                    doc.build(story)
                
                # Get PDF bytes
                pdf_bytes = pdf_buffer.getvalue()
                
                # Display success message
                st.success(f"✅ PDF generated successfully with {len(questions)} questions!")
                
                # Download button
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_bytes,
                    file_name="questions_with_screenshots.pdf",
                    mime="application/pdf",
                    key="download"
                )
                
                # Show stats
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("Total Questions", len(questions))
                with col_stat2:
                    st.metric("Screenshots Embedded", len(screenshots_dict))
                with col_stat3:
                    st.metric("Total Pages", len(questions))
                
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
       - Create a .docx file with 40 questions
       - Each question should be a separate paragraph
       - Save the file
    
    2. **Upload Word Document**
       - Click the uploader in the left column
       - Select your Word file
       - The app will extract all questions automatically
    
    3. **Prepare Screenshots (Optional)**
       - Name them like: `1.png`, `2.png`, ... or any naming scheme
       - Screenshots will be paired with questions in upload order
       - Or let the app match by filename numbers
    
    4. **Configure Settings** (Optional)
       - Choose page size (A4 or Letter)
       - Adjust font size for questions
       - Enable/disable page numbers
    
    5. **Generate PDF**
       - Click "Generate PDF" button
       - The app creates one question per page
       - Screenshots are embedded below questions
    
    6. **Download**
       - Click "Download PDF" to save your file
    
    ### Features:
    - ✅ One question per page (professional layout)
    - ✅ Screenshots embedded in correct order
    - ✅ Page numbers (optional)
    - ✅ Customizable font size
    - ✅ Auto-scaling screenshots
    - ✅ Support for A4 and Letter sizes
    """)

st.markdown("---")
st.markdown("**Requirements (Install before running):**")
st.code("pip install streamlit python-docx reportlab pillow", language="bash")
st.markdown("**Run the app:**")
st.code("streamlit run question_pdf_generator.py", language="bash")

