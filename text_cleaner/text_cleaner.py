import streamlit as st
import pandas as pd
import numpy as np
import PyPDF2
import docx
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from TurkishStemmer import TurkishStemmer
from nltk.util import ngrams
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import io
import pickle
import string
from typing import List, Optional, Dict, Tuple
import zeyrek
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from difflib import SequenceMatcher

# NLTK kaynaklarını indir
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Türkçe morfolojik analiz için Zeyrek
analyzer = zeyrek.MorphAnalyzer()

# Türkçe stemmer
stemmer = TurkishStemmer()

# Türkçe lemmatization için sözlük
TURKISH_LEMMA_DICT = {
    # İsimler için çekim ekleri
    'lara': '',    'lere': '',    'ları': '',    'leri': '',
    'dan': '',     'den': '',     'tan': '',     'ten': '',
    'da': '',      'de': '',      'ta': '',      'te': '',
    'nin': '',     'nın': '',     'nun': '',     'nün': '',
    'ya': '',      'ye': '',      'a': '',       'e': '',
    'ı': '',       'i': '',       'u': '',       'ü': '',
    
    # Fiil çekim ekleri
    'mak': 'mek',  'mek': 'mek',
    'yor': 'mek',  'iyor': 'mek', 'üyor': 'mek', 'uyor': 'mek',
    'acak': 'mek', 'ecek': 'mek',
    'di': 'mek',   'dı': 'mek',   'du': 'mek',   'dü': 'mek',
    'ti': 'mek',   'tı': 'mek',   'tu': 'mek',   'tü': 'mek',
    
    # Yaygın yapım ekleri
    'li': '',      'lı': '',      'lu': '',      'lü': '',
    'siz': '',     'sız': '',     'suz': '',     'süz': '',
    'çi': '',      'ci': '',      'cı': '',      'cu': '',
    'lik': '',     'lık': '',     'luk': '',     'lük': '',
    
    # Çoğul ekler
    'ler': '',     'lar': ''
}

def normalize_turkish_chars(text: str) -> str:
    """Türkçe karakterleri korur ve diğer özel karakterleri temizler."""
    # Türkçe karakterleri koru
    text = text.replace('i', 'i').replace('I', 'İ')
    text = text.replace('ı', 'ı').replace('İ', 'İ')
    
    # Diğer özel karakterleri temizle
    special_chars = {
        '\'': '',
        '"': '',
        ''': '',
        ''': '',
        '"': '',
        '"': '',
        '«': '',
        '»': '',
        '—': '-',
        '–': '-'
    }
    for old, new in special_chars.items():
        text = text.replace(old, new)
    return text

def get_turkish_stopwords() -> set:
    """Genişletilmiş Türkçe stopwords listesi."""
    stop_words = set(stopwords.words('turkish'))
    
    # Ek Türkçe stop words
    additional_stops = {
        've', 'veya', 'ile', 'için', 'gibi', 'kadar', 'göre', 'ancak', 'fakat',
        'ama', 'lakin', 'yani', 'da', 'de', 'ki', 'mi', 'mu', 'mı', 'mü',
        'bir', 'bu', 'şu', 'şey', 'böyle', 'şöyle', 'öyle', 'nasıl', 'neden',
        'ne', 'niye', 'kim', 'hangi', 'hani', 'çünkü', 'zira', 'eğer', 'ise',
        'ama', 'fakat', 'lakin', 'yalnız', 'ancak', 'oysa', 'oysaki', 'halbuki',
        'üzere', 'diye', 'ayrıca', 'hem', 'bile', 'dahi'
    }
    stop_words.update(additional_stops)
    return stop_words

def clean_turkish_text(text: str) -> str:
    """Türkçe metni temizler ve düzenler."""
    # Gereksiz boşlukları temizle
    text = ' '.join(text.split())
    
    # Sayıları temizle (tarihler hariç)
    text = re.sub(r'(?<!\d)\d+(?!\d)', '', text)
    
    # URL'leri temizle
    text = re.sub(r'http\S+|www.\S+', '', text)
    
    # E-posta adreslerini temizle
    text = re.sub(r'\S+@\S+', '', text)
    
    return text

def turkish_stem(word: str) -> str:
    """Türkçe kelime kökünü bulur."""
    return stemmer.stem(word)

def turkish_lemmatize(word: str) -> str:
    """Türkçe kelime lemmatization."""
    word = word.lower()
    original = word
    
    # En uzun eki bul ve kaldır
    while True:
        found_suffix = False
        for suffix in TURKISH_LEMMA_DICT:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                replacement = TURKISH_LEMMA_DICT[suffix]
                word = word[:-len(suffix)] + replacement
                found_suffix = True
                break
        if not found_suffix:
            break
    
    # Eğer kelime çok kısaldıysa orijinali döndür
    if len(word) < 3:
        return original
    
    return word

def clean_text(text: str, 
               normalize_chars: bool = True,
               remove_nums: bool = True,
               remove_puncts: bool = True,
               remove_stopwords: bool = True,
               do_stemming: bool = True,
               do_lemmatization: bool = False) -> str:
    """Gelişmiş Türkçe metin temizleme fonksiyonu"""
    
    # Temel temizlik
    text = clean_turkish_text(text)
    
    if normalize_chars:
        text = normalize_turkish_chars(text)
    
    # Noktalama işaretlerini temizle (özel karakterleri koru)
    if remove_puncts:
        text = re.sub(r'[^\w\s\u0080-\uffff]', ' ', text)
    
    # Fazla boşlukları temizle
    text = ' '.join(text.split())
    
    # Kelimelere ayır
    words = word_tokenize(text)
    
    # Küçük harfe çevir (İ ve I harflerini doğru şekilde)
    words = [word.replace('I', 'ı').replace('İ', 'i').lower() for word in words]
    
    if remove_stopwords:
        stop_words = get_turkish_stopwords()
        words = [word for word in words if word not in stop_words]
    
    # Stemming ve Lemmatization seçenekleri
    if do_stemming and not do_lemmatization:
        words = [turkish_stem(word) for word in words]
    elif do_lemmatization and not do_stemming:
        words = [turkish_lemmatize(word) for word in words]
    
    return ' '.join(words)

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def read_docx(file):
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def create_tfidf(text):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text])
    return vectorizer, tfidf_matrix

def calculate_text_statistics(text: str, cleaned_text: str) -> Dict:
    """Metin istatistiklerini hesaplar."""
    # Orijinal metin istatistikleri
    original_words = text.split()
    original_sentences = sent_tokenize(text)
    
    # Temizlenmiş metin istatistikleri
    cleaned_words = cleaned_text.split()
    
    # En sık kullanılan kelimeler
    word_freq = Counter(cleaned_words)
    top_words = dict(word_freq.most_common(10))
    
    # Kelime uzunluk dağılımı
    word_lengths = [len(word) for word in cleaned_words]
    
    return {
        'original_stats': {
            'total_words': len(original_words),
            'total_sentences': len(original_sentences),
            'avg_sentence_length': len(original_words) / len(original_sentences) if original_sentences else 0,
            'total_chars': len(text)
        },
        'cleaned_stats': {
            'total_words': len(cleaned_words),
            'unique_words': len(set(cleaned_words)),
            'avg_word_length': sum(word_lengths) / len(word_lengths) if word_lengths else 0,
            'vocabulary_density': len(set(cleaned_words)) / len(cleaned_words) if cleaned_words else 0
        },
        'word_frequency': top_words,
        'word_lengths': word_lengths
    }

def plot_word_frequency(word_freq: Dict) -> plt.Figure:
    """En sık kullanılan kelimelerin grafiğini oluşturur."""
    fig, ax = plt.subplots(figsize=(10, 6))
    words = list(word_freq.keys())
    freqs = list(word_freq.values())
    
    sns.barplot(x=freqs, y=words, ax=ax)
    ax.set_title("En Sık Kullanılan 10 Kelime")
    ax.set_xlabel("Frekans")
    ax.set_ylabel("Kelimeler")
    
    return fig

def plot_word_length_dist(word_lengths: List[int]) -> plt.Figure:
    """Kelime uzunluklarının dağılım grafiğini oluşturur."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(word_lengths, ax=ax, bins=20)
    ax.set_title("Kelime Uzunluğu Dağılımı")
    ax.set_xlabel("Kelime Uzunluğu")
    ax.set_ylabel("Frekans")
    
    return fig

def export_detailed_report(text: str, cleaned_text: str, stats: Dict, parameters: Dict) -> Dict:
    """Detaylı rapor oluşturur."""
    return {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'original_text_length': len(text),
            'cleaned_text_length': len(cleaned_text),
            'cleaning_parameters': parameters
        },
        'statistics': stats,
        'sample': {
            'original_text_sample': text[:500] + "..." if len(text) > 500 else text,
            'cleaned_text_sample': cleaned_text[:500] + "..." if len(cleaned_text) > 500 else cleaned_text
        }
    }

def generate_word_cloud(text: str) -> plt.Figure:
    """Kelime bulutu oluşturur."""
    wordcloud = WordCloud(
        width=800, 
        height=400,
        background_color='white',
        font_path='arial.ttf'  # Türkçe karakterler için uygun font
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

def analyze_ngrams(text: str, n: int = 2) -> Dict:
    """N-gram analizi yapar."""
    words = word_tokenize(text)
    n_grams = list(ngrams(words, n))
    n_gram_freq = Counter(n_grams)
    return dict(n_gram_freq.most_common(10))

def plot_ngrams(ngram_freq: Dict, n: int) -> plt.Figure:
    """N-gram frekans grafiği oluşturur."""
    fig, ax = plt.subplots(figsize=(12, 6))
    labels = [' '.join(k) for k in ngram_freq.keys()]
    values = list(ngram_freq.values())
    
    sns.barplot(x=values, y=labels, ax=ax)
    ax.set_title(f"En Sık Kullanılan {n}-gram'lar")
    ax.set_xlabel("Frekans")
    ax.set_ylabel(f"{n}-gram")
    
    return fig

def compare_texts(text1: str, text2: str) -> Dict:
    """İki metni karşılaştırır."""
    # Benzerlik oranı
    similarity_ratio = SequenceMatcher(None, text1, text2).ratio()
    
    # Ortak kelimeler
    words1 = set(word_tokenize(text1.lower()))
    words2 = set(word_tokenize(text2.lower()))
    common_words = words1.intersection(words2)
    
    return {
        'similarity_ratio': similarity_ratio,
        'common_words': len(common_words),
        'unique_to_text1': len(words1 - words2),
        'unique_to_text2': len(words2 - words1)
    }

def plot_text_comparison(comparison_data: Dict) -> plt.Figure:
    """Metin karşılaştırma görselleştirmesi."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Benzerlik grafiği
    ax1.pie([comparison_data['similarity_ratio'], 1 - comparison_data['similarity_ratio']],
            labels=['Benzer', 'Farklı'],
            colors=['green', 'red'],
            autopct='%1.1f%%')
    ax1.set_title("Metinler Arası Benzerlik Oranı")
    
    # Kelime dağılımı
    data = [
        comparison_data['unique_to_text1'],
        comparison_data['common_words'],
        comparison_data['unique_to_text2']
    ]
    labels = ['Sadece Metin 1', 'Ortak', 'Sadece Metin 2']
    
    ax2.bar(labels, data)
    ax2.set_title("Kelime Dağılımı")
    
    plt.tight_layout()
    return fig

def main():
    st.set_page_config(page_title="Metin Temizleyici ve Chatbot Hazırlayıcı", layout="wide")
    st.title("Metin Temizleyici ve Chatbot Hazırlayıcı")
    
    # Ana metin yükleme
    uploaded_file = st.file_uploader("Dosya Yükle (PDF, DOCX veya TXT)", 
                                   type=['pdf', 'docx', 'txt'])
    
    # Karşılaştırma için ikinci metin yükleme
    compare_mode = st.sidebar.checkbox("Metin Karşılaştırma Modu")
    if compare_mode:
        uploaded_file2 = st.file_uploader("İkinci Dosya Yükle (PDF, DOCX veya TXT)",
                                        type=['pdf', 'docx', 'txt'])
    
    if uploaded_file is not None:
        # Dosya türüne göre okuma işlemi
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            text = read_pdf(uploaded_file)
        elif file_extension == 'docx':
            text = read_docx(uploaded_file)
        else:  # txt
            text = uploaded_file.getvalue().decode('utf-8')
            
        st.subheader("Orijinal Metin")
        st.text_area("", text, height=200)
        
        # Temizleme seçenekleri
        st.sidebar.header("Temizleme Seçenekleri")
        normalize_chars = st.sidebar.checkbox("Türkçe karakterleri normalize et", value=True)
        remove_nums = st.sidebar.checkbox("Sayıları temizle", value=True)
        remove_puncts = st.sidebar.checkbox("Noktalama işaretlerini temizle", value=True)
        remove_stopwords = st.sidebar.checkbox("Stop words'leri temizle", value=True)
        
        # Kök bulma seçenekleri
        st.sidebar.subheader("Kök Bulma Yöntemi")
        stemming_option = st.sidebar.radio(
            "Kök Bulma Yöntemi Seçin:",
            ["Hiçbiri", "Stemming", "Lemmatization"]
        )
        
        do_stemming = stemming_option == "Stemming"
        do_lemmatization = stemming_option == "Lemmatization"
        
        # Analiz seçenekleri
        st.sidebar.header("Analiz Seçenekleri")
        show_wordcloud = st.sidebar.checkbox("Kelime Bulutu Göster", value=True)
        show_ngrams = st.sidebar.checkbox("N-gram Analizi Göster", value=True)
        
        if show_ngrams:
            n_value = st.sidebar.slider("N-gram Değeri", min_value=2, max_value=5, value=2)
        
        # Metin temizleme
        cleaned_text = clean_text(
            text,
            normalize_chars=normalize_chars,
            remove_nums=remove_nums,
            remove_puncts=remove_puncts,
            remove_stopwords=remove_stopwords,
            do_stemming=do_stemming,
            do_lemmatization=do_lemmatization
        )
        
        st.subheader("Temizlenmiş Metin")
        st.text_area("", cleaned_text, height=200)
        
        # Metin istatistikleri hesaplama
        stats = calculate_text_statistics(text, cleaned_text)
        
        # İstatistikleri görüntüleme
        st.subheader("Metin İstatistikleri")
        
        # Temel istatistikler
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Toplam Kelime Sayısı", stats['original_stats']['total_words'])
        with col2:
            st.metric("Temizlenmiş Kelime Sayısı", stats['cleaned_stats']['total_words'])
        with col3:
            st.metric("Benzersiz Kelime Sayısı", stats['cleaned_stats']['unique_words'])
        with col4:
            st.metric("Cümle Sayısı", stats['original_stats']['total_sentences'])
        
        # Detaylı istatistikler
        st.subheader("Detaylı İstatistikler")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Orijinal Metin:")
            st.write(f"- Ortalama Cümle Uzunluğu: {stats['original_stats']['avg_sentence_length']:.2f} kelime")
            st.write(f"- Toplam Karakter Sayısı: {stats['original_stats']['total_chars']}")
        
        with col2:
            st.write("Temizlenmiş Metin:")
            st.write(f"- Ortalama Kelime Uzunluğu: {stats['cleaned_stats']['avg_word_length']:.2f} karakter")
            st.write(f"- Kelime Çeşitliliği: {stats['cleaned_stats']['vocabulary_density']:.2%}")
        
        # Görselleştirmeler
        st.subheader("Metin Analiz Grafikleri")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("En Sık Kullanılan Kelimeler")
            fig_freq = plot_word_frequency(stats['word_frequency'])
            st.pyplot(fig_freq)
        
        with col2:
            st.write("Kelime Uzunluğu Dağılımı")
            fig_dist = plot_word_length_dist(stats['word_lengths'])
            st.pyplot(fig_dist)
        
        # Kelime Bulutu
        if show_wordcloud:
            st.subheader("Kelime Bulutu")
            fig_cloud = generate_word_cloud(cleaned_text)
            st.pyplot(fig_cloud)
        
        # N-gram Analizi
        if show_ngrams:
            st.subheader(f"{n_value}-gram Analizi")
            ngram_freq = analyze_ngrams(cleaned_text, n_value)
            fig_ngram = plot_ngrams(ngram_freq, n_value)
            st.pyplot(fig_ngram)
        
        # Metin Karşılaştırma
        if compare_mode and uploaded_file2 is not None:
            st.subheader("Metin Karşılaştırma")
            
            # İkinci metni oku ve temizle
            file_extension2 = uploaded_file2.name.split('.')[-1].lower()
            if file_extension2 == 'pdf':
                text2 = read_pdf(uploaded_file2)
            elif file_extension2 == 'docx':
                text2 = read_docx(uploaded_file2)
            else:
                text2 = uploaded_file2.getvalue().decode('utf-8')
            
            cleaned_text2 = clean_text(
                text2,
                normalize_chars=normalize_chars,
                remove_nums=remove_nums,
                remove_puncts=remove_puncts,
                remove_stopwords=remove_stopwords,
                do_stemming=do_stemming,
                do_lemmatization=do_lemmatization
            )
            
            comparison_data = compare_texts(cleaned_text, cleaned_text2)
            fig_comparison = plot_text_comparison(comparison_data)
            st.pyplot(fig_comparison)
            
            st.write(f"Benzerlik Oranı: {comparison_data['similarity_ratio']:.2%}")
            st.write(f"Ortak Kelime Sayısı: {comparison_data['common_words']}")
        
        # Veri kaydetme seçenekleri
        if st.button("Verileri Kaydet"):
            report = export_detailed_report(
                text, 
                cleaned_text, 
                {
                    **stats,
                    'ngrams': analyze_ngrams(cleaned_text, 2) if show_ngrams else {},
                    'comparison': comparison_data if compare_mode and uploaded_file2 else {}
                },
                {
                    'normalize_chars': normalize_chars,
                    'remove_nums': remove_nums,
                    'remove_puncts': remove_puncts,
                    'remove_stopwords': remove_stopwords,
                    'do_stemming': do_stemming,
                    'do_lemmatization': do_lemmatization
                }
            )
            
            report_json = json.dumps(report, ensure_ascii=False, indent=2)
            st.download_button(
                label="Detaylı Raporu İndir (JSON)",
                data=report_json.encode('utf-8'),
                file_name="text_analysis_report.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()