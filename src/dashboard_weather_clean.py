"""
dashboard_weather_clean.py
Clean weather-responsive dashboard with working animations.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import requests
import os
from datetime import datetime


def get_weather_condition(city):
    """Get current weather condition for animations"""
    try:
        api_key = os.getenv('OPENWEATHER_API_KEY', 'demo_key')
        if api_key == 'demo_key':
            # Return simulated weather for demo
            conditions = ['clear', 'rain', 'snow', 'clouds', 'thunderstorm']
            import random
            return random.choice(conditions)
        
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key}
        response = requests.get(url, params=params)
        data = response.json()
        
        weather_main = data['weather'][0]['main'].lower()
        
        # Map weather conditions to animation types
        if 'rain' in weather_main or 'drizzle' in weather_main:
            return 'rain'
        elif 'snow' in weather_main:
            return 'snow'
        elif 'thunder' in weather_main or 'storm' in weather_main:
            return 'thunderstorm'
        elif 'cloud' in weather_main:
            return 'clouds'
        else:
            return 'clear'
    except Exception:
        return 'clear'


def apply_weather_theme(weather_condition, temperature=20):
    """Apply dynamic CSS styling based on weather conditions"""
    
    # Weather-specific color schemes
    weather_themes = {
        'clear': {
            'bg': '#0a0a0a 0%, #1a1a2e 50%, #16213e 100%',
            'primary': '#00ffff',
            'particle': '#ffff00'
        },
        'rain': {
            'bg': '#0a0a0a 0%, #1a2e3a 50%, #16213e 100%',
            'primary': '#0099ff',
            'particle': '#87ceeb'
        },
        'snow': {
            'bg': '#0a0a0a 0%, #2e3a4a 50%, #4a5568 100%',
            'primary': '#ffffff',
            'particle': '#ffffff'
        },
        'thunderstorm': {
            'bg': '#0a0a0a 0%, #2e1a2e 50%, #4a1a4a 100%',
            'primary': '#ff6600',
            'particle': '#ffff00'
        },
        'clouds': {
            'bg': '#0a0a0a 0%, #2a2a3a 50%, #3a3a4a 100%',
            'primary': '#66ccff',
            'particle': '#ffffff'
        }
    }
    
    theme = weather_themes.get(weather_condition, weather_themes['clear'])
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(135deg, {theme['bg']});
        color: {theme['primary']};
        position: relative;
        overflow: hidden;
    }}
    
    /* Weather Particles */
    .weather-particles {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }}
    
    /* Rain Animation */
    .rain-drop {{
        position: absolute;
        background: linear-gradient(180deg, transparent, {theme['particle']});
        width: 2px;
        height: 50px;
        animation: rain-fall 1s linear infinite;
    }}
    
    @keyframes rain-fall {{
        0% {{ transform: translateY(-100vh); opacity: 0; }}
        10% {{ opacity: 1; }}
        90% {{ opacity: 1; }}
        100% {{ transform: translateY(100vh); opacity: 0; }}
    }}
    
    /* Snow Animation */
    .snow-flake {{
        position: absolute;
        background: {theme['particle']};
        border-radius: 50%;
        width: 6px;
        height: 6px;
        animation: snow-fall 3s linear infinite;
    }}
    
    @keyframes snow-fall {{
        0% {{ transform: translateY(-100vh) rotate(0deg); opacity: 0; }}
        10% {{ opacity: 1; }}
        90% {{ opacity: 1; }}
        100% {{ transform: translateY(100vh) rotate(360deg); opacity: 0; }}
    }}
    
    /* Lightning Animation */
    .lightning {{
        position: absolute;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent 48%, {theme['particle']} 49%, {theme['particle']} 51%, transparent 52%);
        opacity: 0;
        animation: lightning-flash 3s infinite;
    }}
    
    @keyframes lightning-flash {{
        0%, 90%, 96%, 100% {{ opacity: 0; }}
        93% {{ opacity: 0.8; }}
    }}
    
    /* Cloud Animation */
    .cloud {{
        position: absolute;
        background: radial-gradient(ellipse, rgba(255,255,255,0.2) 0%, transparent 70%);
        border-radius: 50px;
        width: 150px;
        height: 75px;
        animation: cloud-float 15s linear infinite;
    }}
    
    @keyframes cloud-float {{
        0% {{ transform: translateX(-100px); }}
        100% {{ transform: translateX(calc(100vw + 100px)); }}
    }}
    
    /* Sunny Animation */
    .sun-rays {{
        position: absolute;
        top: 50%;
        left: 50%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,0,0.1) 0%, transparent 70%);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        animation: sun-pulse 4s ease-in-out infinite;
    }}
    
    @keyframes sun-pulse {{
        0%, 100% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.3; }}
        50% {{ transform: translate(-50%, -50%) scale(1.2); opacity: 0.1; }}
    }}
    
    .main-header {{
        background: linear-gradient(90deg, {theme['primary']}, #8000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 3rem;
        text-align: center;
        animation: weather-glow 2s ease-in-out infinite alternate;
    }}
    
    .metric-card {{
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(128, 0, 255, 0.1));
        border: 1px solid {theme['primary']};
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }}
    
    .weather-indicator {{
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(0, 255, 255, 0.2);
        border: 2px solid {theme['primary']};
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        animation: weather-spin 6s linear infinite;
        z-index: 1000;
    }}
    
    @keyframes weather-glow {{
        from {{ text-shadow: 0 0 20px rgba(0, 255, 255, 0.5); }}
        to {{ text-shadow: 0 0 30px rgba(0, 255, 255, 0.8); }}
    }}
    
    @keyframes weather-spin {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    
    .alert-high {{
        background: linear-gradient(135deg, rgba(255, 0, 100, 0.3), rgba(255, 50, 50, 0.3));
        border: 2px solid #ff0066;
        border-radius: 10px;
        padding: 15px;
        animation: critical-pulse 1s infinite;
    }}
    
    @keyframes critical-pulse {{
        0% {{ box-shadow: 0 0 20px rgba(255, 0, 102, 0.5); }}
        50% {{ box-shadow: 0 0 40px rgba(255, 0, 102, 0.8); }}
        100% {{ box-shadow: 0 0 20px rgba(255, 0, 102, 0.5); }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Add weather particles based on condition
    particles_html = ""
    if weather_condition == 'rain':
        particles_html = """
        <div class="weather-particles">
        """ + "".join([f'<div class="rain-drop" style="left: {i*5}%; animation-delay: {i*0.1}s;"></div>' for i in range(20)]) + """
        </div>
        """
    elif weather_condition == 'snow':
        particles_html = """
        <div class="weather-particles">
        """ + "".join([f'<div class="snow-flake" style="left: {i*7}%; animation-delay: {i*0.2}s; animation-duration: {3+i*0.3}s;"></div>' for i in range(15)]) + """
        </div>
        """
    elif weather_condition == 'thunderstorm':
        particles_html = """
        <div class="weather-particles">
            <div class="lightning"></div>
        </div>
        """
    elif weather_condition == 'clouds':
        particles_html = """
        <div class="weather-particles">
        """ + "".join([f'<div class="cloud" style="top: {20+i*15}%; animation-delay: {i*3}s;"></div>' for i in range(4)]) + """
        </div>
        """
    elif weather_condition == 'clear':
        particles_html = """
        <div class="weather-particles">
            <div class="sun-rays"></div>
        </div>
        """
    
    # Weather indicator emoji
    weather_emojis = {
        'clear': '☀️',
        'rain': '🌧️',
        'snow': '❄️',
        'thunderstorm': '⛈️',
        'clouds': '☁️'
    }
    
    st.markdown(f"""
    {particles_html}
    <div class="weather-indicator">
        {weather_emojis.get(weather_condition, '🌤️')}
    </div>
    """, unsafe_allow_html=True)


def create_metric_card(title, value, unit=""):
    """Create a metric display card"""
    st.markdown(f"""
    <div class="metric-card">
        <h4 style='margin: 0;'>{title}</h4>
        <h2 style='color: #ffffff; margin: 5px 0;'>{value}{unit}</h2>
    </div>
    """, unsafe_allow_html=True)


def load_data():
    """Load climate data"""
    try:
        df = pd.read_csv("data/combined_climate.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except FileNotFoundError:
        st.error("Climate data not found. Please run data collection first.")
        return None


def create_weather_plot(df, city, metric, weather_condition='clear'):
    """Create weather-responsive forecast plot"""
    city_data = df[df['city'] == city].copy()
    
    # Weather-specific colors
    weather_colors = {
        'clear': '#ffaa00',
        'rain': '#0099ff',
        'snow': '#ffffff',
        'thunderstorm': '#ff6600',
        'clouds': '#66ccff'
    }
    
    color = weather_colors.get(weather_condition, '#00ffff')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=city_data['timestamp'],
        y=city_data[metric],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color=color, width=3),
        marker=dict(color=color, size=6)
    ))
    
    fig.update_layout(
        title=f'{metric.title()} - {city}',
        xaxis_title='Time',
        yaxis_title=f'{metric.title()}',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color=color),
        title_font=dict(size=20, color=color)
    )
    
    return fig


def main():
    """Main dashboard function"""
    st.set_page_config(
        page_title="Climate AI Weather System",
        page_icon="🌦️",
        layout="wide"
    )
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar
    cities = df['city'].unique()
    selected_city = st.sidebar.selectbox("🏙️ Select City", cities)
    
    # Get weather condition
    weather_condition = get_weather_condition(selected_city)
    
    # Get current temperature
    city_data = df[df['city'] == selected_city]
    if not city_data.empty:
        current_temp = city_data['temperature'].iloc[-1]
    else:
        current_temp = 20
    
    # Apply weather theme
    apply_weather_theme(weather_condition, current_temp)
    
    # Header
    st.markdown(f"""
    <h1 class="main-header">🌦️ Climate AI Weather System</h1>
    <p style='text-align: center; font-size: 1.2rem; margin-bottom: 2rem;'>
    Live Weather: {weather_condition.title()} | City: {selected_city}
    </p>
    """, unsafe_allow_html=True)
    
    if city_data.empty:
        st.error(f"No data available for {selected_city}")
        return
    
    # Latest data
    latest_data = city_data.iloc[-1]
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card(
            "🌡️ Temperature", 
            f"{latest_data['temperature']:.1f}", 
            "°C"
        )
    
    with col2:
        create_metric_card(
            "💧 Humidity", 
            f"{latest_data['humidity']:.1f}", 
            "%"
        )
    
    with col3:
        create_metric_card(
            "🌧️ Rainfall", 
            f"{latest_data['rainfall']:.1f}", 
            "mm"
        )
    
    with col4:
        aqi_value = latest_data.get('aqi', 0)
        create_metric_card(
            "🏭 Air Quality", 
            f"{aqi_value:.0f}", 
            " AQI"
        )
    
    # Charts
    st.markdown("### 📊 Weather Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_temp = create_weather_plot(df, selected_city, 'temperature', weather_condition)
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        fig_humidity = create_weather_plot(df, selected_city, 'humidity', weather_condition)
        st.plotly_chart(fig_humidity, use_container_width=True)
    
    # Alerts
    st.markdown("### 🚨 Weather Alerts")
    
    if latest_data['temperature'] > 35:
        st.markdown("""
        <div class="alert-high">
            🔥 HIGH TEMPERATURE ALERT: Extreme heat detected!
        </div>
        """, unsafe_allow_html=True)
    
    if aqi_value > 150:
        st.markdown("""
        <div class="alert-high">
            🏭 AIR QUALITY ALERT: Unhealthy air quality levels!
        </div>
        """, unsafe_allow_html=True)
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Weather"):
        st.experimental_rerun()
    
    # Footer
    st.markdown(f"""
    <div style='text-align: center; margin-top: 3rem; padding: 1rem;'>
        <p>🌍 Weather-Responsive Climate AI System</p>
        <p>Current: {weather_condition.title()} | Updated: {datetime.now().strftime('%H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()