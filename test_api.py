"""
Test Script for Mice Protein Classification API
Demonstrates all three testing methods: JSON, Batch, and CSV
"""

import requests
import json
import csv
import sys
import time

# Configuration
BASE_URL = "http://localhost:8000"
SAMPLE_77_FEATURES = [
    0.503, -0.196, 0.230, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006,
    -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223,
    0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129,
    0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167, 0.145, 0.176, 0.198,
    0.134, 0.156, 0.178, 0.201, 0.089, 0.112, 0.145, 0.134, 0.167, 0.189,
    0.156, 0.178, 0.145, 0.123, 0.167, 0.198, 0.156, 0.134, 0.189, 0.167,
    0.145, 0.178, 0.201, 0.156, -0.089, -0.145, -0.123, -0.087, -0.112, -0.134,
    -0.156, -0.178, -0.167, 0.234, 0.156, 0.145, 0.189
]

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_status(status, message):
    """Print status message"""
    icon = "✅" if status == "success" else "❌"
    print(f"{icon} {message}")

def test_health():
    """Test health check endpoint"""
    print_section("TEST 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_status("success", "Health check passed")
            print(f"   Status: {data['status']}")
            print(f"   Models loaded: {len(data['models_loaded'])}")
            print(f"   PCA available: {data['pca_available']}")
            return True
        else:
            print_status("error", f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_status("error", f"Connection failed: {str(e)}")
        return False

def test_single_prediction():
    """Test single prediction endpoint /predict"""
    print_section("TEST 2: Single Prediction (/predict)")
    try:
        payload = {
            "features": SAMPLE_77_FEATURES,
            "model_type": "svm",
            "classification_type": "binary"
        }
        
        print(f"Sending request with:")
        print(f"  - Features: {len(SAMPLE_77_FEATURES)} values")
        print(f"  - Model: SVM")
        print(f"  - Classification: Binary")
        
        response = requests.post(
            f"{BASE_URL}/predict",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_status("success", "Prediction received")
            print(f"   Prediction: {data['predictions']}")
            print(f"   Model used: {data['model_used']}")
            if data.get('confidence'):
                print(f"   Confidence: {data['confidence']}")
            return True
        else:
            print_status("error", f"Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_status("error", f"Request failed: {str(e)}")
        return False

def test_batch_prediction():
    """Test batch prediction endpoint /batch_predict"""
    print_section("TEST 3: Batch Prediction (/batch_predict)")
    try:
        payload = {
            "features": [SAMPLE_77_FEATURES, SAMPLE_77_FEATURES],
            "model_type": "rf",
            "classification_type": "multiclass"
        }
        
        print(f"Sending request with:")
        print(f"  - Samples: 2")
        print(f"  - Features per sample: {len(SAMPLE_77_FEATURES)}")
        print(f"  - Model: Random Forest")
        print(f"  - Classification: Multi-class")
        
        response = requests.post(
            f"{BASE_URL}/batch_predict",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_status("success", "Batch predictions received")
            print(f"   Predictions: {data['predictions']}")
            print(f"   Model used: {data['model_used']}")
            if data.get('confidence'):
                print(f"   Confidence: {data['confidence']}")
            return True
        else:
            print_status("error", f"Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_status("error", f"Request failed: {str(e)}")
        return False

def test_csv_prediction():
    """Test CSV upload endpoint /csv_predict"""
    print_section("TEST 4: CSV Prediction (/csv_predict)")
    
    try:
        # Check if sample CSV exists
        csv_file = "sample_data_77_noheaders.csv"
        try:
            with open(csv_file, 'r') as f:
                csv_data = f.read()
            print(f"   Using CSV file: {csv_file}")
        except FileNotFoundError:
            print_status("warning", f"CSV file not found: {csv_file}")
            print("   Skipping CSV test")
            return None
        
        # Prepare multipart form data
        files = {'file': ('sample_data_77_noheaders.csv', csv_data, 'text/csv')}
        params = {
            'model_type': 'svm',
            'classification_type': 'binary'
        }
        
        print(f"Sending request with:")
        print(f"  - CSV file: {csv_file}")
        print(f"  - Model: SVM")
        print(f"  - Classification: Binary")
        
        response = requests.post(
            f"{BASE_URL}/csv_predict",
            files=files,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_status("success", "CSV predictions received")
            print(f"   Rows processed: {data['rows_processed']}")
            print(f"   Predictions: {data['predictions']}")
            print(f"   Model used: {data['model_used']}")
            return True
        else:
            print_status("error", f"Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_status("error", f"Request failed: {str(e)}")
        return False

def test_available_models():
    """Test available models endpoint"""
    print_section("TEST 5: Available Models (/models/available)")
    try:
        response = requests.get(f"{BASE_URL}/models/available")
        if response.status_code == 200:
            data = response.json()
            print_status("success", "Models list retrieved")
            print(f"   Available models: {', '.join(data['model_types'])}")
            print(f"   Classification types: {', '.join(data['classification_types'])}")
            print(f"   Total models loaded: {data['total_models']}")
            return True
        else:
            print_status("error", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_status("error", f"Request failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪 MICE PROTEIN CLASSIFICATION API TEST SUITE".center(70, "="))
    print(f"Base URL: {BASE_URL}\n")
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server at {BASE_URL}")
        print("\nTo start the server, run:")
        print("  python -m uvicorn app.main_simple:app --reload")
        sys.exit(1)
    
    results = {}
    
    # Run all tests
    results['health'] = test_health()
    results['single'] = test_single_prediction()
    results['batch'] = test_batch_prediction()
    results['csv'] = test_csv_prediction()
    results['models'] = test_available_models()
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v is True)
    total = sum(1 for v in results.values() if v is not None)
    
    print(f"\n✅ Passed: {passed}/{total}")
    for test_name, result in results.items():
        if result is not None:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status}: {test_name}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
