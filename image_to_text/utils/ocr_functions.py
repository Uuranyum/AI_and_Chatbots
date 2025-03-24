import pytesseract
import pdf2image
import platform
import os
import tempfile
from PIL import Image
import streamlit as st

from utils.image_processing import preprocess_image

def configure_paths(tesseract_path, poppler_path):
    """
    Configures Tesseract and Poppler paths
    
    Args:
        tesseract_path: Path to the tesseract exe file
        poppler_path: Path to the poppler bin folder
    
    Returns:
        bool Whether the Poppler path exists
    """
    # Adjust tesseract path
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    # Check and adjust poppler path
    if os.path.exists(poppler_path):
        os.environ["PATH"] += os.pathsep + poppler_path
        return True
    else:
        return False

def process_pdf(pdf_file, ocr_lang, preprocessing_options):
    """
    Extracts text from PDF file with OCR
    
    Args:
        pdf_file: Uploaded PDF file
        ocr_lang: OCR language
        preprocessing_options: Preprocessing options
    
    Returns:
        str: Extracted text
    """
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_file.getvalue())
        temp_pdf_path = temp_pdf.name
    
    try:
        # Convert PDF to images
        with st.spinner("PDF sayfaları görüntülere dönüştürülüyor..."):
            # Use if Poppler path is specified in Windows
            try:
                if platform.system() == "Windows":
                    poppler_path = r'C:\\Program Files\\poppler-24.08.0\\Library\bin'
                    if os.path.exists(poppler_path):
                        images = pdf2image.convert_from_path(temp_pdf_path, poppler_path=poppler_path)
                    else:
                        raise Exception("Poppler path not found")
                else:
                    images = pdf2image.convert_from_path(temp_pdf_path)
                
                st.success(f"Total {len(images)} pages found.")
            except Exception as e:
                st.error(f"Error converting PDF to image: {str(e)}")
                # Try the alternative method
                try:
                    st.warning("The alternative method is being tried....")
                    
                    # Convert using bytes directly via Poppler
                    if platform.system() == "Windows":
                        poppler_path = r'C:\\Program Files\\poppler-24.08.0\\Library\bin'
                        if os.path.exists(poppler_path):
                            images = pdf2image.convert_from_bytes(
                                pdf_file.getvalue(),
                                poppler_path=poppler_path
                            )
                        else:
                            raise Exception("Poppler path not found")
                    else:
                        images = pdf2image.convert_from_bytes(pdf_file.getvalue())
                    
                    st.success(f"Found page {len(images)} with alternative method.")
                except Exception as e2:
                    st.error(f"The alternative method also failed: {str(e2)}")
                    raise Exception(f"Unable to process PDF: {str(e)} / {str(e2)}")
        
        # Transaction information display
        progress_info = st.empty()
        
        # Extract text from all pages
        text = ""
        progress_bar = st.progress(0)
        for i, img in enumerate(images):
            # Update transaction status
            progress_info.info(f"Processing page {i+1}/{len(images)}...")
            
            # Apply image preprocessing
            processed_img = preprocess_image(img, preprocessing_options)
            
            # OCR process
            page_text = pytesseract.image_to_string(processed_img, lang=ocr_lang)
            text += f"Sayfa {i+1}\n{page_text}\n\n"
            
            # Update progress status
            progress_bar.progress((i + 1) / len(images))
        
        progress_info.success("OCR is complete!")
        return text
    finally:
        # Clear temporary file
        if os.path.exists(temp_pdf_path):
            os.unlink(temp_pdf_path)

def process_image(image_file, ocr_lang, preprocessing_options):
    """
    Extracts text from image file with OCR
    
    Args:
        image_file: Uploaded image file
        ocr_lang: OCR language
        preprocessing_options: Preprocessing options
    
    Returns:
        str: Extracted text
    """
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{image_file.name.split('.')[-1]}") as temp_img:
            temp_img.write(image_file.getvalue())
            temp_img_path = temp_img.name
        
        try:
            # Reading the image
            with st.spinner("Image processing..."):
                image = Image.open(temp_img_path)
                st.success("Image uploaded successfully.")
                
                # View image
                st.image(image, caption="Uploaded Image", width=400)
                
                # Apply image preprocessing
                processed_img = preprocess_image(image, preprocessing_options)
                
                # OCR process
                with st.spinner("OCR processing is in progress..."):
                    text = pytesseract.image_to_string(processed_img, lang=ocr_lang)
                    st.success("OCR is complete!")
                
                return text
        finally:
            # Clear temporary filee
            if os.path.exists(temp_img_path):
                os.unlink(temp_img_path)
    except Exception as e:
        st.error(f"An error occurred during image processing: {str(e)}")
        return "" 