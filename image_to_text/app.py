import streamlit as st
import platform
import os

# Yardımcı modülleri içe aktar
import utils.image_processing as img_proc
import utils.ocr_functions as ocr
import utils.file_handling as file_handler
import utils.ui_components as ui

# Sayfa ayarları - İLK STREAMLİT KOMUTU OLMALI!
st.set_page_config(
    page_title="PDF ve Görüntü OCR Uygulaması",
    page_icon="📄",
    layout="wide"
)

# Yolları yapılandır
if platform.system() == "Windows":
    # Windows için Tesseract OCR yolunu ayarla
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Windows için Poppler yolunu ayarla
    poppler_path = r'C:\Program Files\poppler-24.08.0\Library\bin'
    
    # Yolları yapılandırma modülüne gönder
    poppler_found = ocr.configure_paths(tesseract_path, poppler_path)
else:
    # Linux/Mac için
    poppler_found = True

# Uygulama başlığı ve açıklama
ui.render_header()

# Poppler durumunu göster
if platform.system() == "Windows":
    ui.show_poppler_status(poppler_found, poppler_path)

# Dosya tipi seçimi
file_type = st.radio(
    "İşlemek istediğiniz dosya türünü seçin:",
    ["PDF", "Görüntü (JPG, PNG)"]
)

# Dosya yükleme
uploaded_file = ui.render_file_uploader(file_type)

# OCR ayarları
ocr_lang, preprocessing_options = ui.render_sidebar_options()

# Ana uygulama mantığı
if uploaded_file is not None:
    # Dosya bilgilerini göster
    ui.display_file_info(uploaded_file)
    
    # OCR işlemini başlat butonu
    if st.button("OCR İşlemini Başlat"):
        with st.spinner("Dosya işleniyor ve metin çıkarılıyor..."):
            try:
                # Dosya tipine göre işlem yap
                if file_type == "PDF":
                    text = ocr.process_pdf(uploaded_file, ocr_lang, preprocessing_options)
                else:
                    text = ocr.process_image(uploaded_file, ocr_lang, preprocessing_options)
                
                # Sekme oluşturma
                tab1, tab2, tab3 = st.tabs(["Metin Çıktısı", "Görsel Analiz", "İndirme Seçenekleri"])
                
                # Metin çıktısı sekmesi
                with tab1:
                    text = ui.render_text_output_tab(text)
                
                # Görsel analiz sekmesi
                with tab2:
                    ui.render_visual_analysis_tab(
                        file_type, 
                        uploaded_file, 
                        preprocessing_options
                    )
                
                # İndirme seçenekleri sekmesi
                with tab3:
                    ui.render_download_options_tab(text, uploaded_file.name)
                    
            except Exception as e:
                st.error(f"OCR işlemi sırasında bir hata oluştu: {str(e)}")
else:
    st.info("Lütfen OCR işlemi yapmak için bir dosya yükleyin.")

# Footer
st.markdown("---")
st.markdown("PDF OCR Uygulaması - Belgeleri kolayca metne dönüştürün") 