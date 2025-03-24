from PIL import Image

def preprocess_image(image, preprocessing_options):
    """
    Pre-processes image according to user settings
    
    Args:
        image PIL.Image object
        preprocessing_options: Dictionary containing preprocessing options
    
    Returns:
        PIL.Image: Processed image
    """
    # Apply preprocessing based on user settings
    img = image.copy()
    
    # Resizing
    if preprocessing_options.get('apply_resize', False):
        scale_factor = preprocessing_options.get('scale_factor', 1.5)
        width, height = img.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Thresholding
    if preprocessing_options.get('apply_threshold', False):
        threshold_value = preprocessing_options.get('threshold_value', 128)
        img = img.convert('L')  # Convert to grayscale
        img = img.point(lambda x: 0 if x < threshold_value else 255, '1')  # Eşikleme uygula
    
    return img