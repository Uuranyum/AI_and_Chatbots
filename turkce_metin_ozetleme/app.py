"""
Türkçe Dosya Özetleme Sistemi
============================

Bu uygulama PDF, DOCX ve TXT dosyalarını okuyarak Türkçe özetler oluşturur.
Tamamen offline çalışır ve kullanıcı verilerini güvende tutar.

Geliştirici: 
Versiyon: 1.0
Lisans: MIT
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
import PyPDF2
from docx import Document
import io
import re

# Uygulama yapılandırması
st.set_page_config(
    page_title="Türkçe Dosya Özetleme Sistemi",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

class FileProcessor:
    """Dosya işleme sınıfı - farklı dosya formatlarını destekler"""
    
    @staticmethod
    def extract_text_from_pdf(file):
        """PDF dosyasından metin çıkarır"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"PDF okuma hatası: {str(e)}")
            return None

    @staticmethod
    def extract_text_from_docx(file):
        """DOCX dosyasından metin çıkarır"""
        try:
            doc = Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            st.error(f"DOCX okuma hatası: {str(e)}")
            return None

    @staticmethod
    def extract_text_from_txt(file):
        """TXT dosyasından metin çıkarır - Türkçe karakter desteği ile"""
        try:
            content = file.read()
            # Türkçe karakterler için farklı encoding'leri dene
            encodings = ['utf-8', 'windows-1254', 'latin-1']
            
            for encoding in encodings:
                try:
                    text = content.decode(encoding)
                    return text
                except UnicodeDecodeError:
                    continue
            
            # Hiçbiri çalışmazsa son çare
            return content.decode('utf-8', errors='ignore')
            
        except Exception as e:
            st.error(f"TXT okuma hatası: {str(e)}")
            return None

class TextProcessor:
    """Metin işleme ve özetleme sınıfı"""
    
    @staticmethod
    def clean_text(text):
        """Metni temizler ve düzenler"""
        if not text:
            return ""
        
        # Satır sonlarını normalize et
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Birden fazla boşluğu tek boşlukla değiştir
        text = re.sub(r'\s+', ' ', text)
        
        # Paragraf sonlarını koru
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Sayfa numaralarını kaldır
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        
        return text.strip()

    @staticmethod
    def find_key_sentences(sentences, target_count=4):
        """Anahtar cümleleri bulur - Türkçe dil özelliklerine göre optimize edilmiş"""
        if len(sentences) <= target_count:
            return sentences
        
        # Türkçe anahtar kelimeler
        key_terms = [
            'sonuç', 'önemli', 'ana', 'temel', 'başlıca', 'genel', 'toplam', 'değerlendirme',
            'karar', 'öneri', 'hedef', 'amaç', 'planlama', 'strateji', 'politika', 'uygulama',
            'problem', 'çözüm', 'analiz', 'inceleme', 'araştırma', 'gelişim', 'ilerleme',
            'bulgular', 'veriler', 'istatistik', 'rakamlar', 'oran', 'artış', 'azalış'
        ]
        
        scored_sentences = []
        
        for i, sentence in enumerate(sentences):
            score = 0
            sentence_lower = sentence.lower()
            
            # Uzunluk puanı (optimal cümle uzunluğu)
            length = len(sentence.split())
            if 10 <= length <= 25:
                score += 3
            elif 8 <= length <= 30:
                score += 2
            elif 5 <= length <= 35:
                score += 1
            
            # Anahtar kelime puanı
            for term in key_terms:
                if term in sentence_lower:
                    score += 2
            
            # Pozisyon puanı
            total_sentences = len(sentences)
            if i < total_sentences * 0.2:  # İlk %20
                score += 3
            elif i > total_sentences * 0.8:  # Son %20
                score += 2
            
            # Sayısal veri içeren cümleler
            if re.search(r'\d+', sentence):
                score += 1
            
            scored_sentences.append((sentence, score, i))
        
        # Puana göre sırala ve en iyi cümleleri seç
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        
        # Orijinal sırayı koruyarak döndür
        selected = sorted(scored_sentences[:target_count], key=lambda x: x[2])
        return [s[0] for s in selected]

    @staticmethod
    def create_coherent_summary(sentences, word_count, total_sentences, paragraph_count):
        """Tutarlı ve akıcı özet oluşturur"""
        
        if total_sentences <= 3:
            return f"""
**📄 BELGE ÖZETİ**

**📋 İçerik Özeti:**
{' '.join(sentences)} Bu belge kısa ve öz bir içerik sunmaktadır.

**📊 Değerlendirme:**
Toplam {word_count} kelimelik bu belge, temel konuları kapsamaktadır.

---
**📈 Belge Bilgileri:** {word_count:,} kelime, {total_sentences} cümle
"""
        
        # Anahtar cümleleri seç
        key_sentences = TextProcessor.find_key_sentences(sentences, target_count=6)
        
        # İki paragraf oluştur
        first_para_sentences = key_sentences[:3]
        second_para_sentences = key_sentences[3:]
        
        # Geçiş kelimeleri
        transitions_first = ["", "Ayrıca, ", "Bu kapsamda, "]
        transitions_second = ["", "Buna ek olarak, ", "Sonuç olarak, "]
        
        # Paragrafları oluştur
        first_paragraph = ""
        for i, sentence in enumerate(first_para_sentences):
            transition = transitions_first[i] if i < len(transitions_first) else ""
            first_paragraph += transition + sentence + " "
        
        second_paragraph = ""
        for i, sentence in enumerate(second_para_sentences):
            transition = transitions_second[i] if i < len(transitions_second) else ""
            second_paragraph += transition + sentence + " "
        
        # Belge değerlendirmesi
        if word_count > 1000:
            doc_assessment = "kapsamlı ve detaylı bir analiz"
        elif word_count > 500:
            doc_assessment = "orta düzeyde ayrıntılı bir inceleme"
        else:
            doc_assessment = "özet bir değerlendirme"
        
        return f"""
**📄 BELGE ÖZETİ**

**📋 Ana İçerik ve Konu:**
{first_paragraph.strip()}

**📊 Gelişmeler ve Sonuç:**
{second_paragraph.strip()} Bu belge {doc_assessment} sunmaktadır.

---
**📈 Belge Analizi:** {word_count:,} kelime, {paragraph_count} paragraf, {total_sentences} cümle
"""

    @classmethod
    def summarize_text(cls, text):
        """Ana özetleme fonksiyonu"""
        sentences = [s.strip() for s in text.split('.') if s.strip() and len(s.strip()) > 10]
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        word_count = len(text.split())
        total_sentences = len(sentences)
        
        return cls.create_coherent_summary(sentences, word_count, total_sentences, len(paragraphs))

class StreamlitUI:
    """Streamlit kullanıcı arayüzü sınıfı"""
    
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    
    @staticmethod
    def render_sidebar():
        """Yan panel öğelerini oluşturur"""
        with st.sidebar:
            st.header("ℹ️ Uygulama Bilgileri")
            
            st.write("**Desteklenen Formatlar:**")
            st.write("- 📄 PDF (.pdf)")
            st.write("- 📝 Word (.docx)")
            st.write("- 📃 Metin (.txt)")
            
            st.write(f"**Maksimum Boyut:** {StreamlitUI.MAX_FILE_SIZE // (1024*1024)} MB")
            
            st.success("🔒 Tamamen offline çalışır")
            st.info("📝 Profesyonel özetler oluşturur")
            st.warning("⚡ Hızlı ve güvenilir")
            
            st.markdown("---")
            st.markdown("**Geliştirici Bilgileri:**")
            st.markdown("🔧 Türkçe dil desteği optimize edilmiş")
            st.markdown("🎯 Kurumsal kullanım için uygun")

    @staticmethod
    def render_file_upload():
        """Dosya yükleme bölümünü oluşturur"""
        st.header("📁 Dosya Yükleme")
        
        uploaded_file = st.file_uploader(
            "Özetlemek istediğiniz dosyayı seçin:",
            type=['pdf', 'docx', 'txt'],
            help="PDF, DOCX veya TXT formatında dosya yükleyebilirsiniz.",
            key="file_uploader"
        )
        
        if uploaded_file is not None:
            file_size = len(uploaded_file.getvalue())
            
            # Dosya boyutu kontrolü
            if file_size > StreamlitUI.MAX_FILE_SIZE:
                st.error(f"❌ Dosya boyutu {StreamlitUI.MAX_FILE_SIZE // (1024*1024)} MB'dan büyük olamaz!")
                return None
            
            st.success(f"✅ Dosya yüklendi: {uploaded_file.name}")
            st.info(f"📊 Boyut: {file_size / 1024:.1f} KB")
            
            return uploaded_file
        
        return None

    @staticmethod
    def process_file(uploaded_file):
        """Dosyayı işler ve özetler"""
        if st.button("🔄 Metni Çıkar ve Özetle", type="primary"):
            with st.spinner("📖 Metin çıkarılıyor ve özetleniyor..."):
                text = None
                
                # Dosya türüne göre işle
                if uploaded_file.type == "application/pdf":
                    text = FileProcessor.extract_text_from_pdf(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    text = FileProcessor.extract_text_from_docx(uploaded_file)
                elif uploaded_file.type == "text/plain":
                    text = FileProcessor.extract_text_from_txt(uploaded_file)
                
                if text:
                    # Metni temizle ve özetle
                    cleaned_text = TextProcessor.clean_text(text)
                    summary = TextProcessor.summarize_text(cleaned_text)
                    
                    # Session state'e kaydet
                    st.session_state.extracted_text = cleaned_text
                    st.session_state.summary = summary
                    st.session_state.filename = uploaded_file.name
                    
                    st.success("✅ İşlem başarıyla tamamlandı!")
                    st.rerun()

    @staticmethod
    def render_results():
        """Sonuçları gösterir"""
        st.header("📋 Sonuçlar")
        
        if 'summary' in st.session_state:
            st.subheader("📄 Özet Raporu")
            st.markdown(st.session_state.summary)
            
            # İndirme ve kopyalama seçenekleri
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filename = st.session_state.get('filename', 'belge')
                txt_filename = f"{filename.split('.')[0]}_ozet.txt"
                
                st.download_button(
                    label="📥 TXT İndir",
                    data=st.session_state.summary,
                    file_name=txt_filename,
                    mime="text/plain"
                )
            
            with col2:
                if st.button("📋 Panoya Kopyala"):
                    st.code(st.session_state.summary, language=None)
                    st.info("👆 Yukarıdaki metni manuel olarak kopyalayabilirsiniz")
            
            with col3:
                if st.button("🔄 Yeni Dosya"):
                    for key in ['extracted_text', 'summary', 'filename']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
            
            # Geri bildirim
            StreamlitUI.render_feedback()
        
        # Metin önizlemesi
        StreamlitUI.render_text_preview()

    @staticmethod
    def render_feedback():
        """Geri bildirim bölümü"""
        st.markdown("---")
        st.subheader("📊 Değerlendirme")
        
        feedback = st.radio(
            "Özet kalitesi hakkında ne düşünüyorsunuz?",
            ["👍 Çok İyi", "😊 İyi", "🤔 Orta", "👎 Geliştirilmeli"],
            horizontal=True,
            key="feedback_radio"
        )
        
        if feedback:
            st.success(f"Geri bildiriminiz kaydedildi: {feedback}")
            
            if feedback in ["🤔 Orta", "👎 Geliştirilmeli"]:
                suggestion = st.text_area(
                    "Önerinizi paylaşır mısınız?",
                    placeholder="Özetleme kalitesini artırmak için önerileriniz...",
                    key="suggestion_text"
                )

    @staticmethod
    def render_text_preview():
        """Çıkarılan metin önizlemesi"""
        if 'extracted_text' in st.session_state:
            with st.expander("📖 Çıkarılan Metin Önizlemesi"):
                text = st.session_state.extracted_text
                preview_length = 1000
                
                if len(text) > preview_length:
                    preview_text = text[:preview_length] + "..."
                    st.text_area(
                        f"Metin İçeriği (İlk {preview_length} karakter)",
                        preview_text,
                        height=200,
                        disabled=True
                    )
                else:
                    st.text_area(
                        "Metin İçeriği (Tamamı)",
                        text,
                        height=200,
                        disabled=True
                    )
                
                # Metin istatistikleri
                words = len(text.split())
                chars = len(text)
                lines = len(text.split('\n'))
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Kelime Sayısı", f"{words:,}")
                with col2:
                    st.metric("Karakter Sayısı", f"{chars:,}")
                with col3:
                    st.metric("Satır Sayısı", f"{lines:,}")

def main():
    """Ana uygulama fonksiyonu"""
    # Başlık
    st.title("📄 Türkçe Dosya Özetleme Sistemi")
    st.markdown("**Akıllı Belge Analizi ve Özetleme Aracı**")
    st.markdown("---")
    
    # Yan panel
    StreamlitUI.render_sidebar()
    
    # Ana içerik
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = StreamlitUI.render_file_upload()
        if uploaded_file:
            StreamlitUI.process_file(uploaded_file)
    
    with col2:
        StreamlitUI.render_results()
    
    # Alt bilgi
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 14px;'>
            🔒 Bu uygulama tamamen offline çalışır. Dosyalarınız güvende! <br>
            🚀 Developed with ❤️ for Turkish Document Processing
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 