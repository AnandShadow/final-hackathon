"""
dashboard_enhanced.py
Enhanced dashboard with weather animations and all content visible together.
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
        
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key}
        response = requests.get(url, params=params)
        data = response.json()
        
        weather_main = data['weather'][0]['main'].lower()
        
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


def apply_enhanced_theme_with_animations(weather_condition, temperature=20):
    """Apply enhanced theme with visible content and animations"""
    
    # Weather-specific themes
    weather_themes = {
        'clear': {
            'bg_gradient': '#0a0a0a 0%, #1a1a2e 50%, #16213e 100%',
            'primary_color': '#00ffff',
            'secondary_color': '#ffaa00',
            'particle_color': '#ffff00',
            'content_bg': 'rgba(26, 26, 46, 0.85)'
        },
        'rain': {
            'bg_gradient': '#0a0a0a 0%, #1a2e3a 50%, #16213e 100%',
            'primary_color': '#0099ff',
            'secondary_color': '#66ccff',
            'particle_color': '#87ceeb',
            'content_bg': 'rgba(26, 46, 58, 0.85)'
        },
        'snow': {
            'bg_gradient': '#0a0a0a 0%, #2e3a4a 50%, #4a5568 100%',
            'primary_color': '#ffffff',
            'secondary_color': '#ccccff',
            'particle_color': '#ffffff',
            'content_bg': 'rgba(46, 58, 74, 0.85)'
        },
        'thunderstorm': {
            'bg_gradient': '#0a0a0a 0%, #2e1a2e 50%, #4a1a4a 100%',
            'primary_color': '#ff6600',
            'secondary_color': '#ffaa00',
            'particle_color': '#ffff00',
            'content_bg': 'rgba(46, 26, 46, 0.85)'
        },
        'clouds': {
            'bg_gradient': '#0a0a0a 0%, #2a2a3a 50%, #3a3a4a 100%',
            'primary_color': '#66ccff',
            'secondary_color': '#99ccff',
            'particle_color': '#ffffff',
            'content_bg': 'rgba(42, 42, 58, 0.85)'
        }
    }
    
    theme = weather_themes.get(weather_condition, weather_themes['clear'])
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(135deg, {theme['bg_gradient']});
        color: {theme['primary_color']};
        position: relative;
        min-height: 100vh;
    }}
    
    /* Content Container - Ensure content is above animations */
    .main .block-container {{
        background: {theme['content_bg']};
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem;
        border: 1px solid {theme['primary_color']}40;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.2);
        position: relative;
        z-index: 100;
    }}
    
    /* Weather Particles - Behind content */
    .weather-particles {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }}
    
    /* Enhanced Rain Animation */
    .rain-drop {{
        position: absolute;
        background: linear-gradient(180deg, transparent, {theme['particle_color']});
        width: 2px;
        height: 60px;
        animation: rain-fall 1.2s linear infinite;
        opacity: 0.7;
    }}
    
    @keyframes rain-fall {{
        0% {{ transform: translateY(-100vh); opacity: 0; }}
        10% {{ opacity: 0.7; }}
        90% {{ opacity: 0.7; }}
        100% {{ transform: translateY(100vh); opacity: 0; }}
    }}
    
    /* Enhanced Snow Animation */
    .snow-flake {{
        position: absolute;
        background: {theme['particle_color']};
        border-radius: 50%;
        width: 6px;
        height: 6px;
        animation: snow-fall 4s linear infinite;
        opacity: 0.8;
        box-shadow: 0 0 10px {theme['particle_color']};
    }}
    
    @keyframes snow-fall {{
        0% {{ transform: translateY(-100vh) rotate(0deg); opacity: 0; }}
        10% {{ opacity: 0.8; }}
        90% {{ opacity: 0.8; }}
        100% {{ transform: translateY(100vh) rotate(360deg); opacity: 0; }}
    }}
    
    /* Enhanced Lightning Animation */
    .lightning {{
        position: absolute;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, 
            transparent 47%, 
            {theme['particle_color']} 48%, 
            {theme['particle_color']} 52%, 
            transparent 53%);
        opacity: 0;
        animation: lightning-flash 4s infinite;
    }}
    
    @keyframes lightning-flash {{
        0%, 90%, 96%, 100% {{ opacity: 0; }}
        92% {{ opacity: 0.3; }}
        94% {{ opacity: 0.8; }}
    }}
    
    /* Enhanced Cloud Animation */
    .cloud {{
        position: absolute;
        background: radial-gradient(ellipse, 
            rgba(255,255,255,0.15) 0%, 
            rgba(255,255,255,0.05) 50%, 
            transparent 70%);
        border-radius: 100px;
        animation: cloud-float 20s linear infinite;
        opacity: 0.6;
    }}
    
    @keyframes cloud-float {{
        0% {{ transform: translateX(-150px); }}
        100% {{ transform: translateX(calc(100vw + 150px)); }}
    }}
    
    /* Enhanced Sunny Animation */
    .sun-rays {{
        position: absolute;
        top: 10%;
        right: 10%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, 
            rgba(255,255,0,0.1) 0%, 
            rgba(255,170,0,0.05) 50%, 
            transparent 70%);
        border-radius: 50%;
        animation: sun-pulse 6s ease-in-out infinite;
    }}
    
    @keyframes sun-pulse {{
        0%, 100% {{ 
            transform: scale(1) rotate(0deg); 
            opacity: 0.3; 
        }}
        50% {{ 
            transform: scale(1.3) rotate(180deg); 
            opacity: 0.1; 
        }}
    }}
    
    /* Header Styling */
    .main-header {{
        background: linear-gradient(90deg, 
            {theme['primary_color']}, 
            {theme['secondary_color']}, 
            #8000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 3rem;
        text-align: center;
        animation: weather-glow 3s ease-in-out infinite alternate;
        margin-bottom: 2rem;
        text-shadow: 0 0 20px {theme['primary_color']}50;
    }}
    
    /* Enhanced Metric Cards */
    .metric-card {{
        background: linear-gradient(135deg, 
            rgba(0, 255, 255, 0.1), 
            rgba(128, 0, 255, 0.1));
        border: 2px solid {theme['primary_color']};
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 
            0 0 20px rgba(0, 255, 255, 0.3),
            inset 0 0 20px rgba(0, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 
            0 5px 30px rgba(0, 255, 255, 0.5),
            inset 0 0 30px rgba(0, 255, 255, 0.2);
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255,255,255,0.1), 
            transparent);
        animation: shimmer 3s infinite;
    }}
    
    @keyframes shimmer {{
        0% {{ left: -100%; }}
        100% {{ left: 100%; }}
    }}
    
    /* Weather Indicator */
    .weather-indicator {{
        position: fixed;
        top: 20px;
        right: 20px;
        background: {theme['content_bg']};
        border: 3px solid {theme['primary_color']};
        border-radius: 50%;
        width: 90px;
        height: 90px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        animation: weather-bounce 3s ease-in-out infinite;
        z-index: 200;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }}
    
    @keyframes weather-bounce {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
        50% {{ transform: translateY(-10px) rotate(5deg); }}
    }}
    
    /* Enhanced Alerts */
    .alert-high {{
        background: linear-gradient(135deg, 
            rgba(255, 0, 100, 0.3), 
            rgba(255, 50, 50, 0.3));
        border: 3px solid #ff0066;
        border-radius: 15px;
        padding: 1.5rem;
        animation: critical-pulse 2s infinite;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }}
    
    @keyframes critical-pulse {{
        0% {{ 
            box-shadow: 0 0 20px rgba(255, 0, 102, 0.5);
            border-color: #ff0066;
        }}
        50% {{ 
            box-shadow: 0 0 40px rgba(255, 0, 102, 0.8);
            border-color: #ff3399;
        }}
        100% {{ 
            box-shadow: 0 0 20px rgba(255, 0, 102, 0.5);
            border-color: #ff0066;
        }}
    }}
    
    /* Chart Container */
    .stPlotlyChart {{
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid {theme['primary_color']}30;
    }}
    
    /* Sidebar Styling */
    .css-1d391kg {{
        background: {theme['content_bg']};
        border-right: 2px solid {theme['primary_color']};
    }}
    
    /* Global Animations */
    @keyframes weather-glow {{
        from {{ 
            text-shadow: 0 0 20px {theme['primary_color']}50; 
        }}
        to {{ 
            text-shadow: 0 0 30px {theme['primary_color']}80,
                         0 0 40px {theme['secondary_color']}40; 
        }}
    }}
    
    /* Ensure content visibility */
    .element-container, .stMarkdown, .stMetric {{
        position: relative;
        z-index: 50;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Add weather particles based on condition
    particles_html = ""
    if weather_condition == 'rain':
        particles_html = """
        <div class="weather-particles">
        """ + "".join([f'<div class="rain-drop" style="left: {i*4}%; animation-delay: {i*0.08}s;"></div>' for i in range(25)]) + """
        </div>
        """
    elif weather_condition == 'snow':
        particles_html = """
        <div class="weather-particles">
        """ + "".join([f'<div class="snow-flake" style="left: {i*6}%; animation-delay: {i*0.15}s; animation-duration: {3+i*0.2}s;"></div>' for i in range(20)]) + """
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
        """ + "".join([f'<div class="cloud" style="top: {15+i*20}%; width: {120+i*30}px; height: {60+i*15}px; animation-delay: {i*4}s;"></div>' for i in range(5)]) + """
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


def create_enhanced_metric_card(title, value, unit=""):
    """Create enhanced metric display card"""
    st.markdown(f"""
    <div class="metric-card">
        <h4 style='margin: 0; color: #00ffff; font-weight: 700;'>{title}</h4>
        <h2 style='color: #ffffff; margin: 10px 0; font-size: 2.5rem; font-weight: 900;'>{value}{unit}</h2>
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


def create_enhanced_plot(df, city, metric, weather_condition='clear'):
    """Create enhanced weather-responsive plot"""
    city_data = df[df['city'] == city].copy()
    
    # Weather-specific colors
    weather_colors = {
        'clear': {'line': '#ffaa00', 'fill': 'rgba(255, 170, 0, 0.1)'},
        'rain': {'line': '#0099ff', 'fill': 'rgba(0, 153, 255, 0.1)'},
        'snow': {'line': '#ffffff', 'fill': 'rgba(255, 255, 255, 0.1)'},
        'thunderstorm': {'line': '#ff6600', 'fill': 'rgba(255, 102, 0, 0.1)'},
        'clouds': {'line': '#66ccff', 'fill': 'rgba(102, 204, 255, 0.1)'}
    }
    
    colors = weather_colors.get(weather_condition, weather_colors['clear'])
    
    fig = go.Figure()
    
    # Add area fill
    fig.add_trace(go.Scatter(
        x=city_data['timestamp'],
        y=city_data[metric],
        mode='lines',
        name='Trend',
        line=dict(color=colors['line'], width=0),
        fill='tonexty',
        fillcolor=colors['fill']
    ))
    
    # Add main line
    fig.add_trace(go.Scatter(
        x=city_data['timestamp'],
        y=city_data[metric],
        mode='lines+markers',
        name=f'{metric.title()}',
        line=dict(color=colors['line'], width=4),
        marker=dict(
            color=colors['line'], 
            size=8,
            line=dict(width=2, color='white')
        )
    ))
    
    fig.update_layout(
        title=f'📊 {metric.title()} Analysis - {city}',
        xaxis_title='Timeline',
        yaxis_title=f'{metric.title()} Value',
        plot_bgcolor='rgba(0, 0, 0, 0.2)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color=colors['line'], size=12),
        title_font=dict(size=18, color=colors['line']),
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    # Add grid
    fig.update_xaxes(
        gridcolor='rgba(255, 255, 255, 0.1)',
        gridwidth=1
    )
    fig.update_yaxes(
        gridcolor='rgba(255, 255, 255, 0.1)',
        gridwidth=1
    )
    
    return fig


def main():
    """Enhanced main dashboard function"""
    st.set_page_config(
        page_title="Climate AI Enhanced System",
        page_icon="🌦️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar
    st.sidebar.title("🎛️ Control Panel")
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
    
    # Apply enhanced theme with animations
    apply_enhanced_theme_with_animations(weather_condition, current_temp)
    
    # Main Header
    st.markdown(f"""
    <h1 class="main-header">
        🌦️ Climate AI Enhanced System
    </h1>
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h3 style='color: #00ffff; margin: 0;'>
            🌍 Live Weather: {weather_condition.title()} | 🏙️ {selected_city}
        </h3>
        <p style='color: #ffffff; opacity: 0.8; margin: 0.5rem 0;'>
            Real-time climate monitoring with dynamic weather animations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if city_data.empty:
        st.error(f"❌ No data available for {selected_city}")
        return
    
    # Latest data
    latest_data = city_data.iloc[-1]
    
    # Enhanced Metrics Section
    st.markdown("### 📊 Real-time Climate Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_enhanced_metric_card(
            "🌡️ Temperature", 
            f"{latest_data['temperature']:.1f}", 
            "°C"
        )
    
    with col2:
        create_enhanced_metric_card(
            "💧 Humidity", 
            f"{latest_data['humidity']:.1f}", 
            "%"
        )
    
    with col3:
        create_enhanced_metric_card(
            "🌧️ Rainfall", 
            f"{latest_data['rainfall']:.1f}", 
            "mm"
        )
    
    with col4:
        aqi_value = latest_data.get('aqi', 0)
        create_enhanced_metric_card(
            "🏭 Air Quality", 
            f"{aqi_value:.0f}", 
            " AQI"
        )
    
    # Charts Section
    st.markdown("### 📈 Weather Analytics Dashboard")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        fig_temp = create_enhanced_plot(df, selected_city, 'temperature', weather_condition)
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with chart_col2:
        fig_humidity = create_enhanced_plot(df, selected_city, 'humidity', weather_condition)
        st.plotly_chart(fig_humidity, use_container_width=True)
    
    # Additional Charts
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        fig_rainfall = create_enhanced_plot(df, selected_city, 'rainfall', weather_condition)
        st.plotly_chart(fig_rainfall, use_container_width=True)
    
    with chart_col4:
        # Summary statistics
        st.markdown("#### 📊 Climate Summary")
        summary_data = {
            'Metric': ['Temperature', 'Humidity', 'Rainfall', 'AQI'],
            'Current': [
                f"{latest_data['temperature']:.1f}°C",
                f"{latest_data['humidity']:.1f}%", 
                f"{latest_data['rainfall']:.1f}mm",
                f"{aqi_value:.0f}"
            ],
            'Average': [
                f"{city_data['temperature'].mean():.1f}°C",
                f"{city_data['humidity'].mean():.1f}%",
                f"{city_data['rainfall'].mean():.1f}mm",
                f"{city_data.get('aqi', pd.Series([0])).mean():.0f}"
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True)
    
    # Enhanced Alerts Section
    st.markdown("### 🚨 Smart Climate Alerts")
    
    alert_col1, alert_col2 = st.columns(2)
    
    with alert_col1:
        if latest_data['temperature'] > 35:
            st.markdown("""
            <div class="alert-high">
                🔥 <strong>EXTREME HEAT ALERT</strong><br>
                Temperature: {:.1f}°C - Take immediate precautions!
            </div>
            """.format(latest_data['temperature']), unsafe_allow_html=True)
        
        if latest_data['temperature'] < 0:
            st.markdown("""
            <div class="alert-high">
                🧊 <strong>FREEZING ALERT</strong><br>
                Temperature: {:.1f}°C - Risk of frost and ice!
            </div>
            """.format(latest_data['temperature']), unsafe_allow_html=True)
    
    with alert_col2:
        if aqi_value > 150:
            st.markdown("""
            <div class="alert-high">
                🏭 <strong>AIR QUALITY ALERT</strong><br>
                AQI: {} - Unhealthy air quality detected!
            </div>
            """.format(int(aqi_value)), unsafe_allow_html=True)
        
        if latest_data['rainfall'] > 25:
            st.markdown("""
            <div class="alert-high">
                🌧️ <strong>HEAVY RAIN ALERT</strong><br>
                Rainfall: {:.1f}mm - Flooding risk!
            </div>
            """.format(latest_data['rainfall']), unsafe_allow_html=True)
    
    # Control Panel
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎮 Animation Controls")
    
    if st.sidebar.button("🔄 Refresh Weather Animation"):
        st.experimental_rerun()
    
    st.sidebar.markdown(f"""
    **Current Weather:** {weather_condition.title()}  
    **Animation:** Active  
    **Temperature:** {current_temp:.1f}°C  
    **Last Update:** {datetime.now().strftime('%H:%M:%S')}
    """)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem; background: rgba(0,0,0,0.3); border-radius: 10px; margin-top: 2rem;'>
        <h4 style='color: #00ffff; margin: 0;'>
            🌍 Climate AI Enhanced System with Live Weather Animations
        </h4>
        <p style='color: #ffffff; opacity: 0.8; margin: 0.5rem 0;'>
            Current Weather: <strong>{weather_condition.title()}</strong> | 
            City: <strong>{selected_city}</strong> | 
            Last Updated: <strong>{datetime.now().strftime('%H:%M:%S')}</strong>
        </p>
        <p style='color: #66ccff; font-size: 0.9rem; margin: 0;'>
            🎨 Dynamic animations respond to real weather conditions
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()