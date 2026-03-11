"""
Pydantic schemas for request/response validation
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Schema for batch prediction requests"""
    features: List[List[float]] = Field(..., description="List of feature vectors")
    model_type: str = Field("svm", description="Model to use: 'svm', 'rf', 'mlp', 'logreg'")
    classification_type: str = Field("binary", description="Classification type: 'binary' or 'multiclass'")

    class Config:
        json_schema_extra = {
            "example": {
                "features": [[1.0, 2.0, 3.0, 4.0]],
                "model_type": "svm",
                "classification_type": "binary"
            }
        }


class SinglePredictionRequest(BaseModel):
    """Schema for single prediction requests"""
    features: List[float] = Field(..., description="Single feature vector")
    model_type: str = Field("svm", description="Model to use")
    classification_type: str = Field("binary", description="Classification type")


class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    predictions: List[int]
    model_used: str
    classification_type: str
    confidence: Optional[List[float]] = None


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
