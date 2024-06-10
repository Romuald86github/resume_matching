from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import os

def calculate_similarity(resume_tfidf, job_tfidf):
    similarity_scores = []
    for job_vec in job_tfidf:
        job_scores = cosine_similarity(resume_tfidf, job_vec.reshape(1, -1)).flatten()
        similarity_scores.append(job_scores)
    return np.array(similarity_scores)

if __name__ == "__main__":
    resume_tfidf = np.load('intermediate_data/resume_tfidf.npy')
    job_tfidf = np.load('intermediate_data/job_tfidf.npy')

    similarity_scores = calculate_similarity(resume_tfidf, job_tfidf)
    np.save('intermediate_data/similarity_scores.npy', similarity_scores)

    # Create positive examples (matching pairs)
    X_pos = similarity_scores.flatten().reshape(-1, 1)
    y_pos = np.ones(len(X_pos))

    # Create negative examples (non-matching pairs)
    job_tfidf_shuffled = np.random.permutation(job_tfidf)
    similarity_scores_neg = calculate_similarity(resume_tfidf, job_tfidf_shuffled)
    X_neg = similarity_scores_neg.flatten().reshape(-1, 1)
    y_neg = np.zeros(len(X_neg))

    # Combine positive and negative examples
    X = np.vstack((X_pos, X_neg))
    y = np.hstack((y_pos, y_neg))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "Logistic Regression": LogisticRegression(),
        "SVM": SVC(),
        "Random Forest": RandomForestClassifier()
    }

    best_model = None
    best_accuracy = 0

    for model_name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"{model_name} Accuracy: {accuracy}")
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model

    if not os.path.exists('models'):
        os.makedirs('models')
    
    import pickle
    with open('models/best_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
