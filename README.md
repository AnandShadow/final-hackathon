# Climate Risk Prediction AI System

## Overview
A complete Python-based AI system for climate risk prediction that collects real-time climate data, trains forecasting models, sends alerts, and provides an interactive dashboard for visualization.

## Features
- **Data Collection**: Real-time data from OpenWeatherMap & AQICN APIs
- **Forecasting**: Prophet models for temperature, humidity, rainfall, AQI
- **Alerts**: Email/SMS notifications when thresholds are exceeded
- **Dashboard**: Interactive Streamlit visualization
- **Automation**: Scheduled pipeline execution with logging

## Project Structure
```
├── data/
│   ├── realtime_climate.csv      # Real-time API data
│   ├── combined_climate.csv      # Historical + real-time data
│   ├── processed_climate.csv     # Cleaned data
│   └── prophet_*.joblib          # Trained models
├── src/
│   ├── data_collection.py        # API data fetching
│   ├── generate_sample_data.py   # Synthetic data generation
│   ├── data_preprocessing.py     # Data cleaning
│   ├── modeling.py               # Prophet model training
│   ├── alert_system.py           # Email/SMS alerts
│   ├── dashboard.py              # Streamlit dashboard
│   └── automation.py             # Pipeline automation
├── logs/
│   └── climate_pipeline.log      # Automation logs
├── .env                          # API keys and credentials
├── requirements.txt              # Python dependencies
└── run_climate_pipeline.bat      # Windows Task Scheduler script
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Edit `.env` file with your credentials:
```env
OPENWEATHER_API_KEY=your_openweather_api_key
AQICN_API_KEY=your_aqicn_api_key
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
TWILIO_SID=your_twilio_sid
TWILIO_TOKEN=your_twilio_token
TWILIO_PHONE=your_twilio_phone
```

**API Key Setup:**
- OpenWeatherMap: Get free API key at https://openweathermap.org/api
- AQICN: Get token at https://aqicn.org/data-platform/token/
- Gmail: Use App Passwords (2FA required) at https://myaccount.google.com/apppasswords
- Twilio: Get credentials at https://www.twilio.com/console

### 3. Generate Sample Data
```bash
python src/generate_sample_data.py
```

### 4. Train Models
```bash
python src/modeling.py
```

## Usage

### Manual Execution
```bash
# Collect real-time data
python src/data_collection.py

# Preprocess data
python src/data_preprocessing.py

# Train forecasting models
python src/modeling.py

# Test alert system
python src/alert_system.py

# Launch dashboard
streamlit run src/dashboard.py
```

### Automated Pipeline
```bash
# Run pipeline once
python src/automation.py --run-once

# Create Windows Task Scheduler script
python src/automation.py --create-task

# Run continuous scheduling (development)
python src/automation.py
```

## Dashboard Features
- **Interactive plots** for temperature, humidity, rainfall, AQI
- **24-72 hour forecasts** with confidence intervals
- **Real-time alerts** when thresholds are exceeded
- **Summary statistics** and recent data tables
- **Multi-city support** (Delhi, Mumbai, London, New York)

Access at: http://localhost:8501

## Alert Thresholds
| Metric | High Threshold | Low Threshold |
|--------|----------------|---------------|
| Temperature | 40°C | 0°C |
| AQI | 200 | 0 |
| Rainfall | 50mm | 0mm |
| Humidity | 95% | 10% |

## Deployment Options

### Windows Task Scheduler
1. Run `python src/automation.py --create-task`
2. Open Task Scheduler → Create Basic Task
3. Set schedule (e.g., daily at 6 AM)
4. Action: Start a program
5. Program: `C:\path\to\run_climate_pipeline.bat`

### Linux Cron
```bash
# Edit crontab
crontab -e

# Add daily execution at 6 AM
0 6 * * * cd /path/to/project && python src/automation.py --run-once
```

### Cloud Deployment
- **Azure Functions**: Timer-triggered pipeline execution
- **AWS Lambda**: Scheduled EventBridge triggers
- **Google Cloud Functions**: Pub/Sub or Scheduler triggers

## Model Performance
- **Prophet MAE**: ~1.47°C for temperature forecasting
- **Forecast Horizon**: 24-72 hours
- **Training Data**: 30 days synthetic + real-time data
- **Update Frequency**: Models retrain when insufficient data

## Troubleshooting

### Common Issues
1. **API Authentication Errors**: Check `.env` credentials
2. **Insufficient Data**: Run `python src/generate_sample_data.py`
3. **Missing Models**: Run `python src/modeling.py`
4. **Dashboard Not Loading**: Ensure all dependencies installed

### Logs
Check `logs/climate_pipeline.log` for detailed execution logs.

## Security Best Practices
- Keep `.env` file secure and never commit to version control
- Use App Passwords for Gmail instead of account password
- Rotate API keys regularly
- Limit file permissions on credential files

## License
MIT License

## Support
For issues or questions, check the logs directory or review the error messages in the console output.