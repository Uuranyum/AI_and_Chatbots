# PDF ve Görüntü OCR Uygulaması

PDF dosyalarını ve görüntüleri metin formatına dönüştürmek için Streamlit tabanlı bir OCR (Optik Karakter Tanıma) uygulaması.

## Özellikler

- PDF dosyalarını ve görüntüleri (JPG, PNG, TIFF) yükleme ve işleme
- Türkçe ve İngilizce dil desteği
- Görüntü önişleme seçenekleri (eşikleme, yeniden boyutlandırma)
- Sonuçları TXT, DOCX ve PDF formatlarında indirme
- Görsel analiz ve orijinal/işlenmiş görüntü karşılaştırma

## Gereksinimler

- Python 3.7 veya üzeri
- Tesseract OCR
- Poppler (PDF işleme için)
- Python kütüphaneleri (requirements.txt dosyasında listelenmiştir)

## Kurulum

1. Tesseract OCR'ı yükleyin:
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-tur`
   - Mac: `brew install tesseract`

2. Poppler'ı yükleyin:
   - Windows: https://github.com/oschwartz10612/poppler-windows/releases/
   - Linux: `sudo apt-get install poppler-utils`
   - Mac: `brew install poppler`

3. Python bağımlılıklarını yükleyin:
   ```
   pip install -r requirements.txt
   ```

## Kullanım

1. Uygulamayı başlatın:
   ```
   streamlit run app.py
   ```

2. Web tarayıcınızda açılan uygulamada:
   - İşlemek istediğiniz dosya türünü seçin (PDF veya Görüntü)
   - Dosyanızı yükleyin
   - OCR işlemini başlatın
   - Sonuçları görüntüleyin ve indirin

## Windows Kullanıcıları İçin Notlar

Windows'ta çalıştırırken, Tesseract OCR ve Poppler yollarının doğru ayarlandığından emin olun:

1. Tesseract yolu genellikle: `C:\Program Files\Tesseract-OCR\tesseract.exe`
2. Poppler yolu genellikle: `C:\Program Files\poppler-xx.xx.x\Library\bin`

Bu yollar, `app.py` dosyasında ayarlanabilir.

## Proje Yapısı

```
pdf_ocr_app/
├── app.py                  # Ana uygulama dosyası
├── utils/
│   ├── __init__.py         # Utils paketi
│   ├── image_processing.py # Görüntü işleme fonksiyonları
│   ├── ocr_functions.py    # OCR fonksiyonları
│   ├── file_handling.py    # Dosya işleme fonksiyonları
│   └── ui_components.py    # Kullanıcı arayüzü bileşenleri
├── requirements.txt        # Gerekli kütüphaneler
└── README.md               # Bu dosya
```

## Sorun Giderme

- **Tesseract bulunamadı hatası**: Tesseract'ın doğru şekilde yüklendiğinden ve yolun doğru ayarlandığından emin olun.
- **Poppler bulunamadı hatası**: Poppler'ın doğru şekilde yüklendiğinden ve yolun doğru olduğundan emin olun.
- **PDF dönüştürme hataları**: Uygulama, PDF'i işleyemezse alternatif bir metot deneyecektir.

## Dil Desteği

Varsayılan olarak, uygulama Türkçe ve İngilizce dillerini destekler. Başka diller eklemek için, Tesseract dil dosyalarını yüklemeniz ve UI'da seçenekleri güncellemeniz gerekir. 