# Doküman Soru-Cevap Sistemi

Bu proje, kullanıcıların PDF, TXT veya DOCX formatındaki dokümanları yükleyip, içerikle ilgili sorular sorabilecekleri bir Streamlit uygulamasıdır. Uygulama, BM25 algoritması kullanarak doküman içeriğindeki en alakalı bilgileri kullanıcının sorularına cevap olarak sunar.

## Özellikler

- PDF, TXT ve DOCX formatındaki dosyaları okuma
- Metin ön işleme ve tokenizasyon
- BM25 algoritması ile sorgu-dokuman eşleştirme
- Kullanıcı dostu arayüz

## Kurulum

1. Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

2. Uygulamayı çalıştırın:

```bash
streamlit run app.py
```

## Kullanım

1. Uygulamayı başlatın
2. Dosya yükleme alanından bir doküman yükleyin (.pdf, .txt veya .docx)
3. Doküman yüklendikten sonra soru sorma alanına sorunuzu yazın
4. Uygulama, doküman içeriğinden en alakalı yanıtları gösterecektir

## Teknik Detaylar

- **Dosya Okuma:** Farklı dosya formatları için özel okuma fonksiyonları
- **Metin Ön İşleme:** Cümle ve kelime tokenizasyonu, durma kelimelerinin (stop words) kaldırılması
- **BM25 Algoritması:** Sorgu ve doküman içeriği arasındaki alaka düzeyini ölçmek için kullanılır
- **Streamlit Arayüzü:** Kullanıcı dostu bir deneyim için Streamlit framework'ü kullanılmıştır 