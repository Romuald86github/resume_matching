import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_file(file_path):
    text = ""
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.txt'):
        with open(file_path, 'r') as file:
            text = file.read()
    return text

def extract_all_texts(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf') or filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            text = extract_text_from_file(file_path)
            texts.append(text)
    return texts

if __name__ == "__main__":
    resume_texts = extract_all_texts('../data/resumes')
    job_texts = extract_all_texts('../data/jobs')

    with open('../intermediate_data/resume_texts.txt', 'w') as f:
        for text in resume_texts:
            f.write("%s\n" % text)

    with open('../intermediate_data/job_texts.txt', 'w') as f:
        for text in job_texts:
            f.write("%s\n" % text)
