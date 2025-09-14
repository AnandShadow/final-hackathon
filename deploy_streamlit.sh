#!/bin/bash

# Climate AI Deployment Script for GitHub/Streamlit Cloud

echo "🚀 Deploying Climate Risk Prediction AI System..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create data directories if they don't exist
echo "📁 Setting up data directories..."
mkdir -p data/raw data/processed data/models logs

# Generate sample data if needed
echo "🔄 Generating sample data..."
python src/generate_sample_data.py

# Run initial data preprocessing
echo "⚙️ Preprocessing data..."
python src/data_preprocessing.py

# Train models
echo "🧠 Training AI models..."
python src/modeling.py

echo "✅ Deployment complete!"
echo "🎯 Run 'streamlit run src/dashboard_futuristic.py' to start the dashboard"
echo "🌐 Or deploy to Streamlit Cloud: https://share.streamlit.io"