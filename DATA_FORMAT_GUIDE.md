# ✅ API Data Format Guide - **77 Raw Features Required**

## Critical Information

**The API expects 77 RAW PROTEIN FEATURES** (not 37 PCA-reduced features)

The API automatically handles:
1. ✅ Missing value imputation
2. ✅ PCA dimensionality reduction (77 → 37)
3. ✅ Model prediction

---

## Input Format

### Required Features: **77 Protein Measurements**

```json
{
  "features": [
    value1, value2, value3, ..., value77
  ],
  "model_type": "svm",
  "classification_type": "binary"
}
```

### The 77 Features (in order):

| # | Feature | # | Feature | # | Feature |
|---|---------|---|---------|---|---------|
| 1 | DYRK1A_N | 30 | pC3_c | 59 | pTau217_N |
| 2 | ITSN1_N | 31 | RasGRF1_N | 60 | pTau181c_N |
| 3 | CRMP3_N | 32 | ERK_N | 61 | pTau217c_N |
| 4 | CRMP5_N | 33 | pERK_N | 62 | APP_N |
| 5 | Calcineurin_N | 34 | MeCP2_N | 63 | pAPP_c |
| 6 | REST_N | 35 | pMeCP2_N | 64 | Cathepsin_N |
| 7 | NR1_N | 36 | MeCP2_c | 65 | BACE_N |
| 8 | NR2A_N | 37 | pMeCP2_c | 66 | pBADc_N |
| 9 | NR2B_N | 38 | MBP_N | 67 | BADc_N |
| 10 | PSD95_N | 39 | GFAP_N | 68 | pSynGAP_c |
| 11 | SAP102_N | 40 | GluR3_N | 69 | PSD95c_N |
| 12 | NMDA_N | 41 | GluR4_N | 70 | EGR1_N |
| 13 | pNR1_N | 42 | IL1B_N | 71 | EGR1_c |
| 14 | pNR2A_N | 43 | p38_N | 72 | H3MeK4_c |
| 15 | pNR2B_N | 44 | pp38_N | 73 | H4AcK12c_N |
| 16 | pPSD95_N | 45 | SYP_N | 74 | H4AcK12c_c |
| 17 | PSD95_c | 46 | H3AcK9_N | 75 | SYP_c |
| 18 | NMDAR_c | 47 | H3MeK4_N | 76 | **Genotype** |
| 19 | pNMDAR_c | 48 | H4AcK12_N | 77 | **Treatment** |
| 20 | pC3_N | 49 | CaNA_N | | |
| 21 | SynRas_N | 50 | Ubiquitin_N | | |
| 22 | SynGAP_N | 51 | pGSK3B_N | | |
| 23 | pSynGAP_N | 52 | ActiveGSK3B_N | | |
| 24 | SynGAPc_N | 53 | total_Tau_N | | |
| 25 | Raf_N | 54 | pTau_N | | |
| 26 | pC3_c | 55 | GFAP_c | | |
| 27 | RasGRF1_N | 56 | GluR3_c | | |
| 28 | ERK_N | 57 | IL1B_c | | |
| 29 | pERK_N | 58 | Snca_N | | |

---

## Example: Complete Request

### JSON Format
```json
{
  "features": [
    0.503, -0.196, 0.230, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006,
    -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223,
    0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129,
    0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167, 0.145, 0.176, 0.198,
    0.134, 0.156, 0.178, 0.201, 0.089, 0.112, 0.145, 0.134, 0.167, 0.189,
    0.156, 0.178, 0.145, 0.123, 0.167, 0.198, 0.156, 0.134, 0.189, 0.167,
    0.145, 0.178, 0.201, 0.156, -0.089, -0.145, -0.123, -0.087, -0.112, -0.134,
    -0.156, -0.178, -0.167, 0, 0
  ],
  "model_type": "svm",
  "classification_type": "binary"
}
```

✅ **77 values** (indices 0-76)

---

## Batch Prediction

For batch predictions, send **multiple samples**:

```json
{
  "features": [
    [0.503, -0.196, 0.230, ..., -0.167, 0, 0],  // Sample 1 (77 features)
    [0.412, -0.087, 0.156, ..., -0.129, 0, 0],  // Sample 2 (77 features)
    [0.621, -0.312, 0.345, ..., -0.234, 0, 0]   // Sample 3 (77 features)
  ],
  "model_type": "svm",
  "classification_type": "binary"
}
```

Each sample must have **exactly 77 features**

---

## Data Usage

### Last 2 Columns (Categorical - Optional)
- **Column 76**: Genotype (`Control`, `Tg2576`)
- **Column 77**: Treatment (`Saline`, `Memantine`)

⚠️ These are ignored by the API - use them for your own reference only  
✅ The models predict these values from the first 75 numerical features

---

## Error Messages

### ❌ "Expected 77 features, got 37"
**Problem**: Sending PCA-reduced features (37) instead of raw features (77)  
**Solution**: Use raw protein measurement values

### ❌ "Expected 77 features, got N"
**Problem**: Incorrect number of features  
**Solution**: Ensure you provide exactly 77 values

---

## Sample CSV Format

Use [sample_data_77features.csv](sample_data_77features.csv) as reference:
- 6 sample rows
- 77 columns (exactly what API expects)
- First 75 columns: Numerical protein measurements
- Last 2 columns: Categorical metadata (optional)

---

## Quick Test

**Copy-paste this into `/predict` endpoint:**

```json
{
  "features": [0.503, -0.196, 0.230, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006, -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223, 0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129, 0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167, 0.145, 0.176, 0.198, 0.134, 0.156, 0.178, 0.201, 0.089, 0.112, 0.145, 0.134, 0.167, 0.189, 0.156, 0.178, 0.145, 0.123, 0.167, 0.198, 0.156, 0.134, 0.189, 0.167, 0.145, 0.178, 0.201, 0.156, -0.089, -0.145, -0.123, -0.087, -0.112, -0.134, -0.156, -0.178, -0.167, 0, 0],
  "model_type": "svm",
  "classification_type": "binary"
}
```

✅ Should work now!

---

## Valid Options

### model_type
- `svm` (Support Vector Machine) ⭐ Best accuracy
- `rf` (Random Forest) ⭐ Fast
- `mlp` (Neural Network)
- `logreg` (Logistic Regression)

### classification_type
- `binary` - Predict Genotype (Control vs Tg2576)
- `multiclass` - Predict Treatment/Behavior (4 classes)

---

## Next Steps

1. ✅ Get 77-feature data
2. ✅ Send to `/predict` or `/batch_predict`
3. ✅ API automatically preprocesses → PCA → predicts
4. ✅ Get prediction result!

**Questions?** Check [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md) for complete examples.
