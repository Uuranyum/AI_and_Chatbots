import streamlit as st
import PyPDF2
import docx
import google.generativeai as genai
import nltk
import io
import os
from dotenv import load_dotenv

# Download required NLTK data
nltk.download('punkt')

# Page configuration
st.set_page_config(
    page_title="Text Summarizer",
    page_icon="📄",
    layout="centered"
)

# Get Gemini API key
api_key = st.text_input("Enter your Gemini API Key:", type="password")

# Title
st.title("📑🧠 Text Summarizer")
st.markdown("Upload your PDF,TXT, DOCX, or DOC files and generate automatic summaries using Gemini AI!!!")

# File upload
uploaded_file = st.file_uploader("Upload your file here", type=['pdf', 'txt', 'docx', 'doc'])

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_txt(file):
    return file.getvalue().decode("utf-8")

def summarize_text_with_gemini(text, api_key):
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Select model
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Summarization prompt
        prompt = f"""
        Please summarize the following text. Keep the important points and main ideas,
        but present them in a more concise way. The summary should be in English:

        {text}
        """
        
        # Generate summary
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during summarization: {str(e)}"

if uploaded_file is not None and api_key:
    try:
        # Get file extension
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        # Extract text based on file type
        if file_extension == 'pdf':
            text = extract_text_from_pdf(uploaded_file)
        elif file_extension == 'docx':
            text = extract_text_from_docx(uploaded_file)
        elif file_extension == 'txt':
            text = extract_text_from_txt(uploaded_file)
        else:
            st.error("Invalid file format. Please upload a PDF, DOCX, DOC, or TXT file.")
            text = None
        
        if text:
            # Show original text
            with st.expander("Original Text"):
                st.text(text)
            
            # Summarization button
            if st.button("Summarize"):
                with st.spinner("Generating summary..."):
                    summary = summarize_text_with_gemini(text, api_key)
                    
                    # Show summary
                    st.subheader("Summary")
                    st.write(summary)
                    
                    # Download summary button
                    st.download_button(
                        label="Download Summary",
                        data=summary,
                        file_name="summary.txt",
                        mime="text/plain"
                    )
    except Exception as e:
        st.error(f"An error occured during file processing: {str(e)}")
elif uploaded_file is not None and not api_key:
    st.warning("Please enter your Gemini API key to continue!")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by [Ugur Demirkaya](https://github.com/Uuranyum)")            

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