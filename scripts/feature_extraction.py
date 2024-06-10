from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def convert_to_tfidf(resume_texts, job_texts):
    vectorizer = TfidfVectorizer()
    all_texts = resume_texts + job_texts
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    resume_tfidf = tfidf_matrix[:len(resume_texts)]
    job_tfidf = tfidf_matrix[len(resume_texts):]
    return resume_tfidf, job_tfidf

if __name__ == "__main__":
    with open('intermediate_data/preprocessed_resumes.txt', 'r') as f:
        preprocessed_resumes = f.readlines()

    with open('intermediate_data/preprocessed_jobs.txt', 'r') as f:
        preprocessed_jobs = f.readlines()

    resume_tfidf, job_tfidf = convert_to_tfidf(preprocessed_resumes, preprocessed_jobs)
    
    np.save('intermediate_data/resume_tfidf.npy', resume_tfidf.toarray())
    np.save('intermediate_data/job_tfidf.npy', job_tfidf.toarray())
