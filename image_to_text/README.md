# PDF and Image OCR App

A Streamlit-based OCR (Optical Character Recognition) application for converting PDF files and images to text format.

## Features

- Upload and process PDF files and images (JPG, PNG, TIFF)
- Turkish and English language support
- Image preprocessing options (thresholding, resizing)
- Download results in TXT, DOCX and PDF formats
- Visual analysis and original/processed image comparison

## Requirements

- Python 3.7 or higher
- Tesseract OCR
- Poppler (for PDF processing)
- Python libraries (listed in requirements.txt)

## Installation

1. Install Tesseract OCR:
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-tur`
   - Mac: `brew install tesseract`

2. Install Poppler:
   - Windows: https://github.com/oschwartz10612/poppler-windows/releases/
   - Linux: `sudo apt-get install poppler-utils`
   - Mac: `brew install poppler`

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Launch the application:
   ```
   streamlit run app.py
   ```

2. In the application opened in your web browser:
   - Select the file type you want to process (PDF or Image)
   - Upload your file
   - Start the OCR process
   - View and download results

## Notes for Windows Users

When running on Windows, make sure that the Tesseract OCR and Poppler paths are set correctly:

1. The Tesseract path is usually: `C:\Program Files\Tesseract-OCR\tesseract.exe`
2. The Poppler path is usually: `C:\Program Files\poppler-xx.xx.x\Library\bin`

These paths can be set in the `app.py` file.

## Project Structure

```
pdf_ocr_app/
├── app.py # Main application file
├── utils/
│ ├── __init__.py # Utils package
│ ├── image_processing.py # Image processing functions
│ ├── ocr_functions.py # OCR functions
│ ├── file_handling.py # File handling functions
│ └── ui_components.py # User interface components
├── requirements.txt # Required libraries
└── README.md # This file
```

## Troubleshooting

- **Tesseract not found error**: Make sure the Tesseract is loaded correctly and the path is set correctly.
- **Poppler not found error**: Make sure Poppler is installed correctly and the path is set correctly.
- **PDF conversion errors**: If the application cannot process the PDF, it will try an alternative method.

## Language Support

By default, the app supports Turkish and English languages. To add other languages, you need to install Tesseract language files and update options in the UI. 