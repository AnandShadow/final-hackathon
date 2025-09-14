@echo off
echo Starting Climate AI Prediction System...
echo.

REM Change to project directory
cd /d "C:\Users\91770\Documents\Hackathons"

REM Check if data exists, if not generate sample data
if not exist "data\combined_climate.csv" (
    echo Generating sample data...
    python src\generate_sample_data.py
)

REM Check if models exist, if not train them
if not exist "data\prophet_Delhi_temperature.joblib" (
    echo Training AI models...
    python src\modeling.py
)

REM Start the futuristic dashboard
echo.
echo ============================================
echo 🌐 CLIMATE.AI NEURAL PREDICTION SYSTEM
echo ============================================
echo.
echo Starting futuristic dashboard...
echo Dashboard will be available at: http://localhost:8503
echo.
echo Press Ctrl+C to stop the system
echo.

streamlit run src\dashboard_futuristic.py --server.port 8503

pause