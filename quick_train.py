"""
Quick training script - trains models fast for quick demo/testing
Run this first to generate pkl files needed for FastAPI
"""
import os
import sys
import pickle
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("QUICK TRAINING - Mice Protein Expression Classification")
print("=" * 70)


def train_quick():
    """Quick training with optimized parameters"""
    
    print("\n[1/5] Loading dataset...")
    try:
        # Download dataset
        url = 'https://www.ee.iitb.ac.in/~asethi/Dump/MouseTrain.csv'
        dataset = pd.read_csv(url)
        print(f"✓ Dataset loaded: {dataset.shape}")
    except Exception as e:
        print(f"✗ Error loading dataset: {e}")
        return False
    
    # Extract features and targets
    X = dataset.iloc[:, :-2].values
    y1 = dataset.iloc[:, -2].values  # Binary
    y2 = dataset.iloc[:, -1].values  # Multi-class
    
    print("\n[2/5] Preprocessing data...")
    # Impute missing values
    imputer = SimpleImputer(strategy='mean')
    X = imputer.fit_transform(X)
    
    # Encode labels
    le1 = LabelEncoder()
    y1 = le1.fit_transform(y1)
    
    le2 = LabelEncoder()
    y2 = le2.fit_transform(y2)
    
    print(f"✓ Features shape: {X.shape}")
    
    print("\n[3/5] Applying PCA (77 → 37 features)...")
    pca = PCA(n_components=37, random_state=42)
    X = pca.fit_transform(X)
    print(f"✓ PCA applied. Explained variance: {pca.explained_variance_ratio_.sum():.4f}")
    
    # Create models directory
    models_dir = os.path.join(os.path.dirname(__file__), 'models', 'saved_models')
    os.makedirs(models_dir, exist_ok=True)
    
    print("\n[4/5] Training models (using default parameters for speed)...")
    
    # Binary classification models
    print("  • Training Binary Models...")
    
    logreg_binary = LogisticRegression(solver='liblinear', multi_class='auto', max_iter=1000, random_state=42, C=20)
    logreg_binary.fit(X, y1)
    
    mlp_binary = MLPClassifier(max_iter=5000, activation='relu', solver='adam', random_state=42, 
                               hidden_layer_sizes=(30,), alpha=0.0001)
    mlp_binary.fit(X, y1)
    
    svm_binary = SVC(gamma='auto', C=4, kernel='linear', random_state=42, probability=True)
    svm_binary.fit(X, y1)
    
    rf_binary = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf_binary.fit(X, y1)
    
    # Multi-class classification models
    print("  • Training Multi-class Models...")
    
    logreg_4class = LogisticRegression(solver='liblinear', multi_class='auto', max_iter=1000, random_state=42, C=30)
    logreg_4class.fit(X, y2)
    
    mlp_4class = MLPClassifier(max_iter=5000, activation='relu', solver='adam', random_state=42, 
                               hidden_layer_sizes=(50,), alpha=0.01)
    mlp_4class.fit(X, y2)
    
    svm_4class = SVC(gamma='auto', C=8, kernel='rbf', random_state=42, probability=True)
    svm_4class.fit(X, y2)
    
    rf_4class = RandomForestClassifier(n_estimators=100, max_depth=50, random_state=42)
    rf_4class.fit(X, y2)
    
    print("\n[5/5] Saving models...")
    
    # Save binary models
    models_to_save = {
        'logreg_binary.pkl': logreg_binary,
        'mlp_binary.pkl': mlp_binary,
        'svm_binary.pkl': svm_binary,
        'rf_binary.pkl': rf_binary,
        'logreg_4class.pkl': logreg_4class,
        'mlp_4class.pkl': mlp_4class,
        'svm_4class.pkl': svm_4class,
        'rf_4class.pkl': rf_4class,
        'pca_37.pkl': pca,
        'imputer.pkl': imputer
    }
    
    for filename, model in models_to_save.items():
        filepath = os.path.join(models_dir, filename)
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
        print(f"  ✓ {filename}")
    
    # Test with train data
    print("\n[BONUS] Testing on training data...")
    y1_pred = svm_binary.predict(X)
    y2_pred = svm_4class.predict(X)
    
    from sklearn.metrics import accuracy_score
    acc1 = accuracy_score(y1, y1_pred)
    acc2 = accuracy_score(y2, y2_pred)
    
    print(f"  Binary Classification: {acc1:.4f} accuracy")
    print(f"  Multi-class Classification: {acc2:.4f} accuracy")
    
    print("\n" + "=" * 70)
    print("✓ TRAINING COMPLETE!")
    print("=" * 70)
    print("\nNow run FastAPI with:")
    print("  uvicorn app.main:app --reload")
    print("\nThen visit: http://localhost:8000/docs")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    try:
        success = train_quick()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Training failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
