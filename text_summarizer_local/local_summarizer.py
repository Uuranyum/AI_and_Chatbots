import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.cluster.util import cosine_distance
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tag import pos_tag
from string import punctuation
import numpy as np
from typing import List, Dict, Tuple
import networkx as nx
import re

class MetinOzetleyici:
    def __init__(self):
        # Gerekli NLTK verilerini indir
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        
        # Türkçe stop words'leri yükle
        self.stop_words = set(stopwords.words('turkish'))
        
        # Özel Türkçe stop words ve bağlaçlar ekle
        self.stop_words.update([
            've', 'veya', 'ile', 'bu', 'şu', 'için', 'gibi', 'kadar',
            'ancak', 'fakat', 'lakin', 'ama', 'çünkü', 'zira', 'dolayısıyla',
            'böylece', 'ayrıca', 'dahası', 'üstelik', 'hatta', 'örneğin'
        ])
        
        # Noktalama işaretleri
        self.punctuation = set(punctuation + '""''')
    
    def _metin_temizle(self, metin: str) -> str:
        """Metni temizler ve normalleştirir."""
        # Gereksiz boşlukları temizle
        metin = re.sub(r'\s+', ' ', metin)
        
        # Noktalama işaretlerini düzelt
        metin = re.sub(r'([.!?])\s*([.!?])+', r'\1', metin)
        metin = re.sub(r'\s*([.,!?:;])', r'\1', metin)
        
        # URL'leri temizle
        metin = re.sub(r'http\S+|www.\S+', '', metin)
        
        return metin.strip()
    
    def _cumle_ayir(self, metin: str) -> List[str]:
        """Metni cümlelere ayırır ve temizler."""
        # Özel cümle tokenizer oluştur
        tokenizer = PunktSentenceTokenizer()
        
        # Metni cümlelere ayır
        cumleler = tokenizer.tokenize(metin)
        
        # Cümleleri temizle ve filtrele
        temiz_cumleler = []
        for cumle in cumleler:
            cumle = cumle.strip()
            if (len(cumle) > 10 and  # Çok kısa cümleleri ele
                any(c.isalpha() for c in cumle) and  # En az bir harf içermeli
                cumle[-1] in '.!?'):  # Düzgün noktalama ile bitmeli
                temiz_cumleler.append(cumle)
        
        return temiz_cumleler
    
    def _cumle_onem_skoru(self, cumle: str) -> float:
        """Cümlenin önem skorunu hesaplar."""
        # Kelimeleri ve POS etiketlerini al
        kelimeler = word_tokenize(cumle.lower())
        pos_tags = pos_tag(kelimeler)
        
        # Önemli kelime sayısı
        onemli_kelime_sayisi = sum(1 for kelime, tag in pos_tags if tag.startswith(('NN', 'VB', 'JJ')))
        
        # Stop words olmayan kelime sayısı
        anlamli_kelime_sayisi = sum(1 for kelime in kelimeler if kelime not in self.stop_words)
        
        # Cümle uzunluğu skoru (çok uzun veya çok kısa cümleler için penalty)
        uzunluk_skoru = 1.0
        if len(kelimeler) < 5 or len(kelimeler) > 25:
            uzunluk_skoru = 0.7
        
        return (onemli_kelime_sayisi + anlamli_kelime_sayisi) * uzunluk_skoru
    
    def _cumle_benzerlik_skoru(self, cumle1: str, cumle2: str) -> float:
        """İki cümle arasındaki benzerlik skorunu hesaplar."""
        # Cümleleri küçük harfe çevir ve kelimelere ayır
        kelimeler1 = [word.lower() for word in word_tokenize(cumle1)]
        kelimeler2 = [word.lower() for word in word_tokenize(cumle2)]
        
        # Stop words ve noktalama işaretlerini kaldır
        kelimeler1 = [w for w in kelimeler1 if w not in self.stop_words and w not in self.punctuation]
        kelimeler2 = [w for w in kelimeler2 if w not in self.stop_words and w not in self.punctuation]
        
        # Tüm benzersiz kelimeleri bul
        tum_kelimeler = list(set(kelimeler1 + kelimeler2))
        
        # Her cümle için vektör oluştur
        vektor1 = [0] * len(tum_kelimeler)
        vektor2 = [0] * len(tum_kelimeler)
        
        # Vektörleri doldur (TF-IDF benzeri ağırlıklandırma)
        for i, kelime in enumerate(tum_kelimeler):
            if kelime in kelimeler1:
                vektor1[i] = 1 + kelimeler1.count(kelime) * 0.3
            if kelime in kelimeler2:
                vektor2[i] = 1 + kelimeler2.count(kelime) * 0.3
        
        # Kosinüs benzerliğini hesapla
        return 1 - cosine_distance(vektor1, vektor2)
    
    def _cumle_baglanti_kontrolu(self, cumle1: str, cumle2: str) -> bool:
        """İki cümle arasında mantıksal bağlantı olup olmadığını kontrol eder."""
        baglac_listesi = ['ancak', 'fakat', 'lakin', 'ama', 'çünkü', 'zira', 
                         'dolayısıyla', 'böylece', 'ayrıca', 'dahası']
        
        kelimeler2 = word_tokenize(cumle2.lower())
        return any(baglac in kelimeler2 for baglac in baglac_listesi)
    
    def ozetle(self, metin: str, ozet_uzunlugu: float = 0.3) -> str:
        """
        Metni özetler.
        
        Args:
            metin: Özetlenecek metin
            ozet_uzunlugu: Özetin orijinal metne oranı (0-1 arası)
            
        Returns:
            Özetlenmiş metin
        """
        # Metni temizle
        metin = self._metin_temizle(metin)
        
        # Metni cümlelere ayır
        cumleler = self._cumle_ayir(metin)
        
        if len(cumleler) <= 1:
            return metin
        
        # Her cümle için önem skoru hesapla
        onem_skorlari = {i: self._cumle_onem_skoru(cumle) 
                        for i, cumle in enumerate(cumleler)}
        
        # Benzerlik matrisini oluştur
        benzerlik_matrisi = np.zeros((len(cumleler), len(cumleler)))
        for i in range(len(cumleler)):
            for j in range(len(cumleler)):
                if i != j:
                    benzerlik = self._cumle_benzerlik_skoru(cumleler[i], cumleler[j])
                    # Bağlaçlı cümlelere bonus ver
                    if self._cumle_baglanti_kontrolu(cumleler[i], cumleler[j]):
                        benzerlik *= 1.2
                    benzerlik_matrisi[i][j] = benzerlik
        
        # PageRank algoritmasını uygula
        nx_graph = nx.from_numpy_array(benzerlik_matrisi)
        scores = nx.pagerank(nx_graph)
        
        # PageRank skorlarını önem skorları ile birleştir
        for i in scores:
            scores[i] = scores[i] * 0.7 + onem_skorlari[i] * 0.3
        
        # Cümleleri skorlarına göre sırala
        ranked_sentences = sorted(
            [(scores[i], i, cumle) for i, cumle in enumerate(cumleler)],
            reverse=True
        )
        
        # Özet uzunluğunu hesapla
        ozet_cumle_sayisi = int(len(cumleler) * ozet_uzunlugu)
        ozet_cumle_sayisi = max(1, min(ozet_cumle_sayisi, len(cumleler)))
        
        # Seçilen cümleleri orijinal sıralarına göre sırala
        secilen_cumleler = sorted(
            ranked_sentences[:ozet_cumle_sayisi],
            key=lambda x: x[1]
        )
        
        # Özeti oluştur
        ozet = " ".join(cumle for _, _, cumle in secilen_cumleler)
        
        return ozet

if __name__ == "__main__":
    # Test metni
    test_metin = """
    Yapay zeka, bilgisayarların insan zekasını taklit etme yeteneğidir. 
    Makine öğrenimi, yapay zekanın bir alt dalıdır ve bilgisayarların verilerden öğrenmesini sağlar. 
    Derin öğrenme ise makine öğreniminin bir alt kümesidir ve yapay sinir ağlarını kullanır. 
    Günümüzde yapay zeka, sağlık, finans, ulaşım gibi birçok alanda kullanılmaktadır. 
    Özellikle görüntü işleme ve doğal dil işleme alanlarında büyük başarılar elde edilmiştir. 
    Yapay zeka teknolojileri her geçen gün gelişmeye devam etmektedir.
    """
    
    # Özetleyiciyi oluştur
    ozetleyici = MetinOzetleyici()
    
    # Metni özetle
    ozet = ozetleyici.ozetle(test_metin, ozet_uzunlugu=0.5)
    print("Orijinal metin uzunluğu:", len(test_metin.split()))
    print("Özet uzunluğu:", len(ozet.split()))
    print("\nÖzet:")
    print(ozet) 