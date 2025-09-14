# Ultra-Simple Climate Dashboard - No Dependencies
import streamlit as st
from datetime import datetime

# Page setup
st.set_page_config(
    page_title="🌍 Climate AI Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Basic styling
st.markdown("""
<style>
.big-font {
    font-size: 30px !important;
    color: #1f77b4;
    text-align: center;
}
.metric-box {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.title("🌍 Climate AI Dashboard")
    st.markdown('<p class="big-font">AI-Powered Weather Monitoring</p>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("🎛️ Controls")
    cities = ["London", "New York", "Tokyo", "Mumbai", "Sydney"]
    selected_city = st.sidebar.selectbox("🏙️ Select City", cities)
    
    # Simple weather data (hardcoded for reliability)
    weather_data = {
        "London": {"temp": 15, "humidity": 70, "condition": "Cloudy"},
        "New York": {"temp": 22, "humidity": 60, "condition": "Clear"},
        "Tokyo": {"temp": 28, "humidity": 75, "condition": "Partly Cloudy"},
        "Mumbai": {"temp": 34, "humidity": 85, "condition": "Hot & Humid"},
        "Sydney": {"temp": 24, "humidity": 55, "condition": "Clear"}
    }
    
    city_data = weather_data[selected_city]
    
    # Display current weather
    st.subheader(f"📍 Current Weather in {selected_city}")
    st.info(f"**Condition:** {city_data['condition']}")
    
    # Weather metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <h3>🌡️ Temperature</h3>
            <h2>{city_data['temp']}°C</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <h3>💧 Humidity</h3>
            <h2>{city_data['humidity']}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-box">
            <h3>📊 Status</h3>
            <h2>✅ Normal</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Simple forecast
    st.subheader("📈 Weekly Forecast")
    
    forecast_temps = [city_data['temp'] + i - 3 for i in range(7)]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📅 Temperature Forecast:**")
        for i, day in enumerate(days):
            temp = forecast_temps[i]
            st.write(f"**{day}:** {temp}°C")
    
    with col2:
        st.markdown("**📊 Simple Chart:**")
        # Create a simple text-based chart
        for i, temp in enumerate(forecast_temps):
            bars = "█" * max(1, int(temp / 3))
            st.write(f"{days[i]}: {bars} ({temp}°C)")
    
    # Climate alerts
    st.subheader("🚨 Climate Alerts")
    
    temp = city_data['temp']
    if temp > 30:
        st.warning(f"⚠️ High Temperature Alert: {temp}°C in {selected_city}")
    elif temp < 10:
        st.warning(f"❄️ Cold Weather Alert: {temp}°C in {selected_city}")
    else:
        st.success(f"✅ Normal temperature conditions in {selected_city}")
    
    if city_data['humidity'] > 80:
        st.warning(f"💧 High Humidity Alert: {city_data['humidity']}%")
    
    # Footer
    st.markdown("---")
    current_time = datetime.now().strftime('%H:%M:%S')
    st.markdown(f"**🕐 Last Updated:** {current_time} | **🚀 Status:** Live")
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.info("Simple Climate AI Dashboard - monitoring weather "
                    "conditions across major cities.")
    
    st.sidebar.markdown("### 🌍 Cities")
    for city in cities:
        emoji = "⭐" if city == selected_city else "📍"
        st.sidebar.write(f"{emoji} {city}")

if __name__ == "__main__":
    main()