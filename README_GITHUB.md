# Climate Risk Prediction AI System 🌐

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)

A complete Python-based AI system for climate risk prediction with real-time data collection, forecasting models, alert systems, and a futuristic dashboard.

## 🚀 Live Demo

**Futuristic Dashboard**: [Deploy on Streamlit Cloud](https://streamlit.io/cloud)

## ✨ Features

- **🌡️ Real-time Data Collection**: OpenWeatherMap & AQICN APIs
- **🧠 AI Forecasting**: Prophet models with MAE ~1.47°C 
- **🚨 Smart Alerts**: Email/SMS notifications for risk events
- **🎛️ Futuristic Dashboard**: Cyberpunk-styled interactive interface
- **⚡ Automation**: Scheduled pipeline execution with logging
- **📊 Multi-metric Support**: Temperature, humidity, rainfall, AQI

## 🎯 Quick Start

### Option 1: One-Click Streamlit Deployment

[![Deploy](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy)

1. Fork this repository
2. Connect to Streamlit Cloud
3. Deploy with one click!

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/AnandShadow/final-hackathon.git
cd final-hackathon

# Install dependencies
pip install -r requirements.txt

# Run the deployment script
./deploy_climate_ai.bat  # Windows
# or
./deploy_climate_ai.sh   # Linux/Mac
```

### Option 3: Docker Deployment

```bash
# Build and run with Docker
docker-compose up -d

# Access at http://localhost:8503
```

## 🔧 Configuration

1. **Get API Keys**:
   - [OpenWeatherMap API](https://openweathermap.org/api) - Free tier available
   - [AQICN API](https://aqicn.org/data-platform/token/) - Free token

2. **Update Secrets** (for Streamlit Cloud):
   ```toml
   # .streamlit/secrets.toml
   OPENWEATHER_API_KEY = "your_key_here"
   AQICN_API_KEY = "your_token_here"
   ```

3. **Local Setup**:
   ```env
   # .env
   OPENWEATHER_API_KEY=your_openweather_api_key
   AQICN_API_KEY=your_aqicn_api_key
   ```

## 📊 Screenshots

### Futuristic Dashboard
![Dashboard](https://via.placeholder.com/800x400/0a0a0a/00ffff?text=Climate.AI+Neural+Dashboard)

### Alert System
![Alerts](https://via.placeholder.com/400x300/1a1a2e/ff0080?text=Smart+Alert+System)

## 🏗️ Architecture

```
├── src/
│   ├── dashboard_futuristic.py    # Main dashboard
│   ├── data_collection.py         # API data fetching
│   ├── modeling.py               # Prophet forecasting
│   ├── alert_system.py           # Smart notifications
│   └── automation.py             # Pipeline automation
├── data/                         # Data storage
├── logs/                         # System logs
└── deploy_climate_ai.bat         # One-click deployment
```

## 🔮 Tech Stack

- **Frontend**: Streamlit with custom cyberpunk CSS
- **ML/AI**: Prophet, scikit-learn
- **Visualization**: Plotly with futuristic styling
- **APIs**: OpenWeatherMap, AQICN
- **Deployment**: Streamlit Cloud, Docker, Local

## 📈 Model Performance

- **Prophet MAE**: 1.47°C for temperature forecasting
- **Forecast Horizon**: 6-72 hours
- **Cities Supported**: Delhi, Mumbai, London, New York
- **Metrics**: Temperature, Humidity, Rainfall, AQI

## 🎨 Futuristic UI Features

- **Cyberpunk Theme**: Dark gradients with neon accents
- **Animations**: Glowing effects and pulsing alerts
- **Typography**: Orbitron futuristic font
- **Real-time Updates**: Live telemetry display
- **Interactive Charts**: Hover effects and smooth transitions

## 🔄 Automation

- **Data Collection**: Every 3 hours
- **Model Updates**: Daily at 6 AM
- **Alert Monitoring**: Hourly checks
- **Windows Scheduler**: Automated pipeline execution

## 🚨 Alert Thresholds

| Metric | High Risk | Medium Risk |
|--------|-----------|-------------|
| Temperature | >40°C | <0°C |
| AQI | >200 | >100 |
| Rainfall | >50mm | >25mm |
| Humidity | >95% | <10% |

## 🌍 API Integrations

- **OpenWeatherMap**: Real-time weather data
- **AQICN**: Air quality monitoring
- **Email SMTP**: Alert notifications
- **Twilio SMS**: Critical alerts (optional)

## 📱 Deployment Options

### Streamlit Cloud (Recommended)
- Free hosting for public repos
- Automatic updates from GitHub
- Built-in secrets management

### Railway
```bash
railway login
railway init
railway up
```

### Heroku
```bash
heroku create climate-ai-app
git push heroku main
```

### Azure/AWS/GCP
- Container deployment ready
- Auto-scaling support
- Production-grade infrastructure

## 🛠️ Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Code formatting
black src/
flake8 src/

# Start development server
streamlit run src/dashboard_futuristic.py --server.port 8503
```

## 📊 Monitoring & Logs

- **System Logs**: `logs/climate_pipeline.log`
- **Model Performance**: Tracked in dashboard
- **API Status**: Real-time monitoring
- **Error Handling**: Comprehensive logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

- [ ] Mobile-responsive design
- [ ] More ML models (LSTM, XGBoost)
- [ ] Additional cities and countries
- [ ] Historical data analysis
- [ ] ML model comparison dashboard
- [ ] API rate limiting and caching
- [ ] User authentication system

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/AnandShadow/final-hackathon/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AnandShadow/final-hackathon/discussions)
- **Email**: support@climate-ai.com

## 🏆 Acknowledgments

- OpenWeatherMap for weather data API
- AQICN for air quality data
- Streamlit for the amazing framework
- Prophet for time series forecasting

---

**Built with ❤️ for climate awareness and prediction**

*Deploy your own instance and help monitor climate risks worldwide!*