# Object Detection App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://object-detection-app.streamlit.app/)

## Overview

This is a simple object detection web application that allows you to upload photos and identify objects within them. The app uses TensorFlow Lite with a MobileNet SSD model to perform object detection directly in the browser.

![App Screenshot](https://github.com/Uuranyum/object-detection-app/raw/main/screenshot.png)

## Features

- Upload and process images in various formats (JPG, JPEG, PNG)
- Real-time object detection
- Display confidence levels for detected objects
- User-friendly interface
- Optimized for CPU processing

## How it Works

1. The app uses TensorFlow Lite as the backend for object detection
2. The MobileNet SSD model pre-trained on the COCO dataset is used to identify objects
3. When you upload an image, the model processes it and identifies objects
4. The results are displayed with bounding boxes and confidence levels

## Running the App Locally

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Installation

1. Clone this repository:
```bash
git clone https://github.com/Uuranyum/object-detection-app.git
cd object-detection-app
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

4. Open your browser and go to `http://localhost:8501`

## Deployment

This app is ready to be deployed on Streamlit Cloud. Simply push this repository to GitHub and connect it to your Streamlit Cloud account.

## Technologies Used

- [Streamlit](https://streamlit.io/): Frontend framework
- [TensorFlow Lite](https://www.tensorflow.org/lite): Lightweight ML framework
- [MobileNet SSD](https://github.com/tensorflow/models/tree/master/research/object_detection): Pre-trained object detection model
- [OpenCV](https://opencv.org/): Computer vision library
- [NumPy](https://numpy.org/): Numerical computing library
- [Pillow](https://python-pillow.org/): Image processing library

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you like this project, you can buy me a coffee!

[![Buy me a coffee](https://cdn.buymeacoffee.com/buttons/v2/default-blue.png)](https://buymeacoffee.com/ugurdemirkb) 