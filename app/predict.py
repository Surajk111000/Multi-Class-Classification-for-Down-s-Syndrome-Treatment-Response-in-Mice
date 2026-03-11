"""
Prediction utilities for ML models
"""
import numpy as np
from typing import List, Tuple, Optional
from sklearn.impute import SimpleImputer
import logging

from .model_loader import ModelLoader

logger = logging.getLogger(__name__)


class Predictor:
    """Handles predictions using trained models"""

    def __init__(self):
        self.model_loader = ModelLoader()
        self.imputer = self.model_loader.get_imputer()
        if self.imputer is None:
            logger.warning("Imputer not loaded, using fallback")
            self.imputer = SimpleImputer(strategy='mean')

    def preprocess_features(self, X: np.ndarray) -> np.ndarray:
        """
        Preprocess features: handle missing values and apply PCA
        
        Args:
            X: Input features array (n_samples, 77) - expects 77 raw protein features
            
        Returns:
            Preprocessed features after PCA reduction (n_samples, 37)
        """
        # Validate input shape
        if X.shape[1] != 77:
            raise ValueError(f"Expected 77 features, got {X.shape[1]}. Input must have 77 raw protein features.")
        
        # Handle missing values using pre-fitted imputer from training
        if self.imputer is not None:
            X_imputed = self.imputer.transform(X)
        else:
            logger.warning("Imputer not available, skipping imputation")
            X_imputed = X
        
        # Apply PCA transformation
        pca = self.model_loader.get_pca()
        if pca is not None:
            X_transformed = pca.transform(X_imputed)
            return X_transformed
        else:
            raise ValueError("PCA transformer not loaded")

    def predict(
        self,
        features: List[List[float]],
        model_type: str = "svm",
        classification_type: str = "binary"
    ) -> Tuple[List[int], Optional[List[List[float]]]]:
        """
        Make predictions using specified model
        
        Args:
            features: List of feature vectors
            model_type: Type of model ('svm', 'rf', 'mlp', 'logreg')
            classification_type: 'binary' or 'multiclass'
            
        Returns:
            Tuple of (predictions, confidence_scores if available)
        """
        # Convert to numpy array
        X = np.array(features, dtype=np.float32)
        
        # Preprocess features
        X_processed = self.preprocess_features(X)
        
        # Select model
        if classification_type == "binary":
            model_name = f"{model_type}_binary"
        else:
            model_name = f"{model_type}_4class"
        
        model = self.model_loader.get_model(model_name)
        
        if model is None:
            raise ValueError(f"Model {model_name} not found or not loaded")
        
        # Make predictions
        predictions = model.predict(X_processed)
        
        # Get confidence scores if available
        confidence = None
        if hasattr(model, 'predict_proba'):
            try:
                confidence = model.predict_proba(X_processed).tolist()
            except Exception as e:
                logger.warning(f"Could not get confidence scores: {str(e)}")
        
        return predictions.tolist(), confidence

    def validate_features(self, features: List[List[float]], expected_length: int = None) -> bool:
        """
        Validate feature vectors
        
        Args:
            features: List of feature vectors
            expected_length: Expected length of each feature vector
            
        Returns:
            True if valid, False otherwise
        """
        if not features:
            return False
        
        if expected_length is not None:
            for feature_vector in features:
                if len(feature_vector) != expected_length:
                    return False
        
        return True


def make_predictions(
    features: List[List[float]],
    model_type: str = "svm",
    classification_type: str = "binary"
) -> Tuple[List[int], Optional[List[List[float]]]]:
    """
    Convenience function to make predictions
    
    Args:
        features: List of feature vectors
        model_type: Type of model
        classification_type: Classification type
        
    Returns:
        Tuple of predictions and confidence scores
    """
    predictor = Predictor()
    return predictor.predict(features, model_type, classification_type)
