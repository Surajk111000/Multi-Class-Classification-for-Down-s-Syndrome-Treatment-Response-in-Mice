"""
Pydantic schemas for request/response validation
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Schema for batch prediction requests - expects exactly 77 features per sample"""
    features: List[List[float]] = Field(..., description="List of feature vectors (each with exactly 77 features)")
    model_type: str = Field("svm", description="Model to use: 'svm', 'rf', 'mlp', 'logreg'")
    classification_type: str = Field("binary", description="Classification type: 'binary' or 'multiclass'")

    class Config:
        json_schema_extra = {
            "example": {
                "features": [[
                    0.503, -0.196, 0.23, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006,
                    -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223,
                    0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129,
                    0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167, 0.145, 0.176, 0.198,
                    0.134, 0.156, 0.178, 0.201, 0.089, 0.112, 0.145, 0.134, 0.167, 0.189,
                    0.156, 0.178, 0.145, 0.123, 0.167, 0.198, 0.156, 0.134, 0.189, 0.167,
                    0.145, 0.178, 0.201, 0.156, -0.089, -0.145, -0.123, -0.087, -0.112, -0.134,
                    -0.156, -0.178, -0.167, 0.234, 0.156, 0.145, 0.189
                ]],
                "model_type": "svm",
                "classification_type": "binary"
            }
        }


class SinglePredictionRequest(BaseModel):
    """Schema for single prediction requests - expects exactly 77 features"""
    features: List[float] = Field(..., description="Single feature vector (exactly 77 features)")
    model_type: str = Field("svm", description="Model to use: 'svm', 'rf', 'mlp', 'logreg'")
    classification_type: str = Field("binary", description="Classification type: 'binary' or 'multiclass'")

    class Config:
        json_schema_extra = {
            "example": {
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
        }


class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    predictions: List[int]
    model_used: str
    classification_type: str


class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str
    models_loaded: List[str]
    pca_available: bool


class CSVUploadResponse(BaseModel):
    """Schema for CSV upload response"""
    status: str
    rows_processed: int
    predictions: List[int]
    model_used: str
    classification_type: str
