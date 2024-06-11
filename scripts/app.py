from flask import Flask, request, jsonify, render_template
import os
import pickle
import fitz  # PyMuPDF
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'), static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static'))

# Load pre-trained model
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'best_model.pkl'), 'rb') as f:
    best_model = pickle.load(f)

# Preprocessing function
nltk.download('punkt')
nltk.download('stopwords')
stopwords_set = set(stopwords.words('english'))

def preprocess_text(text):
    if isinstance(text, str):
        tokens = word_tokenize(text)
        words = [word.lower() for word in tokens if word.isalpha()]
        words = [word for word in words if word not in stopwords_set and word not in string.punctuation]
        return ' '.join(words)
    else:
        return ''

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    resume_files = request.files.getlist('resume_files')
    job_file = request.files.get('job_file')
    job_text = request.form.get('job_text')

    resume_texts = []
    for file in resume_files:
        file_path = os.path.join('/tmp', secure_filename(file.filename))
        file.save(file_path)
        text = extract_text_from_pdf(file_path)
        resume_texts.append(preprocess_text(text))

    if job_file:
        job_file_path = os.path.join('/tmp', secure_filename(job_file.filename))
        job_file.save(job_file_path)
        job_text = preprocess_text(extract_text_from_pdf(job_file_path))
    else:
        job_text = preprocess_text(job_text)

    combined_texts = resume_texts + [job_text]
    tfidf_matrix = vectorizer.fit_transform(combined_texts)

    similarity_scores = cosine_similarity(tfidf_matrix[:-1], tfidf_matrix[-1:])

    matches = best_model.predict(similarity_scores)

    results = {
        'similarity_scores': similarity_scores.tolist(),
        'matches': matches.tolist()
    }

    return jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)