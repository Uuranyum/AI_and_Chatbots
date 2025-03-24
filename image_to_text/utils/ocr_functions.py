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
    Tesseract ve Poppler yollarını yapılandırır
    
    Args:
        tesseract_path: Tesseract exe dosyasının yolu
        poppler_path: Poppler bin klasörünün yolu
    
    Returns:
        bool: Poppler yolunun bulunup bulunmadığı
    """
    # Tesseract yolunu ayarla
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    # Poppler yolunu kontrol et ve ayarla
    if os.path.exists(poppler_path):
        os.environ["PATH"] += os.pathsep + poppler_path
        return True
    else:
        return False

def process_pdf(pdf_file, ocr_lang, preprocessing_options):
    """
    PDF dosyasından OCR ile metin çıkarır
    
    Args:
        pdf_file: Yüklenen PDF dosyası
        ocr_lang: OCR dili
        preprocessing_options: Ön işleme seçenekleri
    
    Returns:
        str: Çıkarılan metin
    """
    # Geçici dosya oluştur
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_file.getvalue())
        temp_pdf_path = temp_pdf.name
    
    try:
        # PDF'i görüntülere dönüştürme
        with st.spinner("PDF sayfaları görüntülere dönüştürülüyor..."):
            # Windows'ta Poppler yolu belirtilmiş ise kullan
            try:
                if platform.system() == "Windows":
                    poppler_path = r'C:\\Program Files\\poppler-24.08.0\\Library\bin'
                    if os.path.exists(poppler_path):
                        images = pdf2image.convert_from_path(temp_pdf_path, poppler_path=poppler_path)
                    else:
                        raise Exception("Poppler yolu bulunamadı")
                else:
                    images = pdf2image.convert_from_path(temp_pdf_path)
                
                st.success(f"Toplam {len(images)} sayfa bulundu.")
            except Exception as e:
                st.error(f"PDF görüntüye dönüştürülürken hata: {str(e)}")
                # Alternatif metodu dene
                try:
                    st.warning("Alternatif metot deneniyor...")
                    
                    # Poppler yolu ile doğrudan bytes kullanarak dönüştürme
                    if platform.system() == "Windows":
                        poppler_path = r'C:\\Program Files\\poppler-24.08.0\\Library\bin'
                        if os.path.exists(poppler_path):
                            images = pdf2image.convert_from_bytes(
                                pdf_file.getvalue(),
                                poppler_path=poppler_path
                            )
                        else:
                            raise Exception("Poppler yolu bulunamadı")
                    else:
                        images = pdf2image.convert_from_bytes(pdf_file.getvalue())
                    
                    st.success(f"Alternatif metot ile {len(images)} sayfa bulundu.")
                except Exception as e2:
                    st.error(f"Alternatif metot da başarısız oldu: {str(e2)}")
                    raise Exception(f"PDF işlenemiyor: {str(e)} / {str(e2)}")
        
        # İşlem bilgisi gösterimi
        progress_info = st.empty()
        
        # Tüm sayfalardan metni çıkarma
        text = ""
        progress_bar = st.progress(0)
        for i, img in enumerate(images):
            # İşlem durumunu güncelle
            progress_info.info(f"Sayfa {i+1}/{len(images)} işleniyor...")
            
            # Görüntü önişleme uygula
            processed_img = preprocess_image(img, preprocessing_options)
            
            # OCR işlemi
            page_text = pytesseract.image_to_string(processed_img, lang=ocr_lang)
            text += f"Sayfa {i+1}\n{page_text}\n\n"
            
            # İlerleme durumunu güncelleme
            progress_bar.progress((i + 1) / len(images))
        
        progress_info.success("OCR işlemi tamamlandı!")
        return text
    finally:
        # Geçici dosyayı temizleme
        if os.path.exists(temp_pdf_path):
            os.unlink(temp_pdf_path)

def process_image(image_file, ocr_lang, preprocessing_options):
    """
    Görüntü dosyasından OCR ile metin çıkarır
    
    Args:
        image_file: Yüklenen görüntü dosyası
        ocr_lang: OCR dili
        preprocessing_options: Ön işleme seçenekleri
    
    Returns:
        str: Çıkarılan metin
    """
    try:
        # Geçici dosya oluştur
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{image_file.name.split('.')[-1]}") as temp_img:
            temp_img.write(image_file.getvalue())
            temp_img_path = temp_img.name
        
        try:
            # Görüntüyü okuma
            with st.spinner("Görüntü işleniyor..."):
                image = Image.open(temp_img_path)
                st.success("Görüntü başarıyla yüklendi.")
                
                # Görüntüyü görüntüle
                st.image(image, caption="Yüklenen Görüntü", width=400)
                
                # Görüntü önişleme uygula
                processed_img = preprocess_image(image, preprocessing_options)
                
                # OCR işlemi
                with st.spinner("OCR işlemi yapılıyor..."):
                    text = pytesseract.image_to_string(processed_img, lang=ocr_lang)
                    st.success("OCR işlemi tamamlandı!")
                
                return text
        finally:
            # Geçici dosyayı temizleme
            if os.path.exists(temp_img_path):
                os.unlink(temp_img_path)
    except Exception as e:
        st.error(f"Görüntü işleme sırasında bir hata oluştu: {str(e)}")
        return "" 