"""
Generate valid sample data with EXACTLY 77 features for testing
"""
import json

# CORRECT: Exactly 77 features (75 proteins + genotype + treatment columns)
SAMPLE_77_FEATURES = [
    0.503, -0.196, 0.230, -0.226, -0.186, -0.107, -0.035, -0.052, -0.064, 0.006,
    -0.132, -0.156, -0.121, -0.178, -0.146, -0.241, -0.103, 0.041, 0.195, 0.223,
    0.106, 0.187, 0.245, 0.156, 0.089, 0.121, 0.134, 0.178, 0.164, 0.129,
    0.087, 0.145, 0.156, 0.198, 0.234, 0.201, 0.167, 0.145, 0.176, 0.198,
    0.134, 0.156, 0.178, 0.201, 0.089, 0.112, 0.145, 0.134, 0.167, 0.189,
    0.156, 0.178, 0.145, 0.123, 0.167, 0.198, 0.156, 0.134, 0.189, 0.167,
    0.145, 0.178, 0.201, 0.156, -0.089, -0.145, -0.123, -0.087, -0.112, -0.134,
    -0.156, -0.178, -0.167, 0.234, 0.156  # 75 protein features
    # Missing 2 more - Adding them:
]

# Count = 75, need 2 more
SAMPLE_77_FEATURES.extend([0.145, 0.189])  # Add 2 more features = 77 total

print(f"✅ Total Features: {len(SAMPLE_77_FEATURES)}")
print(f"\n📋 Sample Input for /predict (Single):")
print(json.dumps({
    "features": SAMPLE_77_FEATURES,
    "model_type": "svm",
    "classification_type": "binary"
}, indent=2))

print(f"\n📋 Sample Input for /batch_predict (Multiple):")
print(json.dumps({
    "features": [SAMPLE_77_FEATURES, SAMPLE_77_FEATURES],
    "model_type": "svm",
    "classification_type": "binary"
}, indent=2))
