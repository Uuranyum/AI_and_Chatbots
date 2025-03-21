import streamlit as st
import pandas as pd
from pathlib import Path
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

#create .env file and add your Google API key
#GOOGLE_API_KEY=your api key
# Load API key from .env file
load_dotenv()

# Streamlit page configuration
st.set_page_config(
    page_title='Question and answer to the uploaded file',
    page_icon='🔓',
    layout='centered'
)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    st.error('Google API Key not found. Please add it to the .env file.')
    st.stop()

# Make Excel file path dynamic
current_dir = Path(__file__).parent
EXCEL_PATH = current_dir / "Your files path here.xlsx"

if not EXCEL_PATH.exists():
    st.error(f"Excel file not found: {EXCEL_PATH}")
    st.stop()

st.title('📚 QA BOT')

def temizle_metin(metin):
    if isinstance(metin, str):
        metin = re.sub(r'x000D', '', metin)
        metin = re.sub(r'\s+', ' ', metin)
        metin = metin.strip()
    return metin

@st.cache_data
def load_data():
    try:
        df = pd.read_excel(EXCEL_PATH)
        df = df.map(temizle_metin)
        return df
    except Exception as e:
        st.error(f"Error loading Excel file: {str(e)}")
        return None

def get_gemini_response(question, context):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') #gemini-1.5-pro 
        prompt = f"""
        You are a scientist. Use the contextual information below to answer the question in a different way.  
        NEVER repeat or copy the database answer word-for-word.  

        Instead, you should:  
        1. Approach the topic from a scientific and analytical perspective  
        2. Provide up-to-date research or real-world examples  
        3. Explain the topic clearly using simple and understandable language  
        4. Add relevant scientific terms or definitions if necessary  
        5. If the context is not sufficient to answer the question, respond with:  
        "Sorry, there is not enough information in the database to answer this question."  

        Context:  
        {context}  

        Question: {question}  

        Note: NEVER copy the database answer word-for-word!

        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Gemini API Hatası: {str(e)}")
        return None

def search_answer(df, user_question):
    if not user_question.strip():
        return None
        
    df['column'] = df['column'].str.lower()
    user_question = user_question.lower()
    
    best_match = None
    highest_match_count = 0
    
    for idx, row in df.iterrows():
        question_words = set(row['column'].split())
        user_words = set(user_question.split())
        
        common_words = question_words.intersection(user_words)
        
        if len(common_words) > highest_match_count:
            highest_match_count = len(common_words)
            best_match = row
    
    if best_match is not None and highest_match_count > 0:
        return {
            'main_topic': best_match['maincolumn'],
            'sub_topic': best_match['subcolumn'],
            'question': best_match['column'],
            'answer': best_match['answercolumn'],
            'keywords': best_match['keywordscolumn']
}
    return None

df = load_data()

if df is not None:
    user_question = st.text_input('Write your question here:')
    
    if user_question:
        with st.spinner('Searching...'):
            result = search_answer(df, user_question)
            
            if result:
                context = f"""
                main_topic: {result['maincolumn']}
                sub_topic: {result['subcolumn']}
                similiar question: {result['column']}
                Database Answer: {result['answercolumn']}
                """
                
                gemini_response = get_gemini_response(user_question, context)
                if gemini_response:
                    st.write(f"**Question:** {user_question}")
                    st.write(f"**Answer:**")
                    st.write(gemini_response)
            else:
                st.info('Sorry, there is not enough information on this topic in the database.')

st.markdown("---")
st.markdown("💡 Scientific Question Answer Bot") 