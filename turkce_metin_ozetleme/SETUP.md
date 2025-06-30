# 🚀 Hızlı Kurulum Rehberi

Bu rehber, Türkçe Dosya Özetleme Sistemi'ni GitHub'dan indirip çalıştırmanız için gereken adımları açıklar.

## 📋 Ön Koşullar

- **Python 3.7+** yüklü olmalı
- **Git** yüklü olmalı
- **pip** paket yöneticisi aktif olmalı

### Python Kontrolü
```bash
python --version
# veya
python3 --version
```

## ⚡ Hızlı Kurulum (5 dakika)

### 1. Depoyu İndirin
```bash
git clone https://github.com/yourusername/turkce-dosya-ozetleme.git
cd turkce-dosya-ozetleme
```

### 2. Sanal Ortam Oluşturun
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux  
python3 -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements_github.txt
```

### 4. Uygulamayı Başlatın
```bash
streamlit run github_ready_app.py
```

## 🌐 Tarayıcıda Açma

Uygulama otomatik olarak açılmazsa:
- **Adres:** http://localhost:8501
- **Port:** 8501

## 🔧 Sorun Giderme

### Port Zaten Kullanımda
```bash
streamlit run github_ready_app.py --server.port 8502
```

### Python Bulunamadı
- Windows: Microsoft Store'dan Python yükleyin
- macOS: `brew install python3`
- Linux: `sudo apt install python3 python3-pip`

### Streamlit Komut Bulunamadı
```bash
pip install --upgrade streamlit
```

### Encoding Hataları (Windows)
PowerShell'de:
```powershell
chcp 65001
```

## 📦 Geliştirme Kurulumu

Geliştirme yapmak istiyorsanız:

```bash
# Ek geliştirme araçları
pip install pytest black flake8

# Pre-commit hooks
pip install pre-commit
pre-commit install
```

## 🐳 Docker ile Çalıştırma (İsteğe Bağlı)

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements_github.txt .
RUN pip install -r requirements_github.txt

COPY github_ready_app.py .
EXPOSE 8501

CMD ["streamlit", "run", "github_ready_app.py", "--server.address", "0.0.0.0"]
```

```bash
# Docker komutları
docker build -t turkce-ozetleme .
docker run -p 8501:8501 turkce-ozetleme
```

## 📱 Mobil Kullanım

Mobil cihazlarda da çalışır:
- Aynı ağdaki cihazlardan `http://BILGISAYAR-IP:8501` ile erişin
- IP adresinizi öğrenmek için: `ipconfig` (Windows) veya `ifconfig` (macOS/Linux)

## ⚠️ Önemli Notlar

- **Güvenlik**: Uygulama tamamen offline çalışır
- **Dosya Boyutu**: Maksimum 10 MB
- **Desteklenen Formatlar**: PDF, DOCX, TXT
- **Türkçe Karakterler**: Tam destek

## 🆘 Yardım

Sorunlarınız için:
1. GitHub Issues sayfasını kontrol edin
2. Yeni issue oluşturun
3. Hata loglarını paylaşın

## 🎯 Test Etme

Kurulumu test etmek için küçük bir TXT dosyası ile deneyin:

```bash
echo "Bu bir test belgesidir. Özetleme işlemi çalışıyor mu kontrol edelim." > test.txt
```

Sonra `test.txt` dosyasını uygulamaya yükleyin.

---

**✅ Kurulum tamamlandı! Artık belgelerinizi özetleyebilirsiniz.** 