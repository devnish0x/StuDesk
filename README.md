# Campus Complaint Intelligence and Routing Hub

An AI-powered campus complaint management system that classifies student complaints into the correct category and routes them to the appropriate department using Natural Language Processing, FastAPI, Docker, Kubernetes, and basic MLOps practices.

## Project overview

This project is designed to help educational institutions handle student complaints more efficiently. Students can submit complaints through a simple frontend interface, and the system automatically predicts the complaint category and routes it to the relevant department.

## Features

- Multi-class complaint classification using TF-IDF and Logistic Regression
- Automatic routing to the correct department
- FastAPI backend with REST API endpoints
- Frontend interface for complaint submission
- Dockerized deployment
- Kubernetes deployment using Docker Desktop Kubernetes
- Basic MLOps features:
  - Prediction logging
  - Feedback logging
  - Model version tracking

## Complaint categories

The system classifies complaints into the following categories:

- Hostel
- Transport
- Academics
- Canteen
- Facilities
- Administration
- IT Support

## Tech stack

- Python
- FastAPI
- Scikit-learn
- Pandas
- Joblib
- HTML, CSS, JavaScript
- Docker
- Kubernetes
- GitHub

## Project structure

```text
campus-complaint-hub/
├── api/
│   ├── main.py
│   ├── routing.py
│   └── schemas.py
├── frontend/
│   └── index.html
├── deployment/
│   ├── deployment.yaml
│   └── service.yaml
├── data/
│   └── complaints_dataset_cleaned.csv
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── model.pkl
├── vectorizer.pkl
├── train_model.py
├── test_model.py
├── split_dataset.py
├── check_dataset.py
└── README.md
```

## Machine learning workflow

1. Complaint dataset collection and balancing
2. Data cleaning and validation
3. TF-IDF feature extraction
4. Logistic Regression model training
5. Model evaluation
6. Model persistence using `model.pkl` and `vectorizer.pkl`
7. Deployment with FastAPI

## API endpoints

### `GET /`
Returns a basic API status message.

### `GET /health`
Returns health status and model loading information.

### `POST /predict`
Predicts complaint category and routed department.

Example request body:

```json
{
  "complaint_text": "The hostel bathroom water supply is not working properly"
}
```

### `POST /feedback`
Stores user/admin feedback for predictions.

Example request body:

```json
{
  "complaint_text": "The hostel bathroom water supply is not working properly",
  "predicted_category": "Hostel",
  "correct_category": "Hostel",
  "feedback": "Correct prediction"
}
```

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/campus-complaint-hub.git
cd campus-complaint-hub
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI server

```bash
uvicorn api.main:app --reload
```

### 5. Open in browser

- API root: `http://127.0.0.1:8000/`
- Swagger docs: `http://127.0.0.1:8000/docs`

## Docker setup

### Build Docker image

```bash
docker build -t campus-complaint-hub:v1 .
```

### Run Docker container

```bash
docker run -d -p 8000:8000 --name campus-complaint-app campus-complaint-hub:v1
```

## Kubernetes deployment

This project was deployed using **Docker Desktop Kubernetes**.

### Apply Kubernetes manifests

```bash
kubectl apply -f deployment/deployment.yaml
kubectl apply -f deployment/service.yaml
```

### Check resources

```bash
kubectl get pods
kubectl get svc
```

### Access the application

- API: `http://localhost:30080/`
- Swagger docs: `http://localhost:30080/docs`

## MLOps components

This project includes a basic MLOps workflow:

- Model version tracking using a version tag
- Prediction logging to CSV
- Feedback collection for future retraining
- Containerized deployment using Docker
- Kubernetes-based orchestration

## Future enhancements

- Real-time database integration
- Admin dashboard with analytics
- Authentication and role-based access
- Cloud deployment
- Automated retraining pipeline
- Monitoring with Prometheus and Grafana

## Author

**Premkumar S**  
M.Tech Data Science  
Rajalakshmi Engineering College

## License

This project is developed for academic and educational purposes.
