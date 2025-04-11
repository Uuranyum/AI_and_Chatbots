# Türkçe Metin Temizleyici ve Analiz Aracı

Bu uygulama, Türkçe metinler için geliştirilmiş kapsamlı bir metin temizleme ve analiz aracıdır. PDF, DOCX ve TXT formatındaki dosyaları işleyebilir, metinleri temizleyebilir ve çeşitli analizler gerçekleştirebilir.

## Özellikler

### Metin Temizleme
- Türkçe karakter normalizasyonu
- Sayı temizleme
- Noktalama işaretleri temizleme
- Stop words temizleme
- Üç farklı kök bulma yöntemi:
  - Turkish Stemmer
  - Zeyrek Lemmatizer
  - Hiçbiri (orijinal metin)

### Analiz Özellikleri
- Kelime bulutu görselleştirmesi
- N-gram analizi (2-5 gram)
- Detaylı metin istatistikleri
- Kelime frekans analizi
- Metin karşılaştırma

### Veri Dışa Aktarma
- JSON formatında detaylı rapor
- Tüm analiz sonuçlarını içeren raporlama

## Kurulum

1. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

2. NLTK kaynaklarını indirin:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Kullanım

Uygulamayı başlatmak için:
```bash
streamlit run text_cleaner.py
```

## Desteklenen Dosya Formatları
- PDF (.pdf)
- Word (.docx)
- Text (.txt)

## Özelleştirme Seçenekleri

### Temizleme Seçenekleri
- Hiçbir işlem uygulamama
- Türkçe karakter normalizasyonu
- Sayı temizleme
- Noktalama işaretleri temizleme
- Stop words temizleme
- Kök bulma yöntemi seçimi

### Analiz Seçenekleri
- Kelime bulutu gösterimi
- N-gram analizi
- Metin karşılaştırma

## Gereksinimler
- Python 3.8+
- Streamlit
- NLTK
- TurkishStemmer
- Zeyrek
- PyPDF2
- python-docx
- ve diğer gerekli kütüphaneler (requirements.txt dosyasında listelenmiştir)

## Lisans
MIT License

## Katkıda Bulunma
1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Bir Pull Request oluşturun 