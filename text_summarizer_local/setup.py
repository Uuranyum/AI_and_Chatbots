import nltk

def download_nltk_data():
    """NLTK için gerekli verileri indirir."""
    required_packages = [
        'punkt',
        'stopwords',
        'averaged_perceptron_tagger'
    ]
    
    for package in required_packages:
        try:
            nltk.download(package)
            print(f"{package} başarıyla indirildi.")
        except Exception as e:
            print(f"{package} indirilirken hata oluştu: {str(e)}")

if __name__ == "__main__":
    download_nltk_data() 