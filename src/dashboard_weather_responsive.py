"""
dashboard_weather_responsive.py
Advanced futuristic dashboard with weather-responsive animations and graphics.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
from alert_system import ClimateAlertSystem
import requests
import os
from datetime import datetime
import time


def get_weather_condition(city):
    """Get current weather condition for animations"""
    try:
        api_key = os.getenv('OPENWEATHER_API_KEY', 'demo_key')
        if api_key == 'demo_key':
            # Return simulated weather for demo
            conditions = ['clear', 'rain', 'snow', 'clouds', 'thunderstorm', 'fog']
            import random
            return random.choice(conditions)
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        data = response.json()
        
        weather_main = data['weather'][0]['main'].lower()
        weather_desc = data['weather'][0]['description'].lower()
        
        # Map weather conditions to animation types
        if 'rain' in weather_main or 'drizzle' in weather_main:
            return 'rain'
        elif 'snow' in weather_main:
            return 'snow'
        elif 'thunder' in weather_main or 'storm' in weather_main:
            return 'thunderstorm'
        elif 'fog' in weather_main or 'mist' in weather_main or 'haze' in weather_main:
            return 'fog'
        elif 'cloud' in weather_main:
            return 'clouds'
        else:
            return 'clear'
    except:
        return 'clear'


def get_temperature_level(temperature):
    """Get temperature level for color theming"""
    if temperature < 0:
        return 'freezing'
    elif temperature < 10:
        return 'cold'
    elif temperature < 25:
        return 'mild'
    elif temperature < 35:
        return 'warm'
    else:
        return 'hot'


def apply_weather_responsive_theme(weather_condition, temperature=20, time_of_day='day'):
    """Apply dynamic CSS styling based on weather conditions"""
    
    # Weather-specific color schemes
    weather_themes = {
        'clear': {
            'bg_gradient': '#0a0a0a 0%, #1a1a2e 50%, #16213e 100%',
            'primary_color': '#00ffff',
            'secondary_color': '#0080ff',
            'particle_color': '#ffff00',
            'animation': 'sunny'
        },
        'rain': {
            'bg_gradient': '#0a0a0a 0%, #1a2e3a 50%, #16213e 100%',
            'primary_color': '#0099ff',
            'secondary_color': '#0066cc',
            'particle_color': '#87ceeb',
            'animation': 'rain'
        },
        'snow': {
            'bg_gradient': '#0a0a0a 0%, #2e3a4a 50%, #4a5568 100%',
            'primary_color': '#ffffff',
            'secondary_color': '#e6f3ff',
            'particle_color': '#ffffff',
            'animation': 'snow'
        },
        'thunderstorm': {
            'bg_gradient': '#0a0a0a 0%, #2e1a2e 50%, #4a1a4a 100%',
            'primary_color': '#ff6600',
            'secondary_color': '#ffaa00',
            'particle_color': '#ffff00',
            'animation': 'lightning'
        },
        'fog': {
            'bg_gradient': '#0a0a0a 0%, #2e2e2e 50%, #4a4a4a 100%',
            'primary_color': '#cccccc',
            'secondary_color': '#999999',
            'particle_color': '#ffffff',
            'animation': 'fog'
        },
        'clouds': {
            'bg_gradient': '#0a0a0a 0%, #2a2a3a 50%, #3a3a4a 100%',
            'primary_color': '#66ccff',
            'secondary_color': '#4d9fcc',
            'particle_color': '#ffffff',
            'animation': 'clouds'
        }
    }
    
    theme = weather_themes.get(weather_condition, weather_themes['clear'])
    
    # Temperature-based intensity adjustments
    temp_intensity = {
        'freezing': 0.3,
        'cold': 0.5,
        'mild': 0.7,
        'warm': 0.9,
        'hot': 1.2
    }
    
    temp_level = get_temperature_level(temperature)
    intensity = temp_intensity.get(temp_level, 0.7)
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(135deg, {theme['bg_gradient']});
        color: {theme['primary_color']};
        position: relative;
        overflow: hidden;
    }}
    
    /* Weather Particles Container */
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
        background: linear-gradient(180deg, transparent, {theme['particle_color']});
        width: 2px;
        animation: rain-fall 1s linear infinite;
    }}
    
    @keyframes rain-fall {{
        0% {{ 
            transform: translateY(-100vh);
            opacity: 0;
        }}
        10% {{ opacity: 1; }}
        90% {{ opacity: 1; }}
        100% {{ 
            transform: translateY(100vh);
            opacity: 0;
        }}
    }}
    
    /* Snow Animation */
    .snow-flake {{
        position: absolute;
        background: {theme['particle_color']};
        border-radius: 50%;
        animation: snow-fall 3s linear infinite;
    }}
    
    @keyframes snow-fall {{
        0% {{ 
            transform: translateY(-100vh) rotate(0deg);
            opacity: 0;
        }}
        10% {{ opacity: 1; }}
        90% {{ opacity: 1; }}
        100% {{ 
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
        }}
    }}
    
    /* Lightning Animation */
    .lightning {{
        position: absolute;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent 48%, {theme['particle_color']} 49%, {theme['particle_color']} 51%, transparent 52%);
        opacity: 0;
        animation: lightning-flash 3s infinite;
    }}
    
    @keyframes lightning-flash {{
        0%, 90%, 96%, 100% {{ opacity: 0; }}
        93% {{ opacity: 0.8; }}
    }}
    
    /* Fog Animation */
    .fog-layer {{
        position: absolute;
        width: 120%;
        height: 100%;
        background: radial-gradient(ellipse, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: fog-drift 8s linear infinite;
    }}
    
    @keyframes fog-drift {{
        0% {{ transform: translateX(-20%); }}
        100% {{ transform: translateX(20%); }}
    }}
    
    /* Cloud Animation */
    .cloud {{
        position: absolute;
        background: radial-gradient(ellipse, rgba(255,255,255,0.2) 0%, transparent 70%);
        border-radius: 50px;
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
        background: linear-gradient(90deg, {theme['primary_color']}, {theme['secondary_color']}, #8000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 3rem;
        text-align: center;
        animation: weather-glow 2s ease-in-out infinite alternate;
        filter: brightness({intensity});
    }}
    
    .metric-card {{
        background: linear-gradient(135deg, rgba({",".join([str(int(theme['primary_color'][1:3], 16)), str(int(theme['primary_color'][3:5], 16)), str(int(theme['primary_color'][5:7], 16))])}, 0.1), rgba(128, 0, 255, 0.1));
        border: 1px solid {theme['primary_color']};
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 30px rgba({",".join([str(int(theme['primary_color'][1:3], 16)), str(int(theme['primary_color'][3:5], 16)), str(int(theme['primary_color'][5:7], 16))])}, 0.3);
        backdrop-filter: blur(10px);
        animation: card-pulse {2/intensity}s ease-in-out infinite alternate;
    }}
    
    .weather-indicator {{
        position: absolute;
        top: 20px;
        right: 20px;
        background: rgba({",".join([str(int(theme['primary_color'][1:3], 16)), str(int(theme['primary_color'][3:5], 16)), str(int(theme['primary_color'][5:7], 16))])}, 0.2);
        border: 2px solid {theme['primary_color']};
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        animation: weather-spin 6s linear infinite;
    }}
    
    .temperature-bar {{
        height: 10px;
        background: linear-gradient(90deg, 
            #0066ff 0%, 
            #00ccff 20%, 
            #00ff66 40%, 
            #ffff00 60%, 
            #ff6600 80%, 
            #ff0000 100%);
        border-radius: 5px;
        margin: 10px 0;
        position: relative;
        overflow: hidden;
    }}
    
    .temperature-indicator {{
        position: absolute;
        top: -5px;
        width: 20px;
        height: 20px;
        background: {theme['primary_color']};
        border-radius: 50%;
        border: 2px solid white;
        transform: translateX(-50%);
        animation: temp-pulse 1s ease-in-out infinite alternate;
    }}
    
    @keyframes weather-glow {{
        from {{ text-shadow: 0 0 20px rgba({",".join([str(int(theme['primary_color'][1:3], 16)), str(int(theme['primary_color'][3:5], 16)), str(int(theme['primary_color'][5:7], 16))])}, 0.5); }}
        to {{ text-shadow: 0 0 30px rgba({",".join([str(int(theme['primary_color'][1:3], 16)), str(int(theme['primary_color'][3:5], 16)), str(int(theme['primary_color'][5:7], 16))])}, 0.8); }}
    }}
    
    @keyframes card-pulse {{
        from {{ box-shadow: 0 0 20px rgba({",".join([str(int(theme['primary_color'][1:3], 16)), str(int(theme['primary_color'][3:5], 16)), str(int(theme['primary_color'][5:7], 16))])}, 0.3); }}
        to {{ box-shadow: 0 0 40px rgba({",".join([str(int(theme['primary_color'][1:3], 16)), str(int(theme['primary_color'][3:5], 16)), str(int(theme['primary_color'][5:7], 16))])}, 0.6); }}
    }}
    
    @keyframes weather-spin {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    
    @keyframes temp-pulse {{
        from {{ transform: translateX(-50%) scale(1); }}
        to {{ transform: translateX(-50%) scale(1.3); }}
    }}
    
    .alert-high {{
        background: linear-gradient(135deg, rgba(255, 0, 100, 0.3), rgba(255, 50, 50, 0.3));
        border: 2px solid #ff0066;
        border-radius: 10px;
        padding: 15px;
        animation: critical-pulse {1/intensity}s infinite;
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
        """ + "".join([f'<div class="rain-drop" style="left: {i*5}%; height: 100px; animation-delay: {i*0.1}s;"></div>' for i in range(20)]) + """
        </div>
        """
    elif weather_condition == 'snow':
        particles_html = """
        <div class="weather-particles">
        """ + "".join([f'<div class="snow-flake" style="left: {i*7}%; width: 6px; height: 6px; animation-delay: {i*0.2}s; animation-duration: {3+i*0.3}s;"></div>' for i in range(15)]) + """
        </div>
        """
    elif weather_condition == 'thunderstorm':
        particles_html = """
        <div class="weather-particles">
            <div class="lightning"></div>
        </div>
        """
    elif weather_condition == 'fog':
        particles_html = """
        <div class="weather-particles">
        """ + "".join([f'<div class="fog-layer" style="top: {i*20}%; animation-delay: {i*2}s;"></div>' for i in range(3)]) + """
        </div>
        """
    elif weather_condition == 'clouds':
        particles_html = """
        <div class="weather-particles">
        """ + "".join([f'<div class="cloud" style="top: {20+i*15}%; width: 150px; height: 75px; animation-delay: {i*3}s;"></div>' for i in range(4)]) + """
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
        'fog': '🌫️',
        'clouds': '☁️'
    }
    
    st.markdown(f"""
    {particles_html}
    <div class="weather-indicator">
        {weather_emojis.get(weather_condition, '🌤️')}
    </div>
    """, unsafe_allow_html=True)


def create_weather_responsive_metric_card(title, value, unit="", temperature=None):
    """Create a weather-responsive metric display card"""
    temp_bar = ""
    if temperature is not None:
        # Calculate temperature position (0-100%)
        temp_pos = max(0, min(100, (temperature + 10) * 2))  # -10°C to 40°C range
        temp_bar = f"""
        <div class="temperature-bar">
            <div class="temperature-indicator" style="left: {temp_pos}%;"></div>
        </div>
        """
    
    st.markdown(f"""
    <div class="metric-card">
        <h4 style='margin: 0;'>{title}</h4>
        <h2 style='color: #ffffff; margin: 5px 0;'>{value}{unit}</h2>
        {temp_bar}
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


def create_weather_responsive_plot(df, city, metric, forecast_df=None, weather_condition='clear'):
    """Create weather-responsive forecast plot with dynamic styling"""
    city_data = df[df['city'] == city].copy()
    
    # Weather-specific color schemes for plots
    weather_colors = {
        'clear': {'historical': '#ffaa00', 'forecast': '#ff6600'},
        'rain': {'historical': '#0099ff', 'forecast': '#0066cc'},
        'snow': {'historical': '#ffffff', 'forecast': '#ccccff'},
        'thunderstorm': {'historical': '#ff6600', 'forecast': '#ffaa00'},
        'fog': {'historical': '#cccccc', 'forecast': '#999999'},
        'clouds': {'historical': '#66ccff', 'forecast': '#4d9fcc'}
    }
    
    colors = weather_colors.get(weather_condition, weather_colors['clear'])
    
    fig = go.Figure()
    
    # Historical data with weather-specific styling
    fig.add_trace(go.Scatter(
        x=city_data['timestamp'],
        y=city_data[metric],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color=colors['historical'], width=3),
        marker=dict(color=colors['historical'], size=6)
    ))
    
    # Forecast data
    if forecast_df is not None:
        forecast_df = forecast_df.copy()  # Fix pandas warning
        forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
        
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'],
            y=forecast_df['yhat'],
            mode='lines+markers',
            name='AI Forecast',
            line=dict(color=colors['forecast'], width=4, dash='dot'),
            marker=dict(color=colors['forecast'], size=8)
        ))
    
    # Weather-specific background
    bg_colors = {
        'clear': 'rgba(255, 170, 0, 0.05)',
        'rain': 'rgba(0, 153, 255, 0.05)',
        'snow': 'rgba(255, 255, 255, 0.05)',
        'thunderstorm': 'rgba(255, 102, 0, 0.05)',
        'fog': 'rgba(204, 204, 204, 0.05)',
        'clouds': 'rgba(102, 204, 255, 0.05)'
    }
    
    fig.update_layout(
        title=f'{metric.title()} Forecast - {city}',
        xaxis_title='Time',
        yaxis_title=f'{metric.title()}',
        plot_bgcolor=bg_colors.get(weather_condition, 'rgba(0, 0, 0, 0)'),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color=colors['historical']),
        title_font=dict(size=20, color=colors['historical'])
    )
    
    return fig


def main():
    """Main dashboard function with weather-responsive features"""
    st.set_page_config(
        page_title="Climate AI Neural Prediction System",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar for city selection
    cities = df['city'].unique()
    selected_city = st.sidebar.selectbox("🏙️ Select City", cities)
    
    # Get weather condition for animations
    weather_condition = get_weather_condition(selected_city)
    
    # Get current temperature for responsive theming
    city_data = df[df['city'] == selected_city]
    if not city_data.empty:
        current_temp = city_data['temperature'].iloc[-1]
    else:
        current_temp = 20
    
    # Apply weather-responsive theme
    apply_weather_responsive_theme(weather_condition, current_temp)
    
    # Main header with weather info
    st.markdown(f"""
    <h1 class="main-header">🌐 Climate AI Neural Prediction System</h1>
    <p style='text-align: center; font-size: 1.2rem; margin-bottom: 2rem;'>
    Real-time Weather: {weather_condition.title()} | City: {selected_city}
    </p>
    """, unsafe_allow_html=True)
    
    if city_data.empty:
        st.error(f"No data available for {selected_city}")
        return
    
    # Latest data
    latest_data = city_data.iloc[-1]
    
    # Display metrics with weather-responsive styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_weather_responsive_metric_card(
            "🌡️ Temperature", 
            f"{latest_data['temperature']:.1f}", 
            "°C",
            latest_data['temperature']
        )
    
    with col2:
        create_weather_responsive_metric_card(
            "💧 Humidity", 
            f"{latest_data['humidity']:.1f}", 
            "%"
        )
    
    with col3:
        create_weather_responsive_metric_card(
            "🌧️ Rainfall", 
            f"{latest_data['rainfall']:.1f}", 
            "mm"
        )
    
    with col4:
        aqi_value = latest_data.get('aqi', 0)
        create_weather_responsive_metric_card(
            "🏭 Air Quality", 
            f"{aqi_value:.0f}", 
            " AQI"
        )
    
    # Forecast section
    st.markdown("### 🔮 AI Weather Forecast")
    
    forecast_cols = st.columns(2)
    
    with forecast_cols[0]:
        # Temperature forecast
        model_path = f"data/prophet_{selected_city}_temperature.joblib"
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            future = model.make_future_dataframe(periods=24, freq='h')  # Use 'h' instead of 'H'
            forecast = model.predict(future)
            fig = create_weather_responsive_plot(
                df, selected_city, 'temperature', 
                forecast.tail(24), weather_condition
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with forecast_cols[1]:
        # Humidity forecast (using same model structure)
        fig = create_weather_responsive_plot(
            df, selected_city, 'humidity', 
            None, weather_condition
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Alert system
    st.markdown("### 🚨 Smart Climate Alerts")
    
    alert_system = ClimateAlertSystem()
    
    # Check for alerts based on current conditions
    if latest_data['temperature'] > 35:
        st.markdown("""
        <div class="alert-high">
            🔥 HIGH TEMPERATURE ALERT: Extreme heat detected! Take precautions.
        </div>
        """, unsafe_allow_html=True)
    
    if aqi_value > 150:
        st.markdown("""
        <div class="alert-high">
            🏭 AIR QUALITY ALERT: Unhealthy air quality levels detected!
        </div>
        """, unsafe_allow_html=True)
    
    # Real-time updates
    if st.sidebar.button("🔄 Refresh Weather Animation"):
        st.experimental_rerun()
    
    # Auto-refresh every 30 seconds
    time.sleep(0.1)  # Small delay for smooth animation
    
    # Footer
    st.markdown(f"""
    <div style='text-align: center; margin-top: 3rem; padding: 1rem; border-top: 1px solid rgba(255,255,255,0.2);'>
        <p>🌍 Climate AI Neural Prediction System | Weather-Responsive Interface</p>
        <p>Current Weather: {weather_condition.title()} | Last Updated: {datetime.now().strftime('%H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()