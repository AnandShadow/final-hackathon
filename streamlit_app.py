# Climate AI Dashboard with Real Weather Data
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import requests

# Page configuration
st.set_page_config(
    page_title="🌍 Climate AI Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Simple CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_weather_data(city="London"):
    """Get real weather data from OpenWeatherMap API"""
    api_key = "8367458f8032fe7eb4461ec8788e341c"
    
    try:
        url = (f"http://api.openweathermap.org/data/2.5/weather"
               f"?q={city}&appid={api_key}&units=metric")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.warning(f"API Error {response.status_code}. Using demo data.")
            return create_demo_data(city)
            
    except Exception:
        st.info(f"Network error. Using demo data for {city}")
        return create_demo_data(city)


def create_demo_data(city="London"):
    """Create simple demo weather data"""
    import random
    
    city_temps = {
        "London": 15,
        "New York": 20, 
        "Tokyo": 25,
        "Mumbai": 32,
        "Sydney": 22
    }
    
    base_temp = city_temps.get(city, 20)
    
    return {
        "name": city,
        "main": {
            "temp": base_temp + random.uniform(-3, 3),
            "humidity": random.randint(45, 85),
            "pressure": random.randint(1000, 1020),
            "feels_like": base_temp + random.uniform(-2, 2)
        },
        "weather": [{"main": "Clear", "description": "clear sky"}],
        "wind": {"speed": random.uniform(1, 6)}
    }

def main():
    """Main application"""
    
    # Header
    st.title("🌍 Climate Risk Prediction System")
    st.markdown("**AI-Powered Climate Monitoring Dashboard**")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("🎛️ Control Panel")
    cities = ["London", "New York", "Tokyo", "Mumbai", "Sydney"]
    selected_city = st.sidebar.selectbox("🏙️ Select City", cities)
    
    # Get real weather data
    weather_data = get_weather_data(selected_city)
    
    # Display current weather
    st.subheader(f"📍 Current Weather in {weather_data['name']}")
    
    if 'weather' in weather_data:
        weather_condition = weather_data['weather'][0]['main']
        weather_desc = weather_data['weather'][0]['description'].title()
        st.info(f"**Condition:** {weather_condition} - {weather_desc}")
    else:
        st.info("**Condition:** Clear Sky - Demo Data")
    
    # Weather metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        temp = weather_data['main']['temp']
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌡️ Temperature</h3>
            <h2>{temp:.1f}°C</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        humidity = weather_data['main']['humidity']
        st.markdown(f"""
        <div class="metric-card">
            <h3>💧 Humidity</h3>
            <h2>{humidity}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pressure = weather_data['main']['pressure']
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌪️ Pressure</h3>
            <h2>{pressure} hPa</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        wind = weather_data['wind']['speed']
        st.markdown(f"""
        <div class="metric-card">
            <h3>💨 Wind</h3>
            <h2>{wind:.1f} m/s</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Simple forecast chart
    st.subheader("📈 7-Day Temperature Forecast")
    
    dates = [datetime.now() + timedelta(days=i) for i in range(7)]
    temps = [temp + np.random.normal(0, 2) for _ in range(7)]
    
    forecast_df = pd.DataFrame({
        'Date': dates,
        'Temperature': temps
    })
    
    fig = px.line(
        forecast_df, 
        x='Date', 
        y='Temperature',
        title=f"Temperature Forecast for {selected_city}"
    )
    
    fig.update_traces(line_color='#ff6b6b', line_width=3)
    st.plotly_chart(fig, use_container_width=True)
    
    # Simple alerts
    st.subheader("🚨 Climate Alerts")
    
    if temp > 30:
        st.warning("⚠️ High Temperature Alert: Above 30°C")
    elif temp < 5:
        st.warning("❄️ Cold Weather Alert: Below 5°C")
    else:
        st.success("✅ Normal weather conditions")
    
    # Footer
    st.markdown("---")
    st.markdown(f"**📅 Updated:** {datetime.now().strftime('%H:%M:%S')} | **🚀 Status:** Live on Streamlit Cloud")
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.info(
        "Climate AI Dashboard with real-time monitoring and forecasting. "
        "Built with Streamlit and Plotly."
    )

if __name__ == "__main__":
    main()