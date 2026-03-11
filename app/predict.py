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
        self.imputer = SimpleImputer(strategy='mean')

    def preprocess_features(self, X: np.ndarray) -> np.ndarray:
        """
        Preprocess features: handle missing values and apply PCA
        
        Args:
            X: Input features array (n_samples, n_features)
            
        Returns:
            Preprocessed features after PCA reduction
        """
        # Handle missing values
        X_imputed = self.imputer.fit_transform(X)
        
        # Apply PCA
        pca = self.model_loader.get_pca()
        if pca is not None:
            X_transformed = pca.transform(X_imputed)
            return X_transformed
        else:
            logger.warning("PCA not available, returning imputed features")
            return X_imputed

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
