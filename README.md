# Resume Matching System

This project is designed to automatically match resumes with job descriptions using NLP and advanced machine learning techniques. The system can be deployed both locally and on AWS, allowing HR directors to quickly and easily select the best applicants' resumes for job interviews.

## Project Structure

\```
resume-matching/
├── data/
│   ├── resumes/
│   └── jobs/
├── scripts/
│   ├── text_extraction.py
│   ├── text_preprocessing.py
│   ├── feature_extraction.py
│   ├── model_training.py
│   └── app.py
├── models/
│   └── best_model.pkl
├── intermediate_data/
├── templates/
│   └── index.html
├── static/
│   ├── styles.css
│   └── script.js
├── Dockerfile
├── requirements.txt
└── README.md
\```

## Prerequisites

1. **Python 3.8+**
2. **pip**
3. **Docker**
4. **AWS CLI (for deployment on AWS)**

## Setting Up the Project

### Step 1: Create Directories and Files

\```bash
# Create project directories
mkdir -p resume-matching/{data/{resumes,jobs},scripts,models,intermediate_data,templates,static}

```
# Create empty files
touch resume-matching/requirements.txt
touch resume-matching/Dockerfile
touch resume-matching/templates/index.html
touch resume-matching/static/styles.css
touch resume-matching/static/script.js
touch resume-matching/scripts/{text_extraction.py,text_preprocessing.py,feature_extraction.py,model_training.py,app.py}
touch resume-matching/README.md
```

### Step 2: Install Dependencies

Create a virtual environment and install dependencies.

\```bash
cd resume-matching
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
\```

### Step 3: Extract Text from PDFs

Run the script to extract text from resumes and job descriptions.

\```bash
python scripts/text_extraction.py
\```

### Step 4: Preprocess Text

Run the script to preprocess the extracted text.

\```bash
python scripts/text_preprocessing.py
\```

### Step 5: Feature Extraction

Run the script to extract features using TF-IDF.

\```bash
python scripts/feature_extraction.py
\```

### Step 6: Model Training

Run the script to train the machine learning model.

\```bash
python scripts/model_training.py
\```

### Step 7: Test the Flask App Locally

1. **Create and activate a virtual environment:**

    \```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    \```

2. **Run the Flask app:**

    \```bash
    python scripts/app.py
    \```

3. **Open your web browser and go to:**

    \```plaintext
    http://localhost:5000
    \```

### Step 8: Build and Run Docker Container

1. **Build the Docker image:**

    \```bash
    docker build -t resume-matching .
    \```

2. **Run the Docker container:**

    \```bash
    docker run -p 5000:5000 resume-matching
    \```

3. **Check the Docker logs for any errors:**

    \```bash
    docker logs <container_id>
    \```

4. **Open your web browser and go to:**

    \```plaintext
    http://localhost:5000
    \```

### Step 9: Deploy on AWS

#### Prerequisites

1. **AWS CLI:** Install and configure the AWS CLI.
2. **ECR Repository:** Create an ECR repository to store the Docker image.

#### Steps

1. **Tag the Docker image:**

    \```bash
    docker tag resume-matching:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/resume-matching:latest
    \```

2. **Login to ECR:**

    \```bash
    aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
    \```

3. **Push the Docker image to ECR:**

    \```bash
    docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/resume-matching:latest
    \```

4. **Create an ECS Cluster and Task Definition:**
   Follow the AWS ECS documentation to create an ECS cluster and task definition to run your Docker container.

5. **Run the Task:**
   Use the ECS console to run the task on your cluster.

### Step 10: Monitoring

Use CloudWatch to monitor your application logs and performance. Set up alarms and metrics as needed.

### Step 11: Cleanup

When you're done, clean up your resources to avoid unnecessary charges.

\```bash
# Stop the Docker container
docker stop <container_id>

# Remove the Docker container
docker rm <container_id>

# Remove the Docker image
docker rmi resume-matching

# Deactivate the virtual environment
deactivate
\```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

    
