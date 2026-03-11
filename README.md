# Mice Protein Expression Classification API

Multi-Class Classification for Down's Syndrome Treatment Response in Mice

## Overview

This FastAPI-based ML inference interface supports CSV batch uploads for mice gene-expression data with automated preprocessing (feature validation, scaling, and PCA reduction to 37 features).

The project integrates and evaluates SVM, Neural Network, Random Forest, and Logistic Regression models in a unified prediction pipeline, enforcing feature-schema alignment and achieving:
- **88.4% accuracy** for binary classification
- **74.2% accuracy** for multi-class classification

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── model_loader.py      # Model loading utilities
│   ├── predict.py           # Prediction functions
│   ├── schemas.py           # Pydantic models
│   ├── train.py             # Training pipeline
│   └── __pycache__/
├── models/
│   └── saved_models/        # Trained model files (.pkl)
├── tests/
├── Procfile                 # Heroku deployment
├── README.md
├── requirements.txt
└── venv/
```

## Installation

### Prerequisites
- Python 3.8+
- pip or conda
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Surajk111000/Multi-Class-Classification-for-Down-s-Syndrome-Treatment-Response-in-Mice.git
cd ml-fastapi-project
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Training

### Prepare Models

To train the models from scratch:

```bash
python -m app.train
```

This will:
1. Download training data from IIT Bombay's servers
2. Preprocess and impute missing values
3. Apply PCA dimensionality reduction (77 → 37 features)
4. Train 4 models (SVM, MLP, Random Forest, Logistic Regression)
5. Optimize hyperparameters using GridSearchCV
6. Save models as pickle files in `models/saved_models/`
7. Evaluate on test dataset

## Usage

### Start the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### API Endpoints

#### 1. Health Check
```bash
GET /health
```
Response:
```json
{
  "status": "healthy",
  "models_loaded": ["logreg_binary", "mlp_binary", "svm_binary", "rf_binary", "logreg_4class", "mlp_4class", "svm_4class", "rf_4class"],
  "pca_available": true
}
```

#### 2. Single Prediction
```bash
POST /predict
Content-Type: application/json

{
  "features": [1.0, 2.0, 3.0, ..., 77.0],
  "model_type": "svm",
  "classification_type": "binary"
}
```

Response:
```json
{
  "predictions": [1],
  "model_used": "svm_binary",
  "classification_type": "binary",
  "confidence": [[0.2, 0.8]]
}
```

#### 3. Batch Predictions
```bash
POST /batch_predict
Content-Type: application/json

{
  "features": [
    [1.0, 2.0, 3.0, ..., 77.0],
    [4.0, 5.0, 6.0, ..., 77.0]
  ],
  "model_type": "rf",
  "classification_type": "multiclass"
}
```

#### 4. CSV Upload for Batch Predictions
```bash
POST /csv_upload
Content-Type: multipart/form-data

file: <your_csv_file>
model_type: svm
classification_type: binary
```

CSV Format:
- Each row contains feature values (protein expression levels)
- First row can be headers (will be auto-detected)
- Last two columns are skipped if they appear to be target values
- Supports 77 protein expression features

Example CSV:
```
DYRK1A_N,ITSN1_N,CRMP3_N,BDNF_N,...
1.0,2.0,3.0,4.0,...
5.0,6.0,7.0,8.0,...
```

#### 5. Available Models
```bash
GET /models/available
```

Response:
```json
{
  "available_models": [
    "logreg_binary", "mlp_binary", "svm_binary", "rf_binary",
    "logreg_4class", "mlp_4class", "svm_4class", "rf_4class"
  ],
  "model_types": ["svm", "rf", "mlp", "logreg"],
  "classification_types": ["binary", "multiclass"]
}
```

### Model Types

- **svm**: Support Vector Machine
- **rf**: Random Forest
- **mlp**: Multi-Layer Perceptron (Neural Network)
- **logreg**: Logistic Regression

### Classification Types

- **binary**: Binary classification (2 classes)
- **multiclass**: Multi-class classification (4 classes)

## Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Model Performance

### Binary Classification (Genotype)
| Model | Cross-Validation Score | Test Accuracy |
|-------|------------------------|--------------|
| Logistic Regression | 77.0% | - |
| Neural Network | - | **88.44%** ⭐ |
| SVM | 77.0% | - |
| Random Forest | - | - |

### Multi-Class Classification (Treatment/Behaviour)
| Model | Cross-Validation Score | Test Accuracy |
|-------|------------------------|--------------|
| Logistic Regression | 74.2% | - |
| Neural Network | 73.21% | - |
| SVM | - | **74.22%** ⭐ |
| Random Forest | 73.21% | - |

## Data Preprocessing

1. **Missing Value Imputation**: Mean imputation
2. **Feature Correlation**: Removed highly correlated features:
   - ITSN1_N (correlated with DYRK1A_N)
   - NR2A_N (correlated with NR1N)
   - pBRAF_N (correlated with pAKT_N)
   - ERK_N (correlated with ELK_N)
3. **Dimensionality Reduction**: PCA (77 → 37 features)
4. **Label Encoding**: Categorical targets converted to numeric

## Dataset Information

- **Training Samples**: 552 mice
- **Test Samples**: 350 mice
- **Original Features**: 77 protein expression levels
- **Reduced Features**: 37 (via PCA)
- **Binary Target**: Genotype (Control/Trisomy)
- **Multi-class Target**: Treatment/Behavior (4 classes)

### Source
- Training dataset: https://www.ee.iitb.ac.in/~asethi/Dump/MouseTrain.csv
- Test dataset: https://www.ee.iitb.ac.in/~asethi/Dump/MouseTest.csv

## Deployment

### Heroku Deployment

1. **Prerequisites**: Heroku CLI installed

2. **Deploy**:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

3. **Visit your app**:
```
https://your-app-name.herokuapp.com
```

### Docker Deployment

```bash
docker build -t mice-prediction .
docker run -p 8000:8000 mice-prediction
```

## Project Details

**Course**: Down's Syndrome Treatment Response Analysis  
**Institution**: IIT Bombay, Department of Electrical Engineering  
**Duration**: Jan'23 – Jun'23  
**Guide**: Prof. Amit Sethi  
**Developer**: Suraj  

## Technologies Used

- **FastAPI**: Modern Python web framework
- **Scikit-learn**: ML algorithms and preprocessing
- **NumPy/Pandas**: Data manipulation
- **Scikit-learn**: Model training and evaluation
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

## Key Features

✅ Multiple ML algorithms (SVM, RF, MLP, Logistic Regression)  
✅ Binary and Multi-class classification  
✅ CSV batch upload support  
✅ Automated feature preprocessing (PCA reduction)  
✅ Feature schema validation  
✅ High accuracy (88.4% binary, 74.2% multi-class)  
✅ Interactive API documentation  
✅ CORS enabled  
✅ Production-ready  

## Testing

Run tests:
```bash
pytest tests/
```

## Troubleshooting

### Models Not Loaded
```
Error: Model not found or not loaded
```
**Solution**: Ensure you've trained the models first by running `python -m app.train`

### PCA Not Available
**Solution**: The PCA transformer must be saved during training. Re-run the training script.

### CORS Issues
The API has CORS enabled for all origins. Adjust in `app/main.py` if needed.

## References

1. [Feature Importance Calculation](https://machinelearningmastery.com/calculate-feature-importance-with-python/)
2. [Scikit-learn Documentation](https://scikit-learn.org/stable/modules/classes.html)
3. [FastAPI Documentation](https://fastapi.tiangolo.com/)
4. [PCA and Dimensionality Reduction](https://www.youtube.com/watch?v=gJo0uNL-5Qw)

## License

This project is part of academic research at IIT Bombay.

## Contact

- **Developer**: Suraj
- **GitHub**: https://github.com/Surajk111000

---

**Last Updated**: March 2026  
**Version**: 1.0.0
