import io
from docx import Document
from fpdf import FPDF

def save_as_txt(text):
    """
    Saves text as a TXT file
    
    Args:
        text Text to save
    
    Returns:
        bytes TXT file contents
    """
    return text.encode()

def save_as_docx(text):
    """
    Saves text as a DOCX file
    
    Args:
        text Text to save
    
    Returns:
        bytes DOCX file contents
    """
    doc = Document()
    doc.add_paragraph(text)
    
    # Convert docx file to byte array
    with io.BytesIO() as output:
        doc.save(output)
        output.seek(0)
        return output.read()

def save_as_pdf(text):
    """
    Saves text as PDF file
    
    Args:
        text Text to save
    
    Returns:
        bytes PDF file content
    """
    # PDF creation
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Write text to PDF (utf-8 for Turkish characters)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Divide the text into lines
    lines = text.split('\n')
    for line in lines:
        # Encode/decode to support Turkish characters
        pdf.cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'), ln=True)
    
    # Convert PDF to byte array
    with io.BytesIO() as output:
        pdf.output(output)
        return output.getvalue() 