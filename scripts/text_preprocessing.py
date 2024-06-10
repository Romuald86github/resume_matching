import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    tokens = word_tokenize(text)
    words = [word.lower() for word in tokens if word.isalpha()]
    stopwords_set = set(stopwords.words('english'))
    words = [word for word in words if word not in stopwords_set and word not in string.punctuation]
    return ' '.join(words)

if __name__ == "__main__":
    with open('intermediate_data/resume_texts.txt', 'r') as f:
        resume_texts = f.readlines()

    with open('intermediate_data/job_texts.txt', 'r') as f:
        job_texts = f.readlines()

    preprocessed_resumes = [preprocess_text(text) for text in resume_texts]
    preprocessed_jobs = [preprocess_text(text) for text in job_texts]

    with open('intermediate_data/preprocessed_resumes.txt', 'w') as f:
        for text in preprocessed_resumes:
            f.write("%s\n" % text)

    with open('intermediate_data/preprocessed_jobs.txt', 'w') as f:
        for text in preprocessed_jobs:
            f.write("%s\n" % text)
