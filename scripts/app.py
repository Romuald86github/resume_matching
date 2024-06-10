from flask import Flask, request, jsonify
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import PyPDF2

app = Flask(__name__)

# Load pre-trained model
with open('models/best_model.pkl', 'rb') as f:
    best_model = pickle.load(f)

# Preprocessing function
nltk.download('punkt')
nltk.download('stopwords')
stopwords_set = set(stopwords.words('english'))

def preprocess_text(text):
    tokens = word_tokenize(text)
    words = [word.lower() for word in tokens if word.isalpha()]
    words = [word for word in words if word not in stopwords_set and word not in string.punctuation]
    return ' '.join(words)

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    return text

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    job_text = preprocess_text(data.get('job_text', ''))

    if 'job_file' in request.files:
        job_file = request.files['job_file']
        job_text = extract_text_from_pdf(job_file)

    resume_texts = []
    for resume_file in request.files.getlist('resume_files'):
        resume_text = extract_text_from_pdf(resume_file)
        resume_texts.append(preprocess_text(resume_text))

    combined_texts = resume_texts + [job_text]
    tfidf_matrix = vectorizer.fit_transform(combined_texts)

    predictions = []
    for i in range(len(resume_texts)):
        similarity = cosine_similarity(tfidf_matrix[i:i+1], tfidf_matrix[-1:])[0][0]
        prediction = best_model.predict([[similarity]])
        predictions.append({'similarity': similarity, 'match': bool(prediction[0])})

    return jsonify(predictions)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)