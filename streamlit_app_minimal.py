# Minimal Climate AI Dashboard - Streamlit Cloud Compatible
import streamlit as st
from datetime import datetime
import random
import math

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
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
    }
    .metric-card h2 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .alert-success {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
    }
    .alert-warning {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ffeaa7;
    }
</style>
""", unsafe_allow_html=True)


def get_weather_data(city):
    """Generate realistic weather data for demo"""
    # Set seed based on city for consistent data
    random.seed(hash(city) % 1000)
    
    city_data = {
        "London": {"base_temp": 15, "humidity": 70, "condition": "Cloudy"},
        "New York": {"base_temp": 20, "humidity": 60, "condition": "Clear"},
        "Tokyo": {"base_temp": 25, "humidity": 65, "condition": "Partly Cloudy"},
        "Mumbai": {"base_temp": 32, "humidity": 80, "condition": "Hot"},
        "Sydney": {"base_temp": 22, "humidity": 55, "condition": "Clear"}
    }
    
    data = city_data.get(city, {"base_temp": 20, "humidity": 60, "condition": "Clear"})
    
    return {
        "name": city,
        "temperature": round(data["base_temp"] + random.uniform(-3, 3), 1),
        "humidity": data["humidity"] + random.randint(-10, 10),
        "pressure": 1013 + random.randint(-15, 15),
        "wind_speed": round(random.uniform(1, 8), 1),
        "condition": data["condition"]
    }


def generate_forecast(base_temp, days=7):
    """Generate simple forecast data"""
    forecast = []
    current_date = datetime.now()
    
    for i in range(days):
        date = current_date.replace(day=current_date.day + i)
        # Simple sine wave variation
        temp_variation = math.sin(i * 0.5) * 3 + random.uniform(-2, 2)
        temp = round(base_temp + temp_variation, 1)
        
        forecast.append({
            "date": date.strftime("%m/%d"),
            "temperature": temp,
            "day": date.strftime("%a")
        })
    
    return forecast


def main():
    """Main application function"""
    
    # Header
    st.title("🌍 Climate Risk Prediction System")
    st.markdown("**AI-Powered Climate Monitoring Dashboard**")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("🎛️ Control Panel")
    cities = ["London", "New York", "Tokyo", "Mumbai", "Sydney"]
    selected_city = st.sidebar.selectbox("🏙️ Select City", cities)
    
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()
    
    # Get weather data
    weather_data = get_weather_data(selected_city)
    
    # Current Weather Section
    st.subheader(f"📍 Current Weather in {weather_data['name']}")
    st.info(f"**Condition:** {weather_data['condition']}")
    
    # Weather Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌡️ Temperature</h3>
            <h2>{weather_data['temperature']}°C</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💧 Humidity</h3>
            <h2>{weather_data['humidity']}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌪️ Pressure</h3>
            <h2>{weather_data['pressure']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💨 Wind</h3>
            <h2>{weather_data['wind_speed']} m/s</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Forecast Section
    st.subheader("📈 7-Day Temperature Forecast")
    
    forecast_data = generate_forecast(weather_data['temperature'])
    
    # Simple table display
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📅 Forecast Table**")
        for day_data in forecast_data:
            st.write(f"**{day_data['day']} {day_data['date']}:** {day_data['temperature']}°C")
    
    with col2:
        st.markdown("**📊 Temperature Trend**")
        temps = [day['temperature'] for day in forecast_data]
        days = [day['day'] for day in forecast_data]
        
        # Simple line chart using built-in Streamlit
        chart_data = {}
        for i, day in enumerate(days):
            chart_data[day] = temps[i]
        
        st.bar_chart(chart_data)
    
    # Climate Alerts
    st.subheader("🚨 Climate Risk Assessment")
    
    temp = weather_data['temperature']
    humidity = weather_data['humidity']
    
    if temp > 30:
        st.markdown("""
        <div class="alert-warning">
            ⚠️ <strong>High Temperature Alert:</strong> Temperature above 30°C detected.
        </div>
        """, unsafe_allow_html=True)
    elif temp < 5:
        st.markdown("""
        <div class="alert-warning">
            ❄️ <strong>Cold Weather Alert:</strong> Temperature below 5°C detected.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-success">
            ✅ <strong>Normal Conditions:</strong> All weather parameters are within normal range.
        </div>
        """, unsafe_allow_html=True)
    
    if humidity > 80:
        st.markdown("""
        <div class="alert-warning">
            💧 <strong>High Humidity Alert:</strong> Humidity above 80% detected.
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🔗 Status:** ✅ Live on Streamlit Cloud")
    
    with col2:
        st.markdown(f"**📅 Updated:** {datetime.now().strftime('%H:%M:%S')}")
    
    with col3:
        st.markdown("**🚀 Version:** v3.0 Minimal")
    
    # Sidebar Info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.info(
        "Climate AI Dashboard with weather monitoring and forecasting. "
        "Features real-time data simulation and risk assessment for major cities worldwide."
    )
    
    st.sidebar.markdown("### 🏙️ Available Cities")
    for city in cities:
        emoji = "🌟" if city == selected_city else "📍"
        st.sidebar.write(f"{emoji} {city}")


if __name__ == "__main__":
    main()