import streamlit as st
import PyPDF2
import docx
import nltk
import io
from local_summarizer import MetinOzetleyici

# Page configuration
st.set_page_config(
    page_title="Yerel Metin Özetleyici",
    page_icon="📝",
    layout="wide"
)

# Customize interface with CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #60A5FA;
    text-align: center;
    margin-bottom: 1rem;
}
.sub-header {
    font-size: 1.2rem;
    color: #E5E7EB;
    text-align: center;
    margin-bottom: 2rem;
}
.stTextInput > div > div > input {
    font-size: 1.1rem;
    padding: 0.7rem;
}
.answer-container {
    background-color: #1F2937;
    padding: 1.5rem;
    border-radius: 0.5rem;
    border-left: 5px solid #60A5FA;
    margin: 1rem 0;
    color: #E5E7EB;
}
.source-text {
    background-color: #374151;
    padding: 1rem;
    border-radius: 0.3rem;
    font-size: 0.9rem;
    border: 1px solid #4B5563;
    margin-bottom: 0.7rem;
    color: #E5E7EB;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📝 Yerel Metin Özetleyici</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">PDF, TXT veya DOCX dosyalarınızı yükleyin ve yapay zeka kullanmadan özetleyin!</p>', unsafe_allow_html=True)

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

# Initialize summarizer
summarizer = MetinOzetleyici()

# File upload
uploaded_file = st.file_uploader("Dosyanızı buraya yükleyin", type=['pdf', 'txt', 'docx'])

# Summary length selection
summary_length = st.slider(
    "Özet uzunluğu (orijinal metnin yüzdesi olarak)",
    min_value=10,
    max_value=90,
    value=30,
    step=10
) / 100

if uploaded_file is not None:
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
            st.error("Unsupported file format!")
            text = None
        
        if text:
            # Show original text
            with st.expander("Orijinal Metin"):
                st.text(text)
            
            # Summarize button
            if st.button("Özetle"):
                with st.spinner("Özet oluşturuluyor..."):
                    # Summarize text
                    summary = summarizer.ozetle(text, summary_length)
                    
                    # Show statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Orijinal Kelime Sayısı", len(text.split()))
                    with col2:
                        st.metric("Özet Kelime Sayısı", len(summary.split()))
                    with col3:
                        st.metric("Sıkıştırma Oranı", f"%{int((1 - len(summary.split()) / len(text.split())) * 100)}")
                    
                    # Show summary
                    st.subheader("Özet")
                    st.markdown(f'<div class="answer-container">{summary}</div>', unsafe_allow_html=True)
                    
                    # Download summary button
                    st.download_button(
                        label="Özeti İndir",
                        data=summary,
                        file_name="ozet.txt",
                        mime="text/plain"
                    )
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Ugur Demirkaya")

# Info box
with st.expander("ℹ️ Bu uygulama nasıl çalışır?"):
    st.write("""
    Bu uygulama metin özetlemeyi tamamen yerel olarak, herhangi bir API kullanmadan gerçekleştirir. İşte nasıl çalışır:
    
    1. **Metin Analizi**: Yüklenen metin cümlelere ve kelimelere ayrılır.
    2. **Benzerlik Hesaplama**: Her cümle arasındaki kosinüs benzerliği hesaplanır.
    3. **PageRank Algoritması**: Cümle önemi PageRank algoritması kullanılarak belirlenir.
    4. **Özet Oluşturma**: En önemli cümleler seçilerek özet oluşturulur.
    
    Bu yöntem yapay zeka API'lerinden daha hızlı çalışır ve internet bağlantısı gerektirmez.
    """)

# Warning
st.warning("⚠️ Bu uygulama özetleme için yapay zeka kullanmaz. Bu nedenle, özetler daha basit ve mekanik olabilir.") 

# Buy Me a Coffee Butonu
st.markdown("---")
st.markdown("""
    <div style='display: flex; justify-content: center;'>
        <div style='text-align: center; padding: 15px; background-color: #f0f2f6; border-radius: 10px; margin: 20px 0; width: 33%;'>
            <h3 style='color: #1f77b4;'>Uygulamayı beğendiyseniz, bana bir kahve ısmarlayabilirsiniz! ☕</h3>
            <a href="https://buymeacoffee.com/ugurdemirkb" target="_blank">
                <img src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg" alt="Buy me a coffee" style="height: 60px !important;width: 217px !important; margin: 10px 0;">
            </a>
            <p style='color: #666; font-size: 14px;'>Desteğiniz için teşekkürler!</p>
        </div>
    </div>
""", unsafe_allow_html=True) 