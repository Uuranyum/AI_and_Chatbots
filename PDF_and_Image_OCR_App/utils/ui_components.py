import streamlit as st
import os
import tempfile
from PIL import Image
import platform

from utils.file_handling import save_as_txt, save_as_docx, save_as_pdf
from utils.image_processing import preprocess_image
import pdf2image

def render_header():
    """Creates the main title and description"""
    st.title("PDF and Image OCR Transcription App")
    st.markdown("You can upload PDF or image files, convert them to text and download them in different formats.")

def show_poppler_status(poppler_found, poppler_path):
    """Shows Poppler status"""
    with st.sidebar:
        if poppler_found:
            st.success("The Poppler path has been found!")
        else:
            st.error(f"Poppler path not found: {poppler_path}")
            st.info("Please install Poppler and set the correct path.")

def render_file_uploader(file_type):
    """Creates the file upload area"""
    if file_type == "PDF":
        return st.file_uploader("Upload PDF file", type=["pdf"])
    else:
        return st.file_uploader("Upload image file", type=["jpg", "jpeg", "png", "tiff"])

def render_sidebar_options():
    """Generates side panel options"""
    with st.sidebar:
        st.header("OCR Settings")
        
        # Dil seçimi
        ocr_lang = st.selectbox(
            "OCR Languages",
            options=["tur+eng", "tur", "eng"],
            format_func=lambda x: {
                "tur+eng": "Turkish + English",
                "tur": "Turkish only",
                "eng": "English only"
            }[x],
            index=0
        )
        
        # Image preprocessing options
        st.subheader("Image Preprocessing")
        apply_threshold = st.checkbox("Apply Thresholding", value=False, 
                                     help="Apply black-and-white thresholding to make text easier to distinguish")
        threshold_value = st.slider("Threshold Value", 0, 255, 128) if apply_threshold else 128
        
        apply_resize = st.checkbox("Resize", value=False,
                                  help="Can improve OCR accuracy by resizing the image")
        scale_factor = st.slider("Dimension Multiplier", 1.0, 3.0, 1.5, 0.1) if apply_resize else 1.0
        
        # Collect options in a dictionary
        preprocessing_options = {
            'apply_threshold': apply_threshold,
            'threshold_value': threshold_value,
            'apply_resize': apply_resize,
            'scale_factor': scale_factor
        }
        
        return ocr_lang, preprocessing_options

def display_file_info(uploaded_file):
    """Shows file information"""
    file_details = {
        "File Name": uploaded_file.name,
        "Dosya File Size": f"{uploaded_file.size / 1024:.2f} KB"
    }
    
    st.write("**Uploaded File Information:**")
    for k, v in file_details.items():
        st.write(f"- {k}: {v}")

def render_text_output_tab(text):
    """Creates the text output tab"""
    st.subheader("Extracted Text:")
    edited_text = st.text_area("You can review and edit the text", text, height=400)
    
    # Metin değiştiğinde Update when text changes
    if edited_text != text:
        text = edited_text
        st.success("The text was successfully edited!")
    
    # Metin istatistikleri
    st.subheader("Text Statistics")
    col1, col2, col3 = st.columns(3)
    
    lines = text.split('\n')
    words = text.split()
    chars = len(text)
    
    col1.metric("Number of Row", len(lines))
    col2.metric("Word Count", len(words))
    col3.metric("Number of Characters", chars)
    
    return text

def render_visual_analysis_tab(file_type, uploaded_file, preprocessing_options):
    """Creates the visual analysis tab"""
    st.subheader("Processed Image Examples")
    
    if file_type == "PDF":
        st.write("Select page to see image preprocessing results:")
        
        # Convert PDF back to images (first 5 pages only)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_file.getvalue())
            temp_pdf_path = temp_pdf.name
        
        try:
            if platform.system() == "Windows":
                poppler_path = r'C:\\Program Files\\poppler-24.08.0\\Library\bin'
                try:
                    if os.path.exists(poppler_path):
                        all_images = pdf2image.convert_from_path(temp_pdf_path, poppler_path=poppler_path)
                    else:
                        raise Exception("Poppler path not found")
                except Exception as e:
                    st.error(f"Error converting PDF to image: {str(e)}")
                    st.warning("Alternative methods are being tested...")
                    if os.path.exists(poppler_path):
                        all_images = pdf2image.convert_from_bytes(
                            uploaded_file.getvalue(),
                            poppler_path=poppler_path
                        )
                    else:
                        raise Exception("Poppler path not found")
            else:
                try:
                    all_images = pdf2image.convert_from_path(temp_pdf_path)
                except Exception as e:
                    st.error(f"Error converting PDF to image: {str(e)}")
                    st.warning("Alternative methods are being tested...")
                    all_images = pdf2image.convert_from_bytes(uploaded_file.getvalue())
                
            # Show up to 5 pages
            images = all_images[:5]
            
            if os.path.exists(temp_pdf_path):
                os.unlink(temp_pdf_path)
            
            selected_page = st.selectbox("Select Page", range(1, len(images) + 1))
            
            # Show original and processed images
            orig_col, proc_col = st.columns(2)
            
            with orig_col:
                st.write("Original Image")
                selected_img = images[selected_page - 1]
                st.image(selected_img, use_column_width=True)
            
            with proc_col:
                st.write("Processed Image")
                processed_img = preprocess_image(images[selected_page - 1], preprocessing_options)
                st.image(processed_img, use_column_width=True)
                
        except Exception as e:
            st.error(f"Error processing images: {str(e)}")
            if os.path.exists(temp_pdf_path):
                os.unlink(temp_pdf_path)
    else:
        # Operation for image file
        st.write("Image preprocessing results:")
        
        try:
            # Write the image to a temporary file and upload it again
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as temp_img:
                temp_img.write(uploaded_file.getvalue())
                temp_img_path = temp_img.name
            
            try:
                # Upload image
                image = Image.open(temp_img_path)
                
                # Show original and processed images
                orig_col, proc_col = st.columns(2)
                
                with orig_col:
                    st.write("Original Image")
                    st.image(image, use_column_width=True)
                
                with proc_col:
                    st.write("Processed Image")
                    processed_img = preprocess_image(image, preprocessing_options)
                    st.image(processed_img, use_column_width=True)
            finally:
                # Clear temporary file
                if os.path.exists(temp_img_path):
                    os.unlink(temp_img_path)
                
        except Exception as e:
            st.error(f"Error processing the image: {str(e)}")

def render_download_options_tab(text, filename):
    """İndirme seçenekleri Creates the download options tab oluşturur"""
    st.subheader("Download Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        txt_data = save_as_txt(text)
        st.download_button(
            label="Download as TXT",
            data=txt_data,
            file_name=f"{filename.split('.')[0]}.txt",
            mime="text/plain"
        )
    
    with col2:
        docx_data = save_as_docx(text)
        st.download_button(
            label="Download as DOCX",
            data=docx_data,
            file_name=f"{filename.split('.')[0]}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    
    with col3:
        pdf_data = save_as_pdf(text)
        st.download_button(
            label="Download as PDF",
            data=pdf_data,
            file_name=f"{filename.split('.')[0]}_metin.pdf",
            mime="application/pdf"
        ) 