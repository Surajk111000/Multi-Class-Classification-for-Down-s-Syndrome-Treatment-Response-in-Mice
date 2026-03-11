# 🎨 User-Friendly API Testing Guide

## 🚀 Quick Start - The Easy Way

### 1. **Open the HTML Tester** 
File: [api_tester.html](api_tester.html)

**Simply double-click the file OR:**
```bash
# Windows:
start api_tester.html

# Or open in browser:
http://localhost/path/to/api_tester.html
```

### 2. **You'll See:**
- ✅ Beautiful interface with dropdowns
- ✅ Model selection (SVM, Random Forest, MLP, Logistic Regression)
- ✅ Classification type (Binary or Multi-class)
- ✅ Sample count (1, 2, 3, or 5 samples)
- ✅ Pre-built sample data ready to load

### 3. **How to Use:**

**Step 1:** Select number of samples
```
📊 Choose: 1, 2, 3, or 5 samples
```

**Step 2:** Pick your model
```
🎯 SVM - Best accuracy (recommended)
🌲 Random Forest - Fast & accurate
🧠 Neural Network - Advanced
📈 Logistic Regression - Simple
```

**Step 3:** Choose what to predict
```
👥 Binary - Is it Control or Tg2576?
🎨 Multi-class - Which treatment group?
```

**Step 4:** Load sample data
```
Click "Load Sample Data" button
```

**Step 5:** Execute!
```
Click "▶️ Execute Test"
```

**Step 6:** See results in green ✅ or red ❌

---

## 📊 Understanding the 77 Features

### **Feature Breakdown:**

| Columns | Type | Count | Purpose |
|---------|------|-------|---------|
| 1-37 | Numbers | 37 | Protein measurements (5-10 range) |
| 38-75 | Numbers | 38 | Additional protein features |
| 76 | Text | 1 | Genotype: "Control" or "Tg2576" |
| 77 | Text | 1 | Treatment: "Saline" or "Memantine" |

### **Total: 77 Features** (columns in your data)

---

## 📋 Sample Data Explanation

### **Sample 1 (Binary: Control/Saline)**
```
0.503, -0.196, 0.230, ..., 0, 0
↑     ↑       ↑            ↑  ↑
Protein measurements    Genotype Treatment
(normalized -1 to +1)
```

### **Sample 2 (Binary: Tg2576/Saline)**
```
0.412, -0.087, 0.156, ..., 0, 0
(Different protein levels for different genotype)
```

### **Sample 3 (Multi-class: Tg2576/Memantine)**
```
0.621, -0.312, 0.345, ..., 0, 0
(Different again - another treatment)
```

---

## 🎯 Example Scenarios

### Scenario 1: Predict Genotype (Binary)
**Goal:** Identify if mouse is Control or Tg2576

```
Number of Samples:     2
Model Type:            SVM ⭐
Classification Type:   Binary
Expected Output:       [0, 1] or [1, 0]
                       0 = Control
                       1 = Tg2576
```

### Scenario 2: Predict Treatment (Multi-class)
**Goal:** Identify which treatment group (4 classes)

```
Number of Samples:     3
Model Type:            Random Forest
Classification Type:   Multi-class
Expected Output:       [0, 1, 2, 3]
                       0 = Saline (Control)
                       1 = Memantine (Control)
                       2 = Saline (Tg2576)
                       3 = Memantine (Tg2576)
```

---

## 📈 Response Explanation

### **What You'll See (Success):**
```json
{
  "predictions": [0, 1, 2],
  "model_used": "svm_binary",
  "classification_type": "binary",
  "confidence": [[0.95, 0.05], [0.12, 0.88], ...]
}
```

### **Field Meanings:**
| Field | Meaning |
|-------|---------|
| `predictions` | Predicted class for each sample |
| `model_used` | Which model was used |
| `classification_type` | Type of prediction |
| `confidence` | Probability for each class |

---

## 🧪 Multi-Sample Testing

### **Test 2 Samples Using HTML Interface:**

1. Select: **2 Samples (Batch Prediction)**
2. Select: **SVM** model
3. Select: **Binary** classification
4. Click: **Load Sample Data**
5. Click: **Execute Test**

**Result:** 
```
✅ 200 Success
predictions: [0, 1]
confidence: [[0.95, 0.05], [0.15, 0.85]]
```

---

## 🔧 Column Name Reference

For your data files:

```csv
DYRK1A_N,ITSN1_N,CRMP3_N,CRMP5_N,...,Genotype,Treatment
0.503,-0.196,0.230,-0.226,...,Control,Saline
```

**The 77 columns in order:**
1. DYRK1A_N through H4AcK12c_c (75 protein measurements)
2. Genotype (column 76)
3. Treatment (column 77)

---

## 💡 Tips for Best Results

1. **Use SVM model** - Best accuracy (96.72%)
2. **Ensure 77 values** - Not 37, not 75, exactly 77
3. **Test with samples** - See consistency across models
4. **Check confidence** - Higher values = more confident prediction
5. **Try multi-sample** - Test 2-5 samples at once

---

## ❓ Troubleshooting

### **Error: "Cannot reach API"**
✅ Fix: Make sure server is running
```bash
python -m uvicorn app.main_simple:app --port 8000
```

### **Error: "Expected 77 features"**
✅ Fix: Make sure you have exactly 77 values (including genotype and treatment columns)

### **Error: "Invalid model type"**
✅ Fix: Use one of: `svm`, `rf`, `mlp`, `logreg`

### **Error: 422 Unprocessable Entity**
✅ Fix: For `/batch_predict`, wrap features in extra brackets: `[[...], [...]]`

---

## 📱 Desktop vs Web Testing

### **HTML Interface (Easiest!) ⭐**
- Double-click `api_tester.html`
- No installation needed
- Beautiful dropdowns
- Perfect for non-technical users

### **Swagger UI**
- Visit: http://localhost:8000/docs
- More technical
- Useful for API exploration

### **curl Command**
- For power users
- Terminal-based testing

### **Python Script**
- For automation
- Integration testing

---

## 🎯 Decision Tree: Which Option to Use?

```
Are you non-technical?
    ├─ YES → Use api_tester.html ⭐
    └─ NO  → Use Swagger UI (http://localhost:8000/docs)

Want to test 1 sample?
    ├─ YES → Use /predict endpoint
    └─ NO  → Use /batch_predict endpoint

Want pretty interface?
    ├─ YES → Use api_tester.html ⭐
    └─ NO  → Use curl or Python
```

---

## 📊 File Reference

| File | Purpose |
|------|---------|
| [api_tester.html](api_tester.html) | 🌟 Beautiful UI with dropdowns |
| [sample_data_77features.csv](sample_data_77features.csv) | Sample data (77 columns) |
| [DATA_FORMAT_GUIDE.md](DATA_FORMAT_GUIDE.md) | Detailed format info |
| [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md) | Technical testing guide |

---

## ✅ Next Steps

1. **Open** `api_tester.html` in your browser
2. **Select** your preferences from dropdowns
3. **Click** "Load Sample Data"
4. **Click** "Execute Test"
5. **See** results in real-time! 🎉

**The interface will:**
- ✅ Show connection status
- ✅ Remember your settings
- ✅ Display pretty formatted responses
- ✅ Highlight errors clearly
- ✅ Show what each value means

---

## 🎨 Features of api_tester.html

✅ **Dropdowns for easy selection**
- Model type (4 options with descriptions)
- Classification type (2 options explained)
- Sample count (1, 2, 3, or 5)

✅ **Column mapping guide**
- Shows which columns are which

✅ **Pre-built sample data**
- Click "Load Sample Data" to populate

✅ **Real-time connection status**
- Shows if API is reachable

✅ **Beautiful response display**
- Success in green ✅
- Errors in red ❌
- Color-coded for clarity

✅ **Mobile responsive**
- Works on tablets too!

---

## 🚀 Ready to Test?

1. Make sure API is running
2. Open `api_tester.html`
3. Select your options
4. Load sample data
5. Execute! 🎉

**That's it!** No technical knowledge needed. 🌟
