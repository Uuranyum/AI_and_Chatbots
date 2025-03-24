import streamlit as st
import os
import tempfile
from PIL import Image
import platform

from utils.file_handling import save_as_txt, save_as_docx, save_as_pdf
from utils.image_processing import preprocess_image
import pdf2image

def render_header():
    """Ana başlık ve açıklamayı oluşturur"""
    st.title("PDF ve Görüntü OCR Metne Dönüştürme Uygulaması")
    st.markdown("PDF veya görüntü dosyalarını yükleyerek metne dönüştürebilir ve farklı formatlarda indirebilirsiniz.")

def show_poppler_status(poppler_found, poppler_path):
    """Poppler durumunu gösterir"""
    with st.sidebar:
        if poppler_found:
            st.success("Poppler yolu bulundu!")
        else:
            st.error(f"Poppler yolu bulunamadı: {poppler_path}")
            st.info("Lütfen Poppler'ı yükleyin ve doğru yolu ayarlayın.")

def render_file_uploader(file_type):
    """Dosya yükleme alanını oluşturur"""
    if file_type == "PDF":
        return st.file_uploader("PDF dosyası yükleyin", type=["pdf"])
    else:
        return st.file_uploader("Görüntü dosyası yükleyin", type=["jpg", "jpeg", "png", "tiff"])

def render_sidebar_options():
    """Yan panel seçeneklerini oluşturur"""
    with st.sidebar:
        st.header("OCR Ayarları")
        
        # Dil seçimi
        ocr_lang = st.selectbox(
            "OCR Dili",
            options=["tur+eng", "tur", "eng"],
            format_func=lambda x: {
                "tur+eng": "Türkçe + İngilizce",
                "tur": "Sadece Türkçe",
                "eng": "Sadece İngilizce"
            }[x],
            index=0
        )
        
        # Görüntü önişleme seçenekleri
        st.subheader("Görüntü Önişleme")
        apply_threshold = st.checkbox("Eşikleme Uygula", value=False, 
                                     help="Metin ayırt etmeyi kolaylaştırmak için siyah-beyaz eşikleme uygulayın")
        threshold_value = st.slider("Eşik Değeri", 0, 255, 128) if apply_threshold else 128
        
        apply_resize = st.checkbox("Yeniden Boyutlandır", value=False,
                                  help="Görüntüyü yeniden boyutlandırarak OCR doğruluğunu artırabilir")
        scale_factor = st.slider("Boyut Çarpanı", 1.0, 3.0, 1.5, 0.1) if apply_resize else 1.0
        
        # Seçenekleri bir sözlükte topla
        preprocessing_options = {
            'apply_threshold': apply_threshold,
            'threshold_value': threshold_value,
            'apply_resize': apply_resize,
            'scale_factor': scale_factor
        }
        
        return ocr_lang, preprocessing_options

def display_file_info(uploaded_file):
    """Dosya bilgilerini gösterir"""
    file_details = {
        "Dosya Adı": uploaded_file.name,
        "Dosya Boyutu": f"{uploaded_file.size / 1024:.2f} KB"
    }
    
    st.write("**Yüklenen Dosya Bilgileri:**")
    for k, v in file_details.items():
        st.write(f"- {k}: {v}")

def render_text_output_tab(text):
    """Metin çıktısı sekmesini oluşturur"""
    st.subheader("Çıkarılan Metin:")
    edited_text = st.text_area("Metni inceleyebilir ve düzenleyebilirsiniz", text, height=400)
    
    # Metin değiştiğinde güncelleme
    if edited_text != text:
        text = edited_text
        st.success("Metin başarıyla düzenlendi!")
    
    # Metin istatistikleri
    st.subheader("Metin İstatistikleri")
    col1, col2, col3 = st.columns(3)
    
    lines = text.split('\n')
    words = text.split()
    chars = len(text)
    
    col1.metric("Satır Sayısı", len(lines))
    col2.metric("Kelime Sayısı", len(words))
    col3.metric("Karakter Sayısı", chars)
    
    return text

def render_visual_analysis_tab(file_type, uploaded_file, preprocessing_options):
    """Görsel analiz sekmesini oluşturur"""
    st.subheader("İşlenmiş Görüntü Örnekleri")
    
    if file_type == "PDF":
        st.write("Görüntü önişleme sonuçlarını görmek için sayfa seçin:")
        
        # PDF'i tekrar görüntülere dönüştür (sadece ilk 5 sayfa)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_file.getvalue())
            temp_pdf_path = temp_pdf.name
        
        try:
            if platform.system() == "Windows":
                poppler_path = r'C:\Program Files\poppler-24.08.0\Library\bin'
                try:
                    if os.path.exists(poppler_path):
                        all_images = pdf2image.convert_from_path(temp_pdf_path, poppler_path=poppler_path)
                    else:
                        raise Exception("Poppler yolu bulunamadı")
                except Exception as e:
                    st.error(f"PDF görüntüye dönüştürülürken hata: {str(e)}")
                    st.warning("Alternatif metot deneniyor...")
                    if os.path.exists(poppler_path):
                        all_images = pdf2image.convert_from_bytes(
                            uploaded_file.getvalue(),
                            poppler_path=poppler_path
                        )
                    else:
                        raise Exception("Poppler yolu bulunamadı")
            else:
                try:
                    all_images = pdf2image.convert_from_path(temp_pdf_path)
                except Exception as e:
                    st.error(f"PDF görüntüye dönüştürülürken hata: {str(e)}")
                    st.warning("Alternatif metot deneniyor...")
                    all_images = pdf2image.convert_from_bytes(uploaded_file.getvalue())
                
            # En fazla 5 sayfa göster
            images = all_images[:5]
            
            if os.path.exists(temp_pdf_path):
                os.unlink(temp_pdf_path)
            
            selected_page = st.selectbox("Sayfa Seçin", range(1, len(images) + 1))
            
            # Orijinal ve işlenmiş görüntüleri göster
            orig_col, proc_col = st.columns(2)
            
            with orig_col:
                st.write("Orijinal Görüntü")
                selected_img = images[selected_page - 1]
                st.image(selected_img, use_column_width=True)
            
            with proc_col:
                st.write("İşlenmiş Görüntü")
                processed_img = preprocess_image(images[selected_page - 1], preprocessing_options)
                st.image(processed_img, use_column_width=True)
                
        except Exception as e:
            st.error(f"Görüntüleri işlerken hata oluştu: {str(e)}")
            if os.path.exists(temp_pdf_path):
                os.unlink(temp_pdf_path)
    else:
        # Görüntü dosyası için işlem
        st.write("Görüntü önişleme sonuçları:")
        
        try:
            # Görüntüyü geçici dosyaya yazıp tekrar yükle
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as temp_img:
                temp_img.write(uploaded_file.getvalue())
                temp_img_path = temp_img.name
            
            try:
                # Görüntüyü yükle
                image = Image.open(temp_img_path)
                
                # Orijinal ve işlenmiş görüntüleri göster
                orig_col, proc_col = st.columns(2)
                
                with orig_col:
                    st.write("Orijinal Görüntü")
                    st.image(image, use_column_width=True)
                
                with proc_col:
                    st.write("İşlenmiş Görüntü")
                    processed_img = preprocess_image(image, preprocessing_options)
                    st.image(processed_img, use_column_width=True)
            finally:
                # Geçici dosyayı temizle
                if os.path.exists(temp_img_path):
                    os.unlink(temp_img_path)
                
        except Exception as e:
            st.error(f"Görüntüyü işlerken hata oluştu: {str(e)}")

def render_download_options_tab(text, filename):
    """İndirme seçenekleri sekmesini oluşturur"""
    st.subheader("İndirme Seçenekleri")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        txt_data = save_as_txt(text)
        st.download_button(
            label="TXT olarak indir",
            data=txt_data,
            file_name=f"{filename.split('.')[0]}.txt",
            mime="text/plain"
        )
    
    with col2:
        docx_data = save_as_docx(text)
        st.download_button(
            label="DOCX olarak indir",
            data=docx_data,
            file_name=f"{filename.split('.')[0]}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    
    with col3:
        pdf_data = save_as_pdf(text)
        st.download_button(
            label="PDF olarak indir",
            data=pdf_data,
            file_name=f"{filename.split('.')[0]}_metin.pdf",
            mime="application/pdf"
        ) 