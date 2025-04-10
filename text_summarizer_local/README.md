# Türkçe Metin Özetleyici

Bu proje, PDF, DOCX ve TXT formatındaki Türkçe metinleri yapay zeka kullanmadan özetleyen bir web uygulamasıdır. Tamamen yerel olarak çalışır ve internet bağlantısı gerektirmez.

## Özellikler

- PDF, DOCX ve TXT dosya desteği
- Tamamen yerel çalışma (API gerektirmez)
- Özelleştirilmiş özet uzunluğu
- Metin istatistikleri (kelime sayısı, sıkıştırma oranı)
- Özet indirme özelliği
- Türkçe dil desteği
- Modern ve kullanıcı dostu arayüz

## Kurulum

Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

Uygulamayı çalıştırın:
```bash
streamlit run text_summarizer/local_app.py
```

## Örnek Kullanım

Repo içinde `examples` klasöründe örnek metin dosyaları bulunmaktadır. Bu dosyaları kullanarak uygulamayı test edebilirsiniz:

1. Uygulamayı başlatın
2. "Dosyanızı buraya yükleyin" butonuna tıklayın
3. `examples/ornek.txt` dosyasını seçin
4. Özet uzunluğunu ayarlayın (varsayılan: %30)
5. "Özetle" butonuna tıklayın

Uygulama, metni analiz edip önemli cümleleri seçerek bir özet oluşturacaktır.

## Nasıl Çalışır?

1. **Metin Analizi**: Yüklenen metin cümlelere ve kelimelere ayrılır.
2. **Benzerlik Hesaplama**: Her cümle arasındaki kosinüs benzerliği hesaplanır.
3. **PageRank Algoritması**: Cümle önemi PageRank algoritması kullanılarak belirlenir.
4. **Özet Oluşturma**: En önemli cümleler seçilerek özet oluşturulur.

## Katkıda Bulunma

1. Bu repoyu forklayın
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: Özelliğin açıklaması'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

## İletişim

Proje Linki: [https://github.com/Uuranyum/AI_and_Chatbots/tree/main/text_summarizer_local](https://github.com/Uuranyum/AI_and_Chatbots/tree/main/text_summarizer_local) 