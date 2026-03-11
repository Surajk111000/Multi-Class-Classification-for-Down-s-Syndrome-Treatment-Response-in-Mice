"""
Model and PCA loader utility
"""
import os
import pickle
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ModelLoader:
    """Handles loading and managing all trained ML models and PCA"""

    _instance = None
    _models = {}
    _pca = None

    def __new__(cls):
        """Singleton pattern to ensure only one instance"""
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize model loader"""
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._models = {}
            self._pca = None
            self.load_all_models()

    def load_all_models(self) -> None:
        """Load all trained models and PCA from pickle files"""
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'saved_models')
        
        if not os.path.exists(models_dir):
            logger.warning(f"Models directory not found: {models_dir}")
            return

        model_files = {
            # Binary classification models
            'logreg_binary': 'logreg_binary.pkl',
            'mlp_binary': 'mlp_binary.pkl',
            'svm_binary': 'svm_binary.pkl',
            'rf_binary': 'rf_binary.pkl',
            # Multi-class classification models
            'logreg_4class': 'logreg_4class.pkl',
            'mlp_4class': 'mlp_4class.pkl',
            'svm_4class': 'svm_4class.pkl',
            'rf_4class': 'rf_4class.pkl',
        }

        for model_name, filename in model_files.items():
            filepath = os.path.join(models_dir, filename)
            try:
                if os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        self._models[model_name] = pickle.load(f)
                    logger.info(f"Loaded model: {model_name}")
                else:
                    logger.warning(f"Model file not found: {filepath}")
            except Exception as e:
                logger.error(f"Error loading model {model_name}: {str(e)}")

        # Load PCA
        pca_path = os.path.join(models_dir, 'pca_37.pkl')
        try:
            if os.path.exists(pca_path):
                with open(pca_path, 'rb') as f:
                    self._pca = pickle.load(f)
                logger.info("Loaded PCA transformer")
            else:
                logger.warning(f"PCA file not found: {pca_path}")
        except Exception as e:
            logger.error(f"Error loading PCA: {str(e)}")

    @classmethod
    def get_model(cls, model_name: str):
        """Get a specific model by name"""
        instance = cls()
        return instance._models.get(model_name)

    @classmethod
    def get_pca(cls):
        """Get the PCA transformer"""
        instance = cls()
        return instance._pca

    @classmethod
    def get_all_models(cls) -> Dict:
        """Get all loaded models"""
        instance = cls()
        return instance._models

    @classmethod
    def is_model_loaded(cls, model_name: str) -> bool:
        """Check if a model is loaded"""
        instance = cls()
        return model_name in instance._models

    @classmethod
    def get_available_models(cls) -> list:
        """Get list of available models"""
        instance = cls()
        return list(instance._models.keys())


def load_models():
    """Convenience function to load all models"""
    return ModelLoader()
