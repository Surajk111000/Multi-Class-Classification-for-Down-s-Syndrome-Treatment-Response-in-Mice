"""
Deployment startup script - ensures models are trained before starting server
"""
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_models():
    """Check if all required models exist"""
    model_dir = "models/saved_models"
    required_models = [
        "svm_binary.pkl",
        "svm_4class.pkl",
        "rf_binary.pkl",
        "rf_4class.pkl",
        "mlp_binary.pkl",
        "mlp_4class.pkl",
        "logreg_binary.pkl",
        "logreg_4class.pkl",
        "imputer.pkl",
        "pca.pkl"
    ]
    
    missing = []
    for model in required_models:
        model_path = os.path.join(model_dir, model)
        if not os.path.exists(model_path):
            missing.append(model)
    
    return missing

def train_models():
    """Train all models"""
    logger.info("🔄 Training models... This may take 1-2 minutes")
    os.system(f"{sys.executable} quick_train.py")
    
    # Check again
    missing = check_models()
    if missing:
        logger.error(f"❌ Training failed! Missing: {missing}")
        return False
    
    logger.info("✅ Models trained successfully!")
    return True

if __name__ == "__main__":
    logger.info("🚀 Deployment startup check...")
    
    missing = check_models()
    if missing:
        logger.warning(f"⚠️ Missing models: {missing}")
        logger.info("Training models now...")
        if not train_models():
            logger.error("Failed to train models!")
            sys.exit(1)
    else:
        logger.info("✅ All models present!")
    
    logger.info("Starting FastAPI server...")
    os.execvp("gunicorn", ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "app.main_simple:app"])
