import streamlit as st
import platform
import os

# Import auxiliary modules
import utils.image_processing as img_proc
import utils.ocr_functions as ocr
import utils.file_handling as file_handler
import utils.ui_components as ui

# Page settings - MUST BE THE FIRST STREAMLIT COMMAND!
st.set_page_config(
    page_title="PDF and Image OCR Application",
    page_icon="📄",
    layout="wide"
)

# Configure roads
if platform.system() == "Windows":
    # Set Tesseract OCR path for Windows
    tesseract_path = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    # Set Poppler path for Windows
    poppler_path = r'C:/Program Files/poppler-24.08.0/bin'
    
    # Send paths to the configuration module
    poppler_found = ocr.configure_paths(tesseract_path, poppler_path)
else:
    # For Linux/Mac
    poppler_found = True

# Application title and description
ui.render_header()

# Show Poppler status
if platform.system() == "Windows":
    ui.show_poppler_status(poppler_found, poppler_path)

# file type selection
file_type = st.radio(
    "Select the file type you want to process:",
    ["PDF", "Image (JPG, PNG)"]
)

# File upload
uploaded_file = ui.render_file_uploader(file_type)

# OCR settings
ocr_lang, preprocessing_options = ui.render_sidebar_options()

# Main application logic
if uploaded_file is not None:
    # Show file information
    ui.display_file_info(uploaded_file)
    
    # Start OCR process button
    if st.button("Start OCR Process"):
        with st.spinner("Processing file and extracting text..."):
            try:
                # Process by file type
                if file_type == "PDF":
                    text = ocr.process_pdf(uploaded_file, ocr_lang, preprocessing_options)
                else:
                    text = ocr.process_image(uploaded_file, ocr_lang, preprocessing_options)
                
                # Create a tab
                tab1, tab2, tab3 = st.tabs(['Text Output', 'Visual Analysis', 'Download Options'])
                
                # Text output tab
                with tab1:
                    text = ui.render_text_output_tab(text)
                
                # Visual analysis tab
                with tab2:
                    ui.render_visual_analysis_tab(
                        file_type, 
                        uploaded_file, 
                        preprocessing_options
                    )
                
                # Download options tab
                with tab3:
                    ui.render_download_options_tab(text, uploaded_file.name)
                    
            except Exception as e:
                st.error(f"An error occurred during the OCR process: {str(e)}")
else:
    st.info("Please upload a file for OCR processing.")

# Footer
st.markdown("---")
st.markdown("PDF OCR App - Easily convert documents to text") 

# Buy Me a Coffee button at the bottom of the page
st.markdown("---") 
st.markdown("""
    <div style='display: flex; justify-content: center;'>
        <div style='text-align: center; padding: 15px; background-color: #f0f2f6; border-radius: 10px; margin: 20px 0; width: 33%;'>
            <h3 style='color: #1f77b4;'>If you like the app, you can buy me a coffee! ☕</h3>
            <a href="https://buymeacoffee.com/ugurdemirkb" target="_blank">
                <img src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg" alt="Buy me a coffee" style="height: 60px !important;width: 217px !important; margin: 10px 0;">
            </a>
            <p style='color: #666; font-size: 14px;'>Thank you for your support!</p>
        </div>
    </div>
""", unsafe_allow_html=True) 