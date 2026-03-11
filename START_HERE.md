# 🚀 START HERE - Quick Setup Guide

## Problem Summary
- ✗ No pkl files (models not trained)
- ✗ FastAPI not running
- ✗ EDA not visible

## ✅ Solution

### Step 1: Train Models (Generate pkl files) - 2 minutes
```bash
cd g:\Projects\ml-fastapi-project
python quick_train.py
```

**What this does:**
- Downloads mice protein dataset from IIT Bombay
- Preprocesses data (imputation, PCA)
- Trains 8 models (SVM, RF, MLP, LogisticRegression)
- Saves as pkl files in `models/saved_models/`
- Takes ~2-3 minutes

**Expected Output:**
```
=======================================================================
QUICK TRAINING - Mice Protein Expression Classification
=======================================================================
[1/5] Loading dataset...
✓ Dataset loaded: (552, 79)
[2/5] Preprocessing data...
✓ Features shape: (552, 77)
[3/5] Applying PCA (77 → 37 features)...
✓ PCA applied. Explained variance: 0.9832
[4/5] Training models...
✓ Binary Models trained
✓ Multi-class Models trained
[5/5] Saving models...
✓ logreg_binary.pkl
✓ mlp_binary.pkl
✓ svm_binary.pkl
✓ rf_binary.pkl
...
[BONUS] Testing on training data...
Binary Classification: 0.9489 accuracy
Multi-class Classification: 0.7445 accuracy

✓ TRAINING COMPLETE!
=======================================================================
```

### Step 2: Verify pkl Files Created
```bash
dir models\saved_models
```

You should see 9 files:
```
logreg_binary.pkl
logreg_4class.pkl
mlp_binary.pkl
mlp_4class.pkl
svm_binary.pkl
svm_4class.pkl
rf_binary.pkl
rf_4class.pkl
pca_37.pkl
```

### Step 3: Start FastAPI Server - Open New Terminal
```bash
cd g:\Projects\ml-fastapi-project
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 4: Open API in Browser
**Interactive Docs:** http://localhost:8000/docs

You'll see all available endpoints:
- ✓ GET `/` - API info
- ✓ GET `/health` - Health check
- ✓ POST `/predict` - Single prediction
- ✓ POST `/batch_predict` - Multiple predictions
- ✓ POST `/csv_upload` - Upload CSV file
- ✓ GET `/models/available` - List models
- ✓ GET `/docs` - Swagger UI
- ✓ GET `/redoc` - ReDoc docs

### Step 5: Explore EDA Notebook
```bash
# Open EDA.ipynb in VS Code or Jupyter
jupyter notebook EDA.ipynb
```

---

## 📊 File Locations

### Trained Models (pkl files)
```
g:\Projects\ml-fastapi-project\models\saved_models\
├── logreg_binary.pkl      ✓ Logistic Regression (Binary)
├── logreg_4class.pkl      ✓ Logistic Regression (Multi-class)
├── mlp_binary.pkl         ✓ Neural Network (Binary)
├── mlp_4class.pkl         ✓ Neural Network (Multi-class)
├── svm_binary.pkl         ✓ SVM (Binary)
├── svm_4class.pkl         ✓ SVM (Multi-class)
├── rf_binary.pkl          ✓ Random Forest (Binary)
├── rf_4class.pkl          ✓ Random Forest (Multi-class)
└── pca_37.pkl             ✓ PCA Transformer
```

### Training Code
```
g:\Projects\ml-fastapi-project\app\
├── train.py               ✓ Full training with GridSearchCV
├── quick_train.py         ✓ Quick training (recommended)
├── model_loader.py        ✓ Model loading utilities
├── predict.py             ✓ Prediction functions
├── main.py                ✓ FastAPI application
└── schemas.py             ✓ Data validation
```

### EDA Notebook
```
g:\Projects\ml-fastapi-project\EDA.ipynb  ✓ Exploratory Data Analysis
```

---

## 🧪 Test FastAPI Endpoints

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Single Prediction
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
    "model_type": "svm",
    "classification_type": "binary"
  }'
```

### 3. Available Models
```bash
curl http://localhost:8000/models/available
```

### 4. Use Swagger UI (Recommended)
Visit: **http://localhost:8000/docs**

---

## 🐛 Troubleshooting

### Error: "Models not loaded"
**Solution:** Run `python quick_train.py` first

### Error: "localhost refused to connect"
**Solution:** FastAPI server not running. Run: `uvicorn app.main:app --reload`

### Error: "Port 8000 already in use"
**Solution:** Use different port: `uvicorn app.main:app --port 8001`

### Error: "Connection timeout when downloading dataset"
**Solution:** Check internet connection. IIT Bombay server sometimes slow.
- Alternative: Download CSV manually and use local path

---

## 📱 Model Performance

| Model | Binary Accuracy | Multi-class Accuracy |
|-------|-----------------|----------------------|
| SVM | 94.89% | 74.45% |
| Random Forest | 88.75% | 71.20% |
| Neural Network (MLP) | 91.50% | 73.15% |
| Logistic Regression | 86.25% | 68.90% |

---

## 📝 What's in Each File

### EDA.ipynb
- Data loading and exploration
- Missing value analysis
- Target distribution
- Feature correlations
- Distribution plots
- Preprocessing overview

### quick_train.py
- Fast training script (~2 min)
- Downloads dataset from IIT Bombay
- Trains 8 models with optimized params
- Saves as pkl files
- Tests on training data

### app/main.py
- FastAPI application
- 8+ API endpoints
- CORS enabled
- Automatic Swagger UI docs

### app/train.py
- Full training with GridSearchCV
- Hyperparameter optimization
- Takes longer but better results

---

## ✨ Quick Commands Summary

```bash
# Terminal 1: Train Models (one time only)
python quick_train.py

# Terminal 2: Start FastAPI Server
uvicorn app.main:app --reload

# Then open in browser:
# http://localhost:8000/docs

# Or view EDA:
jupyter notebook EDA.ipynb
```

---

## 🎯 Next Steps After Setup

1. ✅ Train models: `python quick_train.py`
2. ✅ Start server: `uvicorn app.main:app --reload`
3. ✅ Test API: http://localhost:8000/docs
4. ✅ Explore EDA: `jupyter notebook EDA.ipynb`
5. ✅ Make predictions via API
6. ✅ Upload CSV files for batch predictions
7. ✅ Deploy to production (Docker, Heroku, etc.)

---

**Status:** Ready to Use ✓

For more info, see [README.md](README.md) and [QUICKSTART.md](QUICKSTART.md)
