from PIL import Image

def preprocess_image(image, preprocessing_options):
    """
    Kullanıcı ayarlarına göre görüntüyü ön işleme tabi tutar
    
    Args:
        image: PIL.Image nesnesi
        preprocessing_options: Ön işleme seçeneklerini içeren sözlük
    
    Returns:
        PIL.Image: İşlenmiş görüntü
    """
    # Kullanıcı ayarlarına göre önişleme uygula
    img = image.copy()
    
    # Yeniden boyutlandırma
    if preprocessing_options.get('apply_resize', False):
        scale_factor = preprocessing_options.get('scale_factor', 1.5)
        width, height = img.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Eşikleme
    if preprocessing_options.get('apply_threshold', False):
        threshold_value = preprocessing_options.get('threshold_value', 128)
        img = img.convert('L')  # Gri tonlamaya dönüştür
        img = img.point(lambda x: 0 if x < threshold_value else 255, '1')  # Eşikleme uygula
    
    return img