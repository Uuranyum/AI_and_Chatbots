import streamlit as st
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title='Data Scientist vs AI Engineer', page_icon='🧪👩‍🔬🧑‍🔬⚗️')

# Function that trains the TF-IDF model
def train_tfidf_bot(text5):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(text5)
    return vectorizer, tfidf_matrix

# Function that finds the most appropriate answer to the user's question
def get_best_answer(user_question, vectorizer, tfidf_matrix, text5):
    user_vec = vectorizer.transform([user_question])
    similarities = cosine_similarity(user_vec, tfidf_matrix).flatten()
    best_match_idx = np.argmax(similarities)
    return text5[best_match_idx]

# Sample texts for the bot to answer questions about the differences between data science and AI engineering
text5 = [
    "Data Scientist Responsibilities: Collect and process large datasets. Perform statistical analysis to identify trends. Develop and implement machine learning models. Clean and preprocess data for analysis. and Evaluate model performance and accuracy. etc.",
    "AI Engineer Responsibilities: Design and develop AI systems. Implement machine learning models. Deploy AI models to production. Optimize AI models for performance.Integrate AI solutions with existing systems. etc."
]

# train the model
vectorizer, tfidf_matrix = train_tfidf_bot(text5)

# Streamlit Interface
st.title("💾 Data Scientist vs AI Engineer")
st.write("Write a question about Data Scientist vs AI Engineer below and press Enter!")

# Get question from user
user_question = st.text_input("Question:")

if st.button("Reply") and user_question:
    best_answer = get_best_answer(user_question, vectorizer, tfidf_matrix, text5)
    st.success(f"**Answer:** {best_answer}")  