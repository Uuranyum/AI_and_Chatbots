# Text Summarizer

A Streamlit web application that extracts text from PDF, TXT, DOCX, and DOC files and generates automatic summaries using Google's Gemini AI.

## Features

- Supports PDF, TXT, DOCX, and DOC file formats
- Uses Google's Gemini 1.5 Pro model for high-quality text summarization
- User-friendly interface
- Download summaries as text files
- Secure API key input
- Responsive design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/text-summarizer.git
cd text-summarizer
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Open the application in your web browser at `http://localhost:8501`
3. Enter your Gemini API key
4. Click "Upload your file here" and select a supported file
5. Click "Summarize" to generate the summary
6. View the summary and download it if needed

## Technologies Used

- Streamlit
- PyPDF2
- python-docx
- Google Generative AI (Gemini)
- NLTK
- Python 3.x

## Requirements

- Python 3.7 or higher
- Gemini API key
- Required Python packages (listed in requirements.txt)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you find this project helpful, consider buying me a coffee! ☕
[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg)](https://buymeacoffee.com/ugurdemirkb) 