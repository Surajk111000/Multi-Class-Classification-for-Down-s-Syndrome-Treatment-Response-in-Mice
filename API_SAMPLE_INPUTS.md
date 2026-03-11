# API Sample Inputs - Ready to Use

## Quick Access
- **Swagger UI:** http://localhost:8000/docs
- **Server Status:** http://localhost:8000/health

---

## 1️⃣ SINGLE PREDICTION (`/predict`)

### Option A: Swagger UI (Easiest)
1. Open: http://localhost:8000/docs
2. Click on `/predict` endpoint
3. Click "Try it out"
4. Copy-paste the example below into the request body
5. Click "Execute"

### Option B: JSON Body
```json
{
  "features": [
    0.503, -0.196, 0.23, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006,
    -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223,
    0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129,
    0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167, 0.145, 0.176, 0.198,
    0.134, 0.156, 0.178, 0.201, 0.089, 0.112, 0.145, 0.134, 0.167, 0.189,
    0.156, 0.178, 0.145, 0.123, 0.167, 0.198, 0.156, 0.134, 0.189, 0.167,
    0.145, 0.178, 0.201, 0.156, -0.089, -0.145, -0.123, -0.087, -0.112, -0.134,
    -0.156, -0.178, -0.167, 0.234, 0.156, 0.145, 0.189
  ],
  "model_type": "svm",
  "classification_type": "binary"
}
```

**Features:** Exactly 77 values (required)  
**Model options:** `svm`, `rf`, `mlp`, `logreg`  
**Classification:** `binary` or `multiclass`

### Option C: PowerShell/cURL
```powershell
$body = @{
    features = @(0.503, -0.196, 0.23, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006, -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223, 0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129, 0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167, 0.145, 0.176, 0.198, 0.134, 0.156, 0.178, 0.201, 0.089, 0.112, 0.145, 0.134, 0.167, 0.189, 0.156, 0.178, 0.145, 0.123, 0.167, 0.198, 0.156, 0.134, 0.189, 0.167, 0.145, 0.178, 0.201, 0.156, -0.089, -0.145, -0.123, -0.087, -0.112, -0.134, -0.156, -0.178, -0.167, 0.234, 0.156, 0.145, 0.189)
    model_type = "svm"
    classification_type = "binary"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8000/predict `
  -Method POST `
  -Body $body `
  -ContentType "application/json" `
  -UseBasicParsing | Select-Object -ExpandProperty Content
```

### Expected Response:
```json
{
  "predictions": [0],
  "model_used": "svm_binary",
  "classification_type": "binary"
}
```

---

## 2️⃣ BATCH PREDICTION (`/batch_predict`)

### Option A: Swagger UI
1. Open: http://localhost:8000/docs
2. Click on `/batch_predict` endpoint
3. Click "Try it out"
4. Copy-paste the example below
5. Click "Execute"

### Option B: JSON Body (2 samples)
```json
{
  "features": [
    [
      0.503, -0.196, 0.23, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006,
      -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223,
      0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129,
      0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167, 0.145, 0.176, 0.198,
      0.134, 0.156, 0.178, 0.201, 0.089, 0.112, 0.145, 0.134, 0.167, 0.189,
      0.156, 0.178, 0.145, 0.123, 0.167, 0.198, 0.156, 0.134, 0.189, 0.167,
      0.145, 0.178, 0.201, 0.156, -0.089, -0.145, -0.123, -0.087, -0.112, -0.134,
      -0.156, -0.178, -0.167, 0.234, 0.156, 0.145, 0.189
    ],
    [
      0.412, -0.087, 0.156, -0.145, -0.098, -0.064, -0.022, -0.031, -0.041, 0.018,
      -0.089, -0.112, -0.076, -0.134, -0.098, -0.178, -0.061, 0.056, 0.142, 0.167,
      0.078, 0.134, 0.189, 0.112, 0.061, 0.089, 0.098, 0.134, 0.121, 0.092,
      0.054, 0.108, 0.119, 0.156, 0.187, 0.156, 0.129, 0.108, 0.134, 0.156,
      0.098, 0.119, 0.134, 0.156, 0.067, 0.089, 0.108, 0.098, 0.129, 0.145,
      0.119, 0.134, 0.108, 0.092, 0.129, 0.156, 0.119, 0.098, 0.145, 0.129,
      0.108, 0.134, 0.156, 0.119, -0.067, -0.108, -0.092, -0.065, -0.087, -0.101,
      -0.119, -0.134, -0.129, 0.145, 0.167, 0.156, 0.178
    ]
  ],
  "model_type": "rf",
  "classification_type": "multiclass"
}
```

**Parameters:**
- `features`: List of 77-feature vectors (can be 1 or more)
- `model_type`: `svm`, `rf`, `mlp`, `logreg`
- `classification_type`: `binary` or `multiclass`

### Expected Response:
```json
{
  "predictions": [2, 2],
  "model_used": "rf_multiclass",
  "classification_type": "multiclass"
}
```

---

## 3️⃣ CSV FILE UPLOAD (`/csv_predict`)

### CSV Format (sample_data_77_noheaders.csv)
```csv
0.503,-0.196,0.23,-0.226,-0.186,-0.107,-0.035,-0.052,-0.064,0.006,-0.132,-0.156,-0.121,-0.178,-0.146,-0.241,-0.103,0.041,0.195,0.223,0.106,0.187,0.245,0.156,0.089,0.121,0.134,0.178,0.164,0.129,0.087,0.145,0.156,0.198,0.234,0.201,0.167,0.145,0.176,0.198,0.134,0.156,0.178,0.201,0.089,0.112,0.145,0.134,0.167,0.189,0.156,0.178,0.145,0.123,0.167,0.198,0.156,0.134,0.189,0.167,0.145,0.178,0.201,0.156,-0.089,-0.145,-0.123,-0.087,-0.112,-0.134,-0.156,-0.178,-0.167,0.234,0.156,0.145,0.189
0.412,-0.087,0.156,-0.145,-0.098,-0.064,-0.022,-0.031,-0.041,0.018,-0.089,-0.112,-0.076,-0.134,-0.098,-0.178,-0.061,0.056,0.142,0.167,0.078,0.134,0.189,0.112,0.061,0.089,0.098,0.134,0.121,0.092,0.054,0.108,0.119,0.156,0.187,0.156,0.129,0.108,0.134,0.156,0.098,0.119,0.134,0.156,0.067,0.089,0.108,0.098,0.129,0.145,0.119,0.134,0.108,0.092,0.129,0.156,0.119,0.098,0.145,0.129,0.108,0.134,0.156,0.119,-0.067,-0.108,-0.092,-0.065,-0.087,-0.101,-0.119,-0.134,-0.129,0.145,0.167,0.156,0.178
```

**Important:** 
- NO headers (just raw data)
- Each row = exactly 77 comma-separated values
- One prediction per row

### PowerShell Command
```powershell
$filePath = "sample_data_77_noheaders.csv"

Invoke-WebRequest -Uri "http://localhost:8000/csv_predict?model_type=svm&classification_type=binary" `
  -Method POST `
  -Form @{file=Get-Item $filePath} `
  -UseBasicParsing | Select-Object -ExpandProperty Content
```

### Or with cURL (if available)
```bash
curl -X POST "http://localhost:8000/csv_predict?model_type=svm&classification_type=binary" \
  -F "file=@sample_data_77_noheaders.csv"
```

### Expected Response:
```json
{
  "status": "success",
  "rows_processed": 2,
  "predictions": [0, 0],
  "model_used": "svm_binary",
  "classification_type": "binary"
}
```

---

## ⚙️ Available Models & Types

### Model Types (model_type parameter):
| Model | Type | Best For |
|-------|------|----------|
| `svm` | Support Vector Machine | Fast, accurate |
| `rf` | Random Forest | Robust, handles outliers |
| `mlp` | Neural Network | Complex patterns |
| `logreg` | Logistic Regression | Baseline, interpretable |

### Classification Types (classification_type parameter):
| Type | Classes | Output |
|------|---------|--------|
| `binary` | 2 classes | Control vs Treated |
| `multiclass` | 4 classes | C/S, C/C, T/S, T/C |

---

## 🧪 Quick Test Commands

### Python Script
```python
python test_api.py  # Runs all 5 tests
```

### Generate Sample
```python
python generate_sample.py  # Shows formatted JSON examples
```

### Health Check
Open in browser: http://localhost:8000/health

---

## 📋 Important Notes

⚠️ **ALWAYS use 77 features** - Not 37, not 75, exactly **77**

✅ **Column breakdown:**
- Columns 1-75: Protein measurements
- Columns 76-77: Metadata (genotype, treatment)

✅ **Predictions:**
- Binary (0 or 1): Control vs Treated
- Multiclass (0-3): Different treatment combinations

✅ **Model Accuracy:**
- Binary: ~96.72%
- Multiclass: ~97.64%

---

## 🔗 API Endpoints Summary

| Endpoint | Method | Purpose | Input |
|----------|--------|---------|-------|
| `/` | GET | API info | None |
| `/health` | GET | Server status | None |
| `/predict` | POST | Single sample | 77 features |
| `/batch_predict` | POST | Multiple samples | N × 77 features |
| `/csv_predict` | POST | CSV file | File upload |
| `/models/available` | GET | List models | None |
| `/docs` | GET | Swagger UI | None |

---

## 💾 Files Available

| File | Purpose |
|------|---------|
| `sample_data_77_noheaders.csv` | Ready-to-use CSV for batch testing |
| `generate_sample.py` | Generates valid JSON examples |
| `test_api.py` | Comprehensive test suite |

---

**Ready to test? Start with Swagger UI → http://localhost:8000/docs** 🚀
