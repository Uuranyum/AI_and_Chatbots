import streamlit as st
import nltk
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from rank_bm25 import BM25Okapi
import docx
import fitz
import io

# download nltk resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

def read_text_file(file):
    """Reads the text file and returns the text content."""
    return file.getvalue().decode("utf-8")

def read_docx_file(file):
    """Reads the docx file and returns the text content."""
    doc = docx.Document(io.BytesIO(file.getvalue()))
    text = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)
    return '\n'.join(text)

def read_pdf_file(file):
    """Reads the pdf file and returns the text content."""
    pdf_file = fitz.open(stream=file.getvalue(), filetype="pdf")
    text = []
    for page_num in range(len(pdf_file)):
        page = pdf_file[page_num]
        text.append(page.get_text())
    return '\n'.join(text)

def preprocess_text(text):
    """Preprocesses the text content."""
    sentences = sent_tokenize(text)

    # create a paragraph from the 1-3 sentences
    paragraphs = []
    current_paragraph = []
    for sent in sentences:
        current_paragraph.append(sent)
        if len(current_paragraph) >= 3 or len(''.join(current_paragraph)) > 300:
            paragraphs.append(' '.join(current_paragraph))
            current_paragraph = []

    # Add the remaining sentences
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))

    return paragraphs

def tokenize_text(text, is_query=False):
    """Tokenizes and remove the stop words of the text content."""
    # lower case
    text = text.lower()
    # punctuation removal
    text = re.sub(r'[^\w\s]', '', text)
    # tokenize
    tokens = word_tokenize(text)
    # remove stopwords
    stop_words = set(stopwords.words('turkish'))
    if is_query:
        reduced_stop_words = {w for w in stop_words if len(w) < 3}
        filtered_tokens = [word for word in tokens if word not in reduced_stop_words]
    else:
        filtered_tokens = [word for word in tokens if word not in stop_words]

    return filtered_tokens

def create_bm25_index(paragraphs):
    """Creates the BM25 index."""
    tokenized_paragraphs = [tokenize_text(p) for p in paragraphs]
    bm25 = BM25Okapi(tokenized_paragraphs)
    return bm25, tokenized_paragraphs, paragraphs

def search_with_bm25(query, bm25, tokenized_paragraphs, paragraphs, top_k=3):
    """Searches the query with BM25 and returns the top k paragraphs."""
    tokenized_query = tokenize_text(query, is_query=True)

    # Search with bm25
    scores = bm25.get_scores(tokenized_query)
    
    # Get top k indices
    top_indices = np.argsort(scores)[-top_k:][::-1]

    # create the results
    results = []
    for i in top_indices:
        if scores[i] > 0:
            results.append({
                'paragraph': paragraphs[i],
                'score': scores[i]
            })
    return results

def main():
    st.title("Document QA Bot")

    # File Upload site
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "docx", "pdf"])    

    if uploaded_file is not None:
        with st.spinner('Processing...'):
            file_type = uploaded_file.name.split('.')[-1].lower()
            
            if file_type == 'txt':
                text = read_text_file(uploaded_file)
            elif file_type == 'docx':
                text = read_docx_file(uploaded_file)
            elif file_type == 'pdf':
                text = read_pdf_file(uploaded_file)

            paragraphs = preprocess_text(text)
            bm25, tokenized_paragraphs, paragraphs = create_bm25_index(paragraphs)

            st.success(f'File uploaded successfully! {len(paragraphs)} paragraphs found.')

            with st.expander("About The Text"):
                st.write(f'Total number of paragraphs: {len(paragraphs)}')
                st.write(f'Total number of words: {len(text.split())}')
                st.write(f'Total number of characters: {len(text)}')
                st.write(f'Example Paragraph: {paragraphs[0][:300]}...')

            query = st.text_input("Enter your question:")

            if query:
                results = search_with_bm25(query, bm25, tokenized_paragraphs, paragraphs)
                
                if results:
                    st.subheader("Yanıtlar:")
                    
                    for i, result in enumerate(results):
                        with st.container():
                            st.markdown(f"**Yanıt {i+1}** (Benzerlik Skoru: {result['score']:.2f})")
                            st.write(result['paragraph'])
                            st.divider()
                else:
                    st.warning("Sorunuzla ilgili yanıt bulunamadı. Lütfen soruyu yeniden formüle edin.")

if __name__ == "__main__":
    main()