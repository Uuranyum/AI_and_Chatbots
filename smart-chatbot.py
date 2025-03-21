import streamlit as st
import google.generativeai as genai
import os
import io
import pandas as pd
from PyPDF2 import PdfReader
import docx

# Page configuration
st.set_page_config(page_title="Smart Document Analysis Chatbot", page_icon="🤖", layout="wide")

# Set API key
GEMINI_API_KEY = 'your api key'
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-pro')


# Function to extract data from different file types
def extract_data_from_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()

    try:
        if file_type == 'txt':
            # Text files
            return {"type": "text", "content": uploaded_file.read().decode('utf-8')}

        elif file_type == 'pdf':
            # PDF files
            text = ""
            pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return {"type": "text", "content": text}

        elif file_type in ['docx', 'doc']:
            # Word documents
            text = ""
            doc = docx.Document(io.BytesIO(uploaded_file.read()))
            for para in doc.paragraphs:
                text += para.text + "\n"
            return {"type": "text", "content": text}

        elif file_type == 'csv':
            # CSV files
            df = pd.read_csv(uploaded_file)
            return {
                "type": "tabular",
                "content": df.to_string(index=False),
                "dataframe": df,
                "description": f"CSV file uploaded. Contains {len(df)} rows and {len(df.columns)} columns.\n\nColumns: {', '.join(df.columns.tolist())}"
            }

        elif file_type in ['xlsx', 'xls']:
            # Excel files
            df = pd.read_excel(uploaded_file)
            return {
                "type": "tabular",
                "content": df.to_string(index=False),
                "dataframe": df,
                "description": f"Excel file uploaded. Contains {len(df)} rows and {len(df.columns)} columns.\n\nColumns: {', '.join(df.columns.tolist())}"
            }

        return {"type": "unknown", "content": "This file type is not supported."}

    except Exception as e:
        st.error(f"File processing error: {str(e)}")
        return {"type": "error", "content": f"Error: {str(e)}"}


# Initialize session states
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'document_data' not in st.session_state:
    st.session_state.document_data = {"type": "", "content": "", "dataframe": None, "description": ""}

if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False

# Display title
st.title("Smart Document Analysis Chatbot")
st.markdown("This chatbot is designed to answer your questions about uploaded documents or tables.")

# File uploader in sidebar
with st.sidebar:
    st.header("Upload File")
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx", "doc", "csv", "xlsx", "xls"])

    if uploaded_file is not None:
        # Extract data from uploaded file
        file_data = extract_data_from_file(uploaded_file)

        if file_data["type"] != "error":
            st.session_state.document_data = file_data
            st.session_state.file_uploaded = True
            st.success(f"'{uploaded_file.name}' successfully uploaded!")

            # Show different previews based on file type
            if file_data["type"] == "tabular":
                st.subheader("File Information")
                st.write(file_data["description"])
                with st.expander("Data Preview"):
                    st.dataframe(file_data["dataframe"].head(10))
            else:
                # Show document preview
                with st.expander("Document Preview"):
                    st.text_area("Document Content", file_data["content"][:5000] +
                                 ("..." if len(file_data["content"]) > 5000 else ""), height=300, disabled=True)

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

# Display data in main section (for tabular data)
if st.session_state.file_uploaded and st.session_state.document_data["type"] == "tabular":
    df = st.session_state.document_data["dataframe"]

    # Show basic statistics
    st.subheader("Data Summary")

    # Show first 5 rows
    st.write("First 5 rows:")
    st.dataframe(df.head())

    # Column types
    st.write("Column data types:")
    st.dataframe(pd.DataFrame(df.dtypes, columns=["Data Type"]))

    # Summary statistics for numerical columns
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if numeric_columns:
        st.write("Summary statistics for numerical columns:")
        st.dataframe(df[numeric_columns].describe())

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get user input
prompt = st.chat_input("Type your question here...", disabled=not st.session_state.file_uploaded)

# Show warning if no file is uploaded
if not st.session_state.file_uploaded:
    st.warning("Please upload a file from the left sidebar first (TXT, PDF, DOCX, CSV, or Excel).")

# Process user input
if prompt and st.session_state.file_uploaded:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Create prompt based on file type
            document_data = st.session_state.document_data

            if document_data["type"] == "tabular":
                # Special prompt for tabular data
                full_prompt = f"""
                You are an expert assistant in data analysis.
                You need to analyze the following table data and answer the user's questions.

                Table Description:
                {document_data["description"]}

                Table Data:
                {document_data["content"]}

                User Question: {prompt}

                Please provide a data-driven, clear, and understandable response. If the question cannot be answered 
                with the available data, indicate this and suggest what the user might ask instead.
                """
            else:
                # Prompt for text documents
                full_prompt = f"""
                You are an expert assistant on the uploaded document.
                The text below contains information related to the uploaded document.
                Based on this information, answer the user's questions.
                If you don't know the answer to a question, honestly say you don't know.

                Document Content:
                {document_data["content"]}

                User Question: {prompt}
                """

            # Get response from Gemini
            response = model.generate_content(full_prompt)
            response_text = response.text

            # Display response
            st.write(response_text)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# Additional information in sidebar
with st.sidebar:
    st.header("About the Application")
    st.info("""
    This chatbot answers your questions about uploaded documents and tables.

    Supported file formats:
    - TXT (text files)
    - PDF files
    - DOCX/DOC (Word documents)
    - CSV (comma-separated values)
    - XLSX/XLS (Excel files)

    Usage:
    1. Upload a file from the left sidebar
    2. Ask your question after the file is successfully uploaded
    3. The AI will respond based on the information in your file

    Example questions (for CSV/Excel):
    - "What's the highest value in this data?"
    - "How many different categories are there in the data?"
    - "Summarize the data"
    - "Which columns have missing data?"
    """)