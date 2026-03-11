#!/usr/bin/env python3
"""
Quick API Test - 77 Raw Features Format
Tests the /predict endpoint with correct data format
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# Correct format: 77 raw protein features
SAMPLE_DATA_77_FEATURES = [
    0.503, -0.196, 0.230, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006,
    -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223,
    0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129,
    0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167, 0.145, 0.176, 0.198,
    0.134, 0.156, 0.178, 0.201, 0.089, 0.112, 0.145, 0.134, 0.167, 0.189,
    0.156, 0.178, 0.145, 0.123, 0.167, 0.198, 0.156, 0.134, 0.189, 0.167,
    0.145, 0.178, 0.201, 0.156, -0.089, -0.145, -0.123, -0.087, -0.112, -0.134,
    -0.156, -0.178, -0.167, 0, 0
]

print("=" * 70)
print("🧪 QUICK API TEST - 77 Raw Features Format")
print("=" * 70)

print(f"\n📊 Input Data:")
print(f"   - Features: {len(SAMPLE_DATA_77_FEATURES)} (expected: 77)")
print(f"   - Model: SVM")
print(f"   - Type: Binary Classification")

payload = {
    "features": SAMPLE_DATA_77_FEATURES,
    "model_type": "svm",
    "classification_type": "binary"
}

print(f"\n📤 Sending request to {BASE_URL}/predict...")

try:
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    
    print(f"\n✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n📋 Response:")
        print(json.dumps(result, indent=2))
        print("\n✅ SUCCESS! API is working with 77-feature format!")
    else:
        print(f"\n❌ Error:")
        print(json.dumps(response.json(), indent=2))
        
except Exception as e:
    print(f"\n❌ Connection Error: {str(e)}")
    print("\n⚠️  Make sure FastAPI is running:")
    print("   python -m uvicorn app.main_simple:app --port 8000")

print("\n" + "=" * 70)
