"""
Training script for Mice Protein Expression Classification
Trains both binary and multi-class models using different algorithms
"""
import numpy as np
import pandas as pd
import os
import pickle
import logging
from typing import Tuple, Dict, List
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MiceProteinTrainer:
    """Trainer for mice protein expression classification models"""

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.pca = None
        self.label_encoders = {}
        self.models = {}

    def load_dataset(self, url: str = None, filepath: str = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Load training dataset"""
        if url:
            logger.info(f"Loading dataset from {url}")
            dataset = pd.read_csv(url)
        elif filepath:
            logger.info(f"Loading dataset from {filepath}")
            dataset = pd.read_csv(filepath)
        else:
            raise ValueError("Either url or filepath must be provided")

        logger.info(f"Dataset shape: {dataset.shape}")
        logger.info(f"Columns: {dataset.columns.tolist()}")

        # Extract features and targets
        X = dataset.iloc[:, :-2].values
        y1 = dataset.iloc[:, -2].values  # Binary data
        y2 = dataset.iloc[:, -1].values  # Four class data

        return X, y1, y2

    def preprocess_data(self, X: np.ndarray, y1: np.ndarray, y2: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Preprocess data: handle missing values and encode labels
        """
        logger.info("Starting data preprocessing...")

        # Handle missing values
        logger.info("Imputing missing values...")
        imputer = SimpleImputer(strategy='mean')
        X = imputer.fit_transform(X)

        # Encode categorical labels
        logger.info("Encoding labels...")
        le1 = LabelEncoder()
        y1 = le1.fit_transform(y1)
        self.label_encoders['binary'] = le1

        le2 = LabelEncoder()
        y2 = le2.fit_transform(y2)
        self.label_encoders['multiclass'] = le2

        logger.info(f"Preprocessed data shape: {X.shape}")
        return X, y1, y2

    def reduce_features(self, X: np.ndarray, n_components: int = 37) -> np.ndarray:
        """Apply PCA for dimensionality reduction"""
        logger.info(f"Applying PCA to reduce features to {n_components} components...")
        logger.info(f"Original features: {X.shape[1]}")

        self.pca = PCA(n_components=n_components)
        X_transformed = self.pca.fit_transform(X)

        logger.info(f"Reduced features shape: {X_transformed.shape}")
        logger.info(f"Explained variance ratio: {self.pca.explained_variance_ratio_.sum():.4f}")

        return X_transformed

    def train_models(self, X: np.ndarray, y1: np.ndarray, y2: np.ndarray, use_gridsearch: bool = True):
        """Train models using GridSearchCV"""
        logger.info("Training models...")

        model_params = {
            'logreg': {
                'model': LogisticRegression(solver='liblinear', multi_class='auto', max_iter=1000),
                'params': {
                    'C': [0.01, 0.1, 1, 10, 20, 30],
                }
            },
            'mlp': {
                'model': MLPClassifier(max_iter=5000, activation='relu', solver='adam', random_state=self.random_state),
                'params': {
                    'hidden_layer_sizes': [(10,), (30,), (50,), (70,)],
                    'alpha': [0.0001, 0.001, 0.01, 0.1, 1]
                }
            },
            'svm': {
                'model': SVC(gamma='auto'),
                'params': {
                    'C': [1, 2, 4, 6, 8, 10],
                    'kernel': ['rbf', 'linear', 'poly'],
                    'degree': [3, 5, 8]
                }
            },
            'rf': {
                'model': RandomForestClassifier(random_state=self.random_state),
                'params': {
                    'n_estimators': [50, 100, 150, 200],
                    'max_depth': [10, 20, 30, 40, 50]
                }
            }
        }

        results_binary = []
        results_multiclass = []

        for model_name, mp in model_params.items():
            logger.info(f"\nTraining {model_name}...")

            if use_gridsearch:
                # Binary classification
                logger.info(f"  GridSearchCV for binary classification...")
                clf1 = GridSearchCV(mp['model'], mp['params'], cv=5, n_jobs=-1, verbose=1)
                clf1.fit(X, y1)
                self.models[f'{model_name}_binary'] = clf1.best_estimator_
                results_binary.append({
                    'model': model_name,
                    'best_score': clf1.best_score_,
                    'best_params': clf1.best_params_
                })
                logger.info(f"    Binary - Best Score: {clf1.best_score_:.4f}")

                # Multi-class classification
                logger.info(f"  GridSearchCV for multi-class classification...")
                clf2 = GridSearchCV(mp['model'], mp['params'], cv=5, n_jobs=-1, verbose=1)
                clf2.fit(X, y2)
                self.models[f'{model_name}_4class'] = clf2.best_estimator_
                results_multiclass.append({
                    'model': model_name,
                    'best_score': clf2.best_score_,
                    'best_params': clf2.best_params_
                })
                logger.info(f"    Multi-class - Best Score: {clf2.best_score_:.4f}")
            else:
                # Train with default parameters
                model_binary = mp['model']
                model_multiclass = mp['model'].__class__(**mp['model'].get_params())

                model_binary.fit(X, y1)
                model_multiclass.fit(X, y2)

                self.models[f'{model_name}_binary'] = model_binary
                self.models[f'{model_name}_4class'] = model_multiclass

        logger.info("\n=== Binary Classification Results ===")
        for result in results_binary:
            logger.info(f"{result['model']}: {result['best_score']:.4f}")

        logger.info("\n=== Multi-class Classification Results ===")
        for result in results_multiclass:
            logger.info(f"{result['model']}: {result['best_score']:.4f}")

    def save_models(self, save_dir: str = "models/saved_models"):
        """Save trained models and PCA to disk"""
        os.makedirs(save_dir, exist_ok=True)
        logger.info(f"Saving models to {save_dir}...")

        # Save models
        for model_name, model in self.models.items():
            filepath = os.path.join(save_dir, f"{model_name}.pkl")
            with open(filepath, 'wb') as f:
                pickle.dump(model, f)
            logger.info(f"  Saved: {model_name}")

        # Save PCA
        pca_path = os.path.join(save_dir, 'pca_37.pkl')
        with open(pca_path, 'wb') as f:
            pickle.dump(self.pca, f)
        logger.info(f"  Saved: PCA transformer")

    def evaluate_on_test(self, X_test: np.ndarray, y1_test: np.ndarray, y2_test: np.ndarray) -> Dict:
        """Evaluate models on test set"""
        from sklearn.metrics import accuracy_score, confusion_matrix

        logger.info("\n=== Test Set Evaluation ===")

        # Preprocess test data
        imputer = SimpleImputer(strategy='mean')
        X_test = imputer.fit_transform(X_test)
        X_test = self.pca.transform(X_test)

        results = {}

        # Binary classification
        logger.info("\nBinary Classification:")
        for model_name in ['logreg_binary', 'mlp_binary', 'svm_binary', 'rf_binary']:
            if model_name in self.models:
                model = self.models[model_name]
                y_pred = model.predict(X_test)
                acc = accuracy_score(y1_test, y_pred)
                results[model_name] = acc
                logger.info(f"  {model_name}: {acc:.4f}")

        # Multi-class classification
        logger.info("\nMulti-class Classification:")
        for model_name in ['logreg_4class', 'mlp_4class', 'svm_4class', 'rf_4class']:
            if model_name in self.models:
                model = self.models[model_name]
                y_pred = model.predict(X_test)
                acc = accuracy_score(y2_test, y_pred)
                results[model_name] = acc
                logger.info(f"  {model_name}: {acc:.4f}")

        return results

    def train_full_pipeline(self, train_url: str, test_url: str = None, reduce_features: bool = True):
        """Run complete training pipeline"""
        logger.info("Starting full training pipeline...")

        # Load training data
        X_train, y1_train, y2_train = self.load_dataset(url=train_url)

        # Preprocess
        X_train, y1_train, y2_train = self.preprocess_data(X_train, y1_train, y2_train)

        # Feature reduction
        if reduce_features:
            X_train = self.reduce_features(X_train, n_components=37)

        # Train models
        self.train_models(X_train, y1_train, y2_train, use_gridsearch=True)

        # Save models
        self.save_models()

        # Evaluate on test set if provided
        if test_url:
            X_test, y1_test, y2_test = self.load_dataset(url=test_url)
            X_test, y1_test, y2_test = self.preprocess_data(X_test, y1_test, y2_test)
            if reduce_features:
                X_test = self.reduce_features(X_test, n_components=37)
            self.evaluate_on_test(X_test, y1_test, y2_test)

        logger.info("Training pipeline completed!")


def main():
    """Main training function"""
    trainer = MiceProteinTrainer(random_state=42)

    # URLs for datasets
    train_url = 'https://www.ee.iitb.ac.in/~asethi/Dump/MouseTrain.csv'
    test_url = 'https://www.ee.iitb.ac.in/~asethi/Dump/MouseTest.csv'

    # Run training pipeline
    trainer.train_full_pipeline(train_url=train_url, test_url=test_url, reduce_features=True)


if __name__ == "__main__":
    main()
