"""
Simple tests for the FastAPI application
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert isinstance(data["models_loaded"], list)
    assert "pca_available" in data


def test_available_models():
    """Test available models endpoint"""
    response = client.get("/models/available")
    assert response.status_code == 200
    data = response.json()
    assert "available_models" in data
    assert "model_types" in data
    assert "classification_types" in data


def test_batch_predict_missing_features():
    """Test batch predict with missing features"""
    response = client.post("/batch_predict", json={
        "features": [],
        "model_type": "svm",
        "classification_type": "binary"
    })
    assert response.status_code == 400


def test_batch_predict_invalid_model_type():
    """Test batch predict with invalid model type"""
    response = client.post("/batch_predict", json={
        "features": [[1.0, 2.0, 3.0]],
        "model_type": "invalid_model",
        "classification_type": "binary"
    })
    assert response.status_code == 400


def test_batch_predict_invalid_classification_type():
    """Test batch predict with invalid classification type"""
    response = client.post("/batch_predict", json={
        "features": [[1.0, 2.0, 3.0]],
        "model_type": "svm",
        "classification_type": "invalid_type"
    })
    assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
