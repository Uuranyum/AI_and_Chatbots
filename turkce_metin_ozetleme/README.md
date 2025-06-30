# 📄 Türkçe Dosya Özetleme Sistemi

Bu uygulama PDF, DOCX ve TXT dosyalarını okuyarak **Türkçe özetler** oluşturan web tabanlı bir araçtır. Tamamen **offline** çalışır ve kullanıcı verilerini güvende tutar.

## ✨ Özellikler

- 📄 **Çoklu Format Desteği**: PDF, DOCX, TXT
- 🔒 **Tamamen Offline**: İnternet bağlantısı gerektirmez
- 🇹🇷 **Türkçe Optimize**: Türkçe dil özelliklerine göre optimize edilmiş
- ⚡ **Hızlı İşleme**: Anında sonuç alma
- 📊 **Detaylı Analiz**: Kelime, cümle ve paragraf sayısı
- 💾 **Kolay Dışa Aktarma**: TXT formatında indirme
- 🎯 **Kullanıcı Dostu**: Basit ve sezgisel arayüz

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.7 veya üzeri
- pip paket yöneticisi

### Kurulum

1. **Depoyu klonlayın:**
   ```bash
   git clone https://github.com/yourusername/turkce-dosya-ozetleme.git
   cd turkce-dosya-ozetleme
   ```

2. **Sanal ortam oluşturun (önerilen):**
   ```bash
   python -m venv venv
   
   # Windows için:
   venv\Scripts\activate
   
   # macOS/Linux için:
   source venv/bin/activate
   ```

3. **Gerekli paketleri yükleyin:**
   ```bash
   pip install -r requirements_github.txt
   ```

### Çalıştırma

```bash
streamlit run github_ready_app.py
```

Uygulama otomatik olarak `http://localhost:8501` adresinde açılacaktır.

## 📖 Kullanım

1. **Dosya Yükleme**: Özetlemek istediğiniz PDF, DOCX veya TXT dosyasını yükleyin
2. **İşleme**: "Metni Çıkar ve Özetle" butonuna tıklayın
3. **Özet İnceleme**: Oluşturulan özeti inceleyin
4. **İndirme**: İsterseniz özeti TXT formatında bilgisayarınıza indirin

## 🛠️ Teknik Detaylar

### Desteklenen Dosya Formatları

| Format | Uzantı | Açıklama |
|--------|---------|----------|
| PDF | `.pdf` | Adobe PDF belgeleri |
| Word | `.docx` | Microsoft Word belgeleri |
| Metin | `.txt` | Düz metin dosyaları |

### Dosya Boyutu Limiti

- Maksimum dosya boyutu: **10 MB**
- Önerilen dosya boyutu: 1-5 MB arası (daha hızlı işleme)

### Özetleme Algoritması

Uygulama, Türkçe dilin özelliklerine göre optimize edilmiş bir özetleme algoritması kullanır:

- **Anahtar Kelime Analizi**: Türkçe'ye özel anahtar kelimeler
- **Cümle Puanlama**: Uzunluk, pozisyon ve içerik analizi
- **Bağlam Koruma**: Orijinal metindeki anlam bütünlüğünü korur
- **İki Paragraf Özet**: Mantıklı ve akıcı yapı

## 🔧 Geliştirme

### Proje Yapısı

```
├── github_ready_app.py      # Ana uygulama dosyası
├── requirements_github.txt  # Python bağımlılıkları
├── README_github.md         # Bu dosya
└── .gitignore              # Git ihmal listesi
```

### Sınıf Yapısı

- **`FileProcessor`**: Dosya okuma ve metin çıkarma
- **`TextProcessor`**: Metin temizleme ve özetleme
- **`StreamlitUI`**: Kullanıcı arayüzü yönetimi

### Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin yeni-ozellik`)
5. Pull Request oluşturun

## 📊 Performans

| Dosya Boyutu | Ortalama İşleme Süresi |
|--------------|------------------------|
| < 1 MB | 2-5 saniye |
| 1-5 MB | 5-15 saniye |
| 5-10 MB | 15-30 saniye |

## 🛡️ Güvenlik

- **Offline İşleme**: Dosyalarınız hiçbir zaman internete gönderilmez
- **Lokal Depolama**: Tüm işlemler bilgisayarınızda gerçekleşir
- **Geçici Dosyalar**: İşlem sonrası otomatik temizlik

## 📋 Sık Sorulan Sorular

### Hangi dilleri destekliyor?
Şu anda sadece **Türkçe** metinler için optimize edilmiştir. Diğer diller için temel işlevsellik mevcuttur.

### İnternet bağlantısı gerekli mi?
Hayır, uygulama tamamen **offline** çalışır.

### Dosyalarım güvende mi?
Evet, dosyalarınız bilgisayarınızdan çıkmaz ve hiçbir yere gönderilmez.

### Hangi işletim sistemlerinde çalışır?
Windows, macOS ve Linux sistemlerinde çalışır.

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 👨‍💻 Geliştirici

Bu uygulama, Türkçe doküman işleme ihtiyaçları için geliştirilmiştir.

## 🔄 Sürüm Geçmişi

### v1.0.0 (Şu anki sürüm)
- ✅ PDF, DOCX, TXT dosya desteği
- ✅ Türkçe optimize özetleme
- ✅ Web tabanlı arayüz
- ✅ Offline çalışma
- ✅ TXT dışa aktarma

## 🤝 Destek

Sorunlarınız için GitHub Issues kullanabilirsiniz.

---

**🌟 Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!** 