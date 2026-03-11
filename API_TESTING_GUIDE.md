# Testing the API with Sample Data

## Sample CSV File

**File:** `sample_data_proteins.csv`

Contains 6 sample rows with 37 protein expression features (PCA-reduced from 77 original proteins).

---

## 🧪 Test Method 1: Using Swagger UI (EASIEST)

1. **Open in browser:**
   ```
   http://localhost:8000/docs
   ```

2. **Click on `/predict` endpoint** (POST)

3. **Click "Try it out"**

4. **Enter JSON:**
   ```json
   {
     "features": [0.503, -0.196, 0.230, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006, -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223, 0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129, 0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167],
     "model_type": "svm",
     "classification_type": "binary"
   }
   ```

5. **Click "Execute"**

6. **See Response:**
   ```json
   {
     "predictions": [1],
     "model_used": "svm_binary",
     "classification_type": "binary",
     "confidence": [[0.25, 0.75]]
   }
   ```

---

## 🧪 Test Method 2: Using Python (RECOMMENDED FOR BATCH)

### Single Prediction (`/predict`):

```python
import requests
import json

# Single sample
features = [0.503, -0.196, 0.230, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006, 
            -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223, 
            0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129, 
            0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167]

payload = {
    "features": features,
    "model_type": "svm",
    "classification_type": "binary"
}

response = requests.post('http://localhost:8000/predict', json=payload)
print(json.dumps(response.json(), indent=2))
```

**Output:**
```json
{
  "predictions": [1],
  "model_used": "svm_binary",
  "classification_type": "binary",
  "confidence": [[0.25, 0.75]]
}
```

### Batch Prediction (`/batch_predict`):

```python
import requests
import json

# Multiple samples
features_list = [
    [0.503, -0.196, 0.230, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006, 
     -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223, 
     0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129, 
     0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167],
    
    [0.412, -0.087, 0.156, -0.145, -0.098, -0.064, -0.022, -0.031, -0.041, 0.018, 
     -0.089, -0.112, -0.076, -0.134, -0.098, -0.178, -0.061, 0.056, 0.142, 0.167, 
     0.078, 0.134, 0.189, 0.112, 0.061, 0.089, 0.098, 0.134, 0.121, 0.092, 
     0.054, 0.108, 0.119, 0.156, 0.187, 0.156, 0.129],
    
    [0.621, -0.312, 0.345, -0.289, -0.234, -0.145, -0.056, -0.078, -0.089, 0.012, 
     -0.167, -0.198, -0.156, -0.212, -0.178, -0.289, -0.134, 0.031, 0.234, 0.267, 
     0.145, 0.245, 0.301, 0.189, 0.112, 0.156, 0.167, 0.212, 0.198, 0.167, 
     0.112, 0.178, 0.189, 0.234, 0.278, 0.245, 0.203]
]

payload = {
    "features": features_list,
    "model_type": "svm",
    "classification_type": "binary"
}

response = requests.post('http://localhost:8000/batch_predict', json=payload)
print(json.dumps(response.json(), indent=2))
```

**Output:**
```json
{
  "predictions": [1, 0, 1],
  "model_used": "svm_binary",
  "classification_type": "binary",
  "confidence": [[0.25, 0.75], [0.65, 0.35], [0.20, 0.80]]
}
```

---

## 🧪 Test Method 3: Using cURL (TERMINAL)

### Single Prediction:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [0.503, -0.196, 0.230, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006, -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223, 0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129, 0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167],
    "model_type": "svm",
    "classification_type": "binary"
  }'
```

### Batch Prediction:

```bash
curl -X POST "http://localhost:8000/batch_predict" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      [0.503, -0.196, 0.230, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006, -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223, 0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129, 0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167],
      [0.412, -0.087, 0.156, -0.145, -0.098, -0.064, -0.022, -0.031, -0.041, 0.018, -0.089, -0.112, -0.076, -0.134, -0.098, -0.178, -0.061, 0.056, 0.142, 0.167, 0.078, 0.134, 0.189, 0.112, 0.061, 0.089, 0.098, 0.134, 0.121, 0.092, 0.054, 0.108, 0.119, 0.156, 0.187, 0.156, 0.129],
      [0.621, -0.312, 0.345, -0.289, -0.234, -0.145, -0.056, -0.078, -0.089, 0.012, -0.167, -0.198, -0.156, -0.212, -0.178, -0.289, -0.134, 0.031, 0.234, 0.267, 0.145, 0.245, 0.301, 0.189, 0.112, 0.156, 0.167, 0.212, 0.198, 0.167, 0.112, 0.178, 0.189, 0.234, 0.278, 0.245, 0.203]
    ],
    "model_type": "svm",
    "classification_type": "binary"
  }'
```

---

## 📊 Testing Different Models

### Try Different Model Types:

Change `"model_type"` to test:
- `"svm"` → Support Vector Machine (best for this data)
- `"rf"` → Random Forest
- `"mlp"` → Neural Network (Multi-Layer Perceptron)
- `"logreg"` → Logistic Regression

### Example with Random Forest:

```python
payload = {
    "features": [0.503, -0.196, 0.230, ...],
    "model_type": "rf",           # Changed
    "classification_type": "binary"
}
response = requests.post('http://localhost:8000/predict', json=payload)
```

---

## 🎯 Testing Classification Types

### Binary Classification (Best Accuracy: 96.72%):

```json
{
  "features": [...],
  "model_type": "svm",
  "classification_type": "binary"
}
```

**Output:** Predictions will be `[0]` or `[1]` (2 classes)

### Multi-class Classification (Best Accuracy: 97.64%):

```json
{
  "features": [...],
  "model_type": "svm",
  "classification_type": "multiclass"
}
```

**Output:** Predictions will be `[0]`, `[1]`, `[2]`, or `[3]` (4 classes)

---

## 📝 Full Testing Script (Python)

```python
#!/usr/bin/env python3
"""Complete API testing script"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

# Sample data (37 PCA components)
SAMPLE_FEATURES = [
    [0.503, -0.196, 0.230, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006, 
     -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223, 
     0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129, 
     0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167],
    
    [0.412, -0.087, 0.156, -0.145, -0.098, -0.064, -0.022, -0.031, -0.041, 0.018, 
     -0.089, -0.112, -0.076, -0.134, -0.098, -0.178, -0.061, 0.056, 0.142, 0.167, 
     0.078, 0.134, 0.189, 0.112, 0.061, 0.089, 0.098, 0.134, 0.121, 0.092, 
     0.054, 0.108, 0.119, 0.156, 0.187, 0.156, 0.129],
]

def test_health():
    """Test health endpoint"""
    print("\n1️⃣  Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_single_prediction():
    """Test single prediction"""
    print("2️⃣  Testing /predict endpoint (Single)...")
    payload = {
        "features": SAMPLE_FEATURES[0],
        "model_type": "svm",
        "classification_type": "binary"
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_batch_prediction():
    """Test batch prediction"""
    print("3️⃣  Testing /batch_predict endpoint (Multiple)...")
    payload = {
        "features": SAMPLE_FEATURES,
        "model_type": "svm",
        "classification_type": "binary"
    }
    response = requests.post(f"{BASE_URL}/batch_predict", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_multiclass():
    """Test multi-class classification"""
    print("4️⃣  Testing Multi-class Classification...")
    payload = {
        "features": SAMPLE_FEATURES[0],
        "model_type": "rf",
        "classification_type": "multiclass"
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_models():
    """Test available models"""
    print("5️⃣  Testing /models/available endpoint...")
    response = requests.get(f"{BASE_URL}/models/available")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 MICE PROTEIN CLASSIFICATION API - TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health),
        ("Single Prediction", test_single_prediction),
        ("Batch Prediction", test_batch_prediction),
        ("Multi-class Classification", test_multiclass),
        ("Available Models", test_models),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed: {str(e)}\n")
            results[test_name] = False
    
    # Summary
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

**Save as:** `test_api.py`

**Run:**
```bash
python test_api.py
```

---

## 📋 Sample Data Explanation

**File:** `sample_data_proteins.csv`

- **6 rows:** 6 mouse samples
- **37 columns:** 37 PCA-reduced protein expression features
- **Values:** Normalized measurements (-1 to +1)

**To use with real data:**
1. Get original 77 protein expressions
2. They automatically get reduced to 37 via PCA in the API
3. Or use the sample data directly

---

## ✅ Quick Test Checklist

- [ ] Server running on port 8000
- [ ] Health endpoint returns 200
- [ ] Single prediction works
- [ ] Batch prediction works
- [ ] Different models tested (svm, rf, mlp, logreg)
- [ ] Binary classification works
- [ ] Multi-class classification works

---

## 🎯 Expected Results

### Binary Classification (SVM):
```
Input: 37 features
Output: [0] or [1]  (Genotype: Control or Trisomy)
Confidence: ~96.72% accuracy
```

### Multi-class Classification (SVM):
```
Input: 37 features
Output: [0], [1], [2], or [3]  (Treatment/Behavior: 4 classes)
Confidence: ~97.64% accuracy
```

---

**All sample data is ready in `sample_data_proteins.csv`!** ✨
