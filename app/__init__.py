"""
Mice Protein Expression Classification FastAPI Application
Multi-Class Classification for Down's Syndrome Treatment Response in Mice
"""

from app.model_loader import ModelLoader
from app.predict import Predictor, make_predictions
from app.main import app

__version__ = "1.0.0"
__author__ = "Suraj"
__description__ = "Multi-Class Classification for Down's Syndrome Treatment Response in Mice"

__all__ = [
    'app',
    'ModelLoader',
    'Predictor',
    'make_predictions'
]
