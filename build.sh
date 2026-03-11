#!/bin/bash
# Render.com build script - trains models on first deployment

echo "Starting build process..."
pip install -r requirements.txt

# Check if models exist
if [ ! -f "models/saved_models/svm_binary.pkl" ]; then
    echo "Models not found. Training models..."
    python quick_train.py
else
    echo "Models already exist. Skipping training."
fi

echo "Build complete!"
