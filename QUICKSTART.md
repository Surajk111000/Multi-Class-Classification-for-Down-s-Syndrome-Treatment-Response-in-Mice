# Quick Start Guide

## Get Started in 5 Minutes

### 1. Clone Repository
```bash
git clone https://github.com/Surajk111000/Multi-Class-Classification-for-Down-s-Syndrome-Treatment-Response-in-Mice.git
cd ml-fastapi-project
```

### 2. Setup Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train Models (Optional - if models don't exist)
```bash
python -m app.train
```
This will download datasets and train all models (may take 5-10 minutes).

### 5. Start API Server
```bash
uvicorn app.main:app --reload
```

### 6. Test the API
Open your browser and go to: **http://localhost:8000/docs**

You'll see the interactive Swagger UI with all available endpoints.

## Example Requests

### Test with Single Prediction
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
    "model_type": "svm",
    "classification_type": "binary"
  }'
```

### Test with CSV Upload
```bash
curl -X POST "http://localhost:8000/csv_upload" \
  -F "file=@data.csv" \
  -F "model_type=svm" \
  -F "classification_type=binary"
```

## Docker Deployment

### Build and Run
```bash
docker-compose up --build
```

API will be available at: **http://localhost:8000**

## Available Models

| Type | Binary | Multi-class |
|------|--------|------------|
| SVM | `svm_binary` | `svm_4class` |
| Random Forest | `rf_binary` | `rf_4class` |
| Neural Network | `mlp_binary` | `mlp_4class` |
| Logistic Regression | `logreg_binary` | `logreg_4class` |

## Model Performance

- **Binary Classification**: 88.4% accuracy (Neural Network)
- **Multi-class Classification**: 74.2% accuracy (SVM)

## Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/predict` | POST | Single prediction |
| `/batch_predict` | POST | Batch predictions |
| `/csv_upload` | POST | CSV file upload |
| `/models/available` | GET | List of available models |
| `/docs` | GET | Interactive API docs |
| `/redoc` | GET | ReDoc documentation |

## Troubleshooting

### Port Already in Use
```bash
# Use different port
uvicorn app.main:app --port 8001
```

### Models Not Found
```bash
# Train models first
python -m app.train
```

### Permission Denied (Linux/Mac)
```bash
# Make scripts executable
chmod +x run.sh
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [API Documentation](http://localhost:8000/docs) for all endpoints
- Explore model performance in the Results section of README

---

For more information, see the full [README.md](README.md)
