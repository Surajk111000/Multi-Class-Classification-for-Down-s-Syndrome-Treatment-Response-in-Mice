"""
FastAPI application for Mice Protein Expression Classification
Multi-Class Classification for Down's Syndrome Treatment Response in Mice
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import List

from app.schemas import (
    PredictionRequest,
    SinglePredictionRequest,
    PredictionResponse,
    HealthResponse,
    CSVUploadResponse
)
from app.predict import make_predictions, Predictor
from app.model_loader import ModelLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Mice Protein Expression Classification",
    description="Multi-Class Classification for Down's Syndrome Treatment Response in Mice",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model loader on startup
@app.on_event("startup")
async def startup_event():
    """Load models on application startup"""
    logger.info("Loading ML models...")
    ModelLoader()
    logger.info("Models loaded successfully")


@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with API information"""
    model_loader = ModelLoader()
    available_models = model_loader.get_available_models()
    
    if not available_models:
        models_msg = "⚠️ No models loaded. Run: python quick_train.py"
    else:
        models_msg = f"✓ {len(available_models)} models loaded"
    
    return {
        "message": "Mice Protein Expression Classification API",
        "version": "1.0.0",
        "description": "Multi-Class Classification for Down's Syndrome Treatment Response in Mice",
        "status": models_msg,
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "batch_predict": "/batch_predict",
            "docs": "/docs"
        },
        "quick_start": "Run: python quick_train.py (first time only)"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    model_loader = ModelLoader()
    available_models = model_loader.get_available_models()
    pca_available = model_loader.get_pca() is not None
    
    return HealthResponse(
        status="healthy",
        models_loaded=available_models,
        pca_available=pca_available
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict_single(request: SinglePredictionRequest):
    """
    Make a single prediction
    
    Parameters:
    - features: List of float values (feature vector)
    - model_type: 'svm', 'rf', 'mlp', or 'logreg'
    - classification_type: 'binary' or 'multiclass'
    
    Example:
    ```json
    {
        "features": [1.0, 2.0, 3.0, ...],
        "model_type": "svm",
        "classification_type": "binary"
    }
    ```
    """
    try:
        # Check if models are loaded
        model_loader = ModelLoader()
        if not model_loader.get_available_models():
            raise HTTPException(
                status_code=503,
                detail="Models not loaded. Please run: python quick_train.py"
            )
        
        # Validate model and classification type
        if request.model_type not in ['svm', 'rf', 'mlp', 'logreg']:
            raise ValueError(f"Invalid model type. Choose from: svm, rf, mlp, logreg")
        
        if request.classification_type not in ['binary', 'multiclass']:
            raise ValueError(f"Invalid classification type. Choose from: binary, multiclass")
        
        predictions, confidence = make_predictions(
            [request.features],
            request.model_type,
            request.classification_type
        )
        
        return PredictionResponse(
            predictions=predictions,
            model_used=f"{request.model_type}_{request.classification_type}",
            classification_type=request.classification_type,
            confidence=confidence
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/batch_predict", response_model=PredictionResponse, tags=["Predictions"])
async def batch_predict(request: PredictionRequest):
    """
    Batch predictions for multiple samples
    
    Parameters:
    - features: List of feature vectors (2D list)
    - model_type: 'svm', 'rf', 'mlp', or 'logreg'
    - classification_type: 'binary' or 'multiclass'
    
    Example:
    ```json
    {
        "features": [[1.0, 2.0, 3.0, ...], [4.0, 5.0, 6.0, ...]],
        "model_type": "svm",
        "classification_type": "binary"
    }
    ```
    """
    try:
        # Check if models are loaded
        model_loader = ModelLoader()
        if not model_loader.get_available_models():
            raise HTTPException(
                status_code=503,
                detail="Models not loaded. Please run: python quick_train.py"
            )
        
        # Validate inputs
        if not request.features:
            raise ValueError("Features list cannot be empty")
        
        if request.model_type not in ['svm', 'rf', 'mlp', 'logreg']:
            raise ValueError(f"Invalid model type. Choose from: svm, rf, mlp, logreg")
        
        if request.classification_type not in ['binary', 'multiclass']:
            raise ValueError(f"Invalid classification type. Choose from: binary, multiclass")
        
        predictions, confidence = make_predictions(
            request.features,
            request.model_type,
            request.classification_type
        )
        
        return PredictionResponse(
            predictions=predictions,
            model_used=f"{request.model_type}_{request.classification_type}",
            classification_type=request.classification_type,
            confidence=confidence
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/models/available", tags=["Info"])
async def get_available_models():
    """Get list of available models"""
    available_models = ModelLoader().get_available_models()
    return {
        "available_models": available_models,
        "model_types": ["svm", "rf", "mlp", "logreg"],
        "classification_types": ["binary", "multiclass"],
        "total_models": len(available_models),
        "note": "CSV upload endpoint is available with 'python-multipart' installed"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
