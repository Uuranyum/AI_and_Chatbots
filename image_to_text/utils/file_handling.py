import io
from docx import Document
from fpdf import FPDF

def save_as_txt(text):
    """
    Metni TXT dosyası olarak kaydeder
    
    Args:
        text: Kaydedilecek metin
    
    Returns:
        bytes: TXT dosyası içeriği
    """
    return text.encode()

def save_as_docx(text):
    """
    Metni DOCX dosyası olarak kaydeder
    
    Args:
        text: Kaydedilecek metin
    
    Returns:
        bytes: DOCX dosyası içeriği
    """
    doc = Document()
    doc.add_paragraph(text)
    
    # docx dosyasını byte array'e dönüştürme
    with io.BytesIO() as output:
        doc.save(output)
        output.seek(0)
        return output.read()

def save_as_pdf(text):
    """
    Metni PDF dosyası olarak kaydeder
    
    Args:
        text: Kaydedilecek metin
    
    Returns:
        bytes: PDF dosyası içeriği
    """
    # PDF oluşturma
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Metni PDF'e yazma (Türkçe karakterler için utf-8)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Metni satırlara bölelim
    lines = text.split('\n')
    for line in lines:
        # Türkçe karakterleri desteklemek için encode/decode
        pdf.cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'), ln=True)
    
    # PDF'i byte array'e dönüştürme
    with io.BytesIO() as output:
        pdf.output(output)
        return output.getvalue() 