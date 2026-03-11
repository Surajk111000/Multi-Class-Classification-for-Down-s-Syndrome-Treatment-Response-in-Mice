#!/usr/bin/env python3
"""
Complete API Testing Script for Mice Protein Classification API
Tests all endpoints with sample data
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

# Sample data (37 PCA-reduced protein features)
SAMPLE_FEATURES = [
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
     0.112, 0.178, 0.189, 0.234, 0.278, 0.245, 0.203],
]

def test_health():
    """Test health endpoint"""
    print("\n" + "="*70)
    print("1️⃣  Testing /health endpoint...")
    print("="*70)
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Status Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_root():
    """Test root endpoint"""
    print("\n" + "="*70)
    print("0️⃣  Testing / (root) endpoint...")
    print("="*70)
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Status Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_single_prediction_binary():
    """Test single prediction - Binary"""
    print("\n" + "="*70)
    print("2️⃣  Testing /predict endpoint - BINARY Classification...")
    print("="*70)
    try:
        payload = {
            "features": SAMPLE_FEATURES[0],
            "model_type": "svm",
            "classification_type": "binary"
        }
        print(f"Request: {json.dumps(payload, indent=2)[:200]}...")
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"✅ Status Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_single_prediction_multiclass():
    """Test single prediction - Multi-class"""
    print("\n" + "="*70)
    print("2️⃣  Testing /predict endpoint - MULTI-CLASS Classification...")
    print("="*70)
    try:
        payload = {
            "features": SAMPLE_FEATURES[0],
            "model_type": "svm",
            "classification_type": "multiclass"
        }
        print(f"Request: {json.dumps(payload, indent=2)[:200]}...")
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"✅ Status Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_batch_prediction():
    """Test batch prediction"""
    print("\n" + "="*70)
    print("3️⃣  Testing /batch_predict endpoint - BATCH Processing...")
    print("="*70)
    try:
        payload = {
            "features": SAMPLE_FEATURES,
            "model_type": "svm",
            "classification_type": "binary"
        }
        print(f"Batch Size: {len(SAMPLE_FEATURES)} samples")
        print(f"Features per sample: {len(SAMPLE_FEATURES[0])}")
        response = requests.post(f"{BASE_URL}/batch_predict", json=payload)
        print(f"✅ Status Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_different_models():
    """Test different models"""
    print("\n" + "="*70)
    print("4️⃣  Testing Different Models...")
    print("="*70)
    models = ["svm", "rf", "mlp", "logreg"]
    results = {}
    
    for model in models:
        try:
            payload = {
                "features": SAMPLE_FEATURES[0],
                "model_type": model,
                "classification_type": "binary"
            }
            response = requests.post(f"{BASE_URL}/predict", json=payload)
            success = response.status_code == 200
            results[model] = success
            status = "✅" if success else "❌"
            pred = response.json().get("predictions", []) if success else "ERROR"
            print(f"{status} {model.upper():10s} - Prediction: {pred}")
        except Exception as e:
            results[model] = False
            print(f"❌ {model.upper():10s} - Error: {str(e)[:50]}")
    
    return all(results.values())

def test_available_models():
    """Test available models endpoint"""
    print("\n" + "="*70)
    print("5️⃣  Testing /models/available endpoint...")
    print("="*70)
    try:
        response = requests.get(f"{BASE_URL}/models/available")
        print(f"✅ Status Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  🧪 MICE PROTEIN CLASSIFICATION API - TEST SUITE  ".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    print(f"\n📍 API URL: {BASE_URL}")
    print(f"📊 Sample Size: {len(SAMPLE_FEATURES)} samples")
    print(f"🎯 Features: 37 (PCA-reduced from 77 proteins)")
    
    tests = [
        ("Root Endpoint", test_root),
        ("Health Check", test_health),
        ("Single Prediction (Binary)", test_single_prediction_binary),
        ("Single Prediction (Multi-class)", test_single_prediction_multiclass),
        ("Batch Prediction", test_batch_prediction),
        ("Multiple Models", test_different_models),
        ("Available Models", test_available_models),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} failed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  📊 TEST SUMMARY  ".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name:.<45} {status}")
    
    total = len(results)
    passed = sum(results.values())
    percentage = (passed / total * 100) if total > 0 else 0
    
    print("\n" + "-" * 70)
    print(f"  Total Passed: {passed}/{total} ({percentage:.0f}%)")
    print("-" * 70)
    
    if all(results.values()):
        print("\n🎉 ALL TESTS PASSED! API is working perfectly! 🎉\n")
        return True
    else:
        print("\n⚠️  Some tests failed. Check errors above.\n")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Test suite interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
