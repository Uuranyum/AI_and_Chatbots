import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import tensorflow as tf
import urllib.request
import time
import shutil

# Page configuration
st.set_page_config(
    page_title="Object Detection App",
    page_icon="🔍",
    layout="wide"
)

# Header
st.title("🔍 Object Detection App")
st.write("This app allows you to detect objects in your photos.")

# Create models directory in the current app directory
@st.cache_resource
def create_model_dir():
    # Get the absolute path to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, 'models')
    
    # Create the models directory if it doesn't exist
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    
    return models_dir

# Download MobileNet model
@st.cache_resource
def download_model():
    # Create folder for model files
    models_dir = create_model_dir()
    
    # Download MobileNet SSD v1 (COCO) model
    model_url = "https://tfhub.dev/tensorflow/lite-model/ssd_mobilenet_v1/1/metadata/2?lite-format=tflite"
    model_path = os.path.join(models_dir, "ssd_mobilenet_v1.tflite")
    
    if not os.path.exists(model_path):
        with st.spinner("Downloading model..."):
            urllib.request.urlretrieve(model_url, model_path)
    
    # Download file containing COCO class labels
    labels_url = "https://raw.githubusercontent.com/amikelive/coco-labels/master/coco-labels-paper.txt"
    labels_path = os.path.join(models_dir, "coco-labels.txt")
    
    if not os.path.exists(labels_path):
        with st.spinner("Downloading labels..."):
            urllib.request.urlretrieve(labels_url, labels_path)
    
    # Read labels
    with open(labels_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    
    # Create TensorFlow Lite Interpreter
    try:
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter, labels
    except Exception as e:
        st.error(f"Error initializing interpreter: {str(e)}")
        st.error("Please try reloading the page.")
        return None, labels

try:
    # Load model and labels
    interpreter, labels = download_model()
    
    if interpreter:
        st.success("Model successfully loaded!")
        
        # Get model information
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        height = input_details[0]['shape'][1]
        width = input_details[0]['shape'][2]
    else:
        st.stop()
    
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.stop()

# Object detection function
def detect_objects(image_np, interpreter, labels):
    # Resize image to match model input size
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_shape = input_details[0]['shape']
    height = input_shape[1]
    width = input_shape[2]
    
    input_image = cv2.resize(image_np, (width, height))
    input_image = np.expand_dims(input_image, axis=0)
    
    # Run the model
    interpreter.set_tensor(input_details[0]['index'], input_image)
    interpreter.invoke()
    
    # Get results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[2]['index'])[0]
    
    # Filter results and visualize
    result_image = image_np.copy()
    detected_objects = []
    
    for i in range(len(scores)):
        if scores[i] > 0.5:  # Confidence threshold
            ymin, xmin, ymax, xmax = boxes[i]
            
            # Convert normalized coordinates to pixel values
            xmin = int(xmin * image_np.shape[1])
            xmax = int(xmax * image_np.shape[1])
            ymin = int(ymin * image_np.shape[0])
            ymax = int(ymax * image_np.shape[0])
            
            # Class information
            class_id = int(classes[i])
            class_name = labels[class_id] if class_id < len(labels) else f"Class {class_id}"
            confidence = float(scores[i])
            
            # Draw bounding box
            cv2.rectangle(result_image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            
            # Draw label
            label = f"{class_name}: {confidence:.2%}"
            cv2.putText(result_image, label, (xmin, ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Save detected object
            detected_objects.append({
                "class": class_name,
                "confidence": confidence
            })
    
    return result_image, detected_objects

# File upload
uploaded_file = st.file_uploader("Upload a photo", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Image processing
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Object detection
    with st.spinner("Detecting objects..."):
        try:
            result_image, detected_objects = detect_objects(image_np, interpreter, labels)
            
            # Show results
            st.subheader("Detected Objects:")
            
            # Result image
            st.image(result_image, caption="Detection Result", use_column_width=True)
            
            # Detected objects
            if detected_objects:
                for obj in detected_objects:
                    st.write(f"- {obj['class']}: {obj['confidence']:.2%} confidence")
            else:
                st.info("No objects detected.")
                
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

# Information note
st.info("""
### Information
- This app uses TensorFlow Lite and MobileNet SSD model
- Optimized to run on CPU
- Supported file formats: JPG, JPEG, PNG
""") 

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by [Ugur Demirkaya](https://github.com/Uuranyum)")            

st.markdown("---")
st.markdown("""
    <div style='display: flex; justify-content: center;'>
        <div style='text-align: center; padding: 15px; background-color: #f0f2f6; border-radius: 10px; margin: 20px 0; width: 33%;'>
            <h3 style='color: #1f77b4;'>If you like the app, you can buy me a coffee! ☕</h3>
            <a href="https://buymeacoffee.com/ugurdemirkb" target="_blank">
                <img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy me a coffee" style="height: 60px !important;width: 217px !important; margin: 10px 0;">
            </a>
            <p style='color: #666; font-size: 14px;'>Thank you for your support!</p>
        </div>
    </div>
""", unsafe_allow_html=True) 