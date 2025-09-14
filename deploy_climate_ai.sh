#!/bin/bash
# Climate AI Deployment Script for Production

echo "🌐 CLIMATE.AI NEURAL PREDICTION SYSTEM - DEPLOYMENT"
echo "===================================================="

# Set project directory
PROJECT_DIR="/path/to/your/project"
cd "$PROJECT_DIR"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Generate data if needed
if [ ! -f "data/combined_climate.csv" ]; then
    echo "🔄 Generating sample data..."
    python src/generate_sample_data.py
fi

# Train models if needed
if [ ! -f "data/prophet_Delhi_temperature.joblib" ]; then
    echo "🧠 Training AI models..."
    python src/modeling.py
fi

# Set environment variables
export STREAMLIT_SERVER_PORT=8503
export STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Start the dashboard
echo "🚀 Starting Climate AI dashboard..."
echo "Dashboard available at: http://localhost:8503"

streamlit run src/dashboard_futuristic.py --server.port 8503 --server.address 0.0.0.0