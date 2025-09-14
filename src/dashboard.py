"""
dashboard.py
Futuristic Interactive Streamlit dashboard for climate risk prediction visualization.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
from datetime import datetime, timedelta
import os
import time
import numpy as np
from alert_system import ClimateAlertSystem


def apply_futuristic_theme():
    """Apply futuristic CSS styling"""
    st.markdown("""
    <style>
    /* Import futuristic font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #00ffff;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #00ffff, #0080ff, #8000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 3rem;
        text-align: center;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f3460 0%, #1a1a2e 100%);
        border-right: 2px solid #00ffff;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(128, 0, 255, 0.1));
        border: 1px solid #00ffff;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Alert styling */
    .alert-high {
        background: linear-gradient(135deg, rgba(255, 0, 100, 0.2), rgba(255, 50, 50, 0.2));
        border: 2px solid #ff0066;
        border-radius: 10px;
        padding: 15px;
        animation: pulse 1.5s infinite;
    }
    
    .alert-medium {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.2), rgba(255, 215, 0, 0.2));
        border: 2px solid #ffa500;
        border-radius: 10px;
        padding: 15px;
    }
    
    .alert-normal {
        background: linear-gradient(135deg, rgba(0, 255, 100, 0.2), rgba(50, 255, 50, 0.2));
        border: 2px solid #00ff66;
        border-radius: 10px;
        padding: 15px;
    }
    
    /* Animations */
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(0, 255, 255, 0.5); }
        to { text-shadow: 0 0 30px rgba(0, 255, 255, 0.8), 0 0 40px rgba(0, 255, 255, 0.6); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 20px rgba(255, 0, 102, 0.5); }
        50% { box-shadow: 0 0 40px rgba(255, 0, 102, 0.8); }
        100% { box-shadow: 0 0 20px rgba(255, 0, 102, 0.5); }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #00ffff, #0080ff);
        color: #000;
        border: none;
        border-radius: 25px;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.6);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(26, 26, 46, 0.8);
        border: 1px solid #00ffff;
        border-radius: 10px;
    }
    
    /* Text styling */
    .stMarkdown {
        font-family: 'Orbitron', monospace;
    }
    
    /* Hide default streamlit styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """, unsafe_allow_html=True)


def create_futuristic_metric_card(title, value, unit="", trend=None):
    """Create a futuristic metric display card"""
    trend_icon = ""
    if trend == "up":
        trend_icon = "📈"
    elif trend == "down":
        trend_icon = "📉"
    elif trend == "stable":
        trend_icon = "➡️"
    
    st.markdown(f"""
    <div class="metric-card">
        <h4 style='color: #00ffff; margin: 0; font-family: Orbitron;'>{title} {trend_icon}</h4>
        <h2 style='color: #ffffff; margin: 5px 0; font-family: Orbitron; font-weight: 900;'>{value}{unit}</h2>
    </div>
    """, unsafe_allow_html=True)


def create_futuristic_alert(message, alert_type="normal"):
    """Create futuristic alert display"""
    st.markdown(f"""
    <div class="alert-{alert_type}">
        <p style='margin: 0; font-family: Orbitron; font-weight: 700;'>{message}</p>
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


def load_model(city, metric):
    """Load trained Prophet model"""
    model_path = f"data/prophet_{city}_{metric}.joblib"
    try:
        return joblib.load(model_path)
    except FileNotFoundError:
        st.warning(f"Model not found for {city} {metric}. Please train the model first.")
        return None


def create_futuristic_forecast_plot(df, city, metric, forecast_df=None):
    """Create futuristic interactive forecast plot with cyberpunk styling"""
    city_data = df[df['city'] == city].copy()
    
    fig = go.Figure()
    
    # Historical data with cyberpunk styling
    fig.add_trace(go.Scatter(
        x=city_data['timestamp'],
        y=city_data[metric],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='#00ffff', width=3, shape='spline'),
        marker=dict(color='#00ffff', size=6, symbol='diamond'),
        hovertemplate='<b>%{y:.2f}</b><br>%{x}<extra></extra>'
    ))
    
    # Forecast data with futuristic styling
    if forecast_df is not None:
        forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
        
        # Forecast line
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'],
            y=forecast_df['yhat'],
            mode='lines+markers',
            name='AI Forecast',
            line=dict(color='#ff0080', width=4, dash='dot'),
            marker=dict(color='#ff0080', size=8, symbol='star'),
            hovertemplate='<b>Forecast: %{y:.2f}</b><br>%{x}<extra></extra>'
        ))
        
        # Confidence interval with gradient fill
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'],
            y=forecast_df['yhat_upper'],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'],
            y=forecast_df['yhat_lower'],
            mode='lines',
            fill='tonexty',
            line=dict(width=0),
            name='Confidence Zone',
            fillcolor='rgba(255, 0, 128, 0.2)',
            hoverinfo='skip'
        ))
    
    # Futuristic plot styling
    fig.update_layout(
        title=dict(
            text=f'🌐 {metric.upper()} NEURAL FORECAST - {city.upper()}',
            font=dict(family='Orbitron', size=24, color='#00ffff'),
            x=0.5
        ),
        xaxis=dict(
            title='TEMPORAL AXIS',
            gridcolor='rgba(0, 255, 255, 0.2)',
            color='#00ffff',
            showgrid=True,
            titlefont=dict(family='Orbitron'),
            tickfont=dict(family='Orbitron')
        ),
        yaxis=dict(
            title=f'{metric.upper()} READINGS',
            gridcolor='rgba(0, 255, 255, 0.2)',
            color='#00ffff',
            showgrid=True,
            titlefont=dict(family='Orbitron'),
            tickfont=dict(family='Orbitron')
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        legend=dict(
            bgcolor='rgba(26, 26, 46, 0.8)',
            bordercolor='#00ffff',
            borderwidth=1,
            font=dict(family='Orbitron', color='#00ffff')
        )
    )
    
    return fig
    """Load climate data"""
    try:
        df = pd.read_csv("data/combined_climate.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except FileNotFoundError:
        st.error("Climate data not found. Please run data collection first.")
        return None


def load_model(city, metric):
    """Load trained Prophet model"""
    model_path = f"data/prophet_{city}_{metric}.joblib"
    try:
        return joblib.load(model_path)
    except FileNotFoundError:
        st.warning(f"Model not found for {city} {metric}. Please train the model first.")
        return None


def create_forecast_plot(df, city, metric, forecast_df=None):
    """Create interactive forecast plot"""
    city_data = df[df['city'] == city].copy()
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=city_data['timestamp'],
        y=city_data[metric],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='blue')
    ))
    
    # Forecast data
    if forecast_df is not None:
        forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
        
        # Forecast line
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'],
            y=forecast_df['yhat'],
            mode='lines',
            name='Forecast',
            line=dict(color='red', dash='dash')
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'],
            y=forecast_df['yhat_upper'],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'],
            y=forecast_df['yhat_lower'],
            mode='lines',
            fill='tonexty',
            line=dict(width=0),
            name='Confidence Interval',
            fillcolor='rgba(255,0,0,0.2)'
        ))
    
    fig.update_layout(
        title=f'{metric.title()} Forecast for {city}',
        xaxis_title='Date',
        yaxis_title=metric.title(),
        hovermode='x unified'
    )
    
    return fig


def main():
    """Main futuristic dashboard function"""
    st.set_page_config(
        page_title="🌐 CLIMATE.AI - Neural Prediction System",
        page_icon="🌡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply futuristic theme
    apply_futuristic_theme()
    
    # Main header with animation
    st.markdown('<h1 class="main-header">🌐 CLIMATE.AI NEURAL PREDICTION SYSTEM</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar with futuristic styling
    st.sidebar.markdown("## 🎛️ CONTROL PANEL")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Enhanced sidebar controls
    st.sidebar.markdown("### 🌍 TARGET SELECTION")
    cities = df['city'].unique()
    selected_city = st.sidebar.selectbox("🏙️ Neural Node", cities, 
                                        help="Select monitoring station")
    
    metrics = ['temperature', 'humidity', 'rainfall', 'aqi']
    metric_icons = {'temperature': '🌡️', 'humidity': '💧', 
                   'rainfall': '🌧️', 'aqi': '🏭'}
    
    selected_metric = st.sidebar.selectbox(
        "📊 Data Stream", 
        [f"{metric_icons[m]} {m.title()}" for m in metrics],
        help="Select monitoring parameter"
    )
    selected_metric = selected_metric.split(' ')[1].lower()
    
    forecast_hours = st.sidebar.slider("⏱️ Forecast Horizon", 6, 72, 24,
                                      help="Prediction time range (hours)")
    
    # Real-time status indicator
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔴 SYSTEM STATUS")
    st.sidebar.markdown("🟢 **NEURAL NETWORK**: ONLINE")
    st.sidebar.markdown("🟢 **DATA STREAMS**: ACTIVE")
    st.sidebar.markdown("🟢 **PREDICTION ENGINE**: OPERATIONAL")
    
    # Main dashboard layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 📊 NEURAL ANALYSIS MATRIX")
        
        # Load model and create forecast
        model = load_model(selected_city, selected_metric)
        forecast_df = None
        
        if model:
            try:
                future = model.make_future_dataframe(periods=forecast_hours, freq='H')
                forecast_df = model.predict(future)
                forecast_df = forecast_df[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
            except Exception as e:
                st.error(f"Neural prediction failed: {e}")
        
        # Create and display futuristic plot
        fig = create_futuristic_forecast_plot(df, selected_city, selected_metric, forecast_df)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🚨 THREAT ASSESSMENT")
        
        # Get latest data for alerts
        latest_data = df[df['city'] == selected_city].iloc[-1]
        current_values = {
            'temperature': latest_data['temperature'],
            'humidity': latest_data['humidity'],
            'rainfall': latest_data['rainfall'],
            'aqi': latest_data['aqi']
        }
        
        # Check for alerts with futuristic display
        alert_system = ClimateAlertSystem()
        alerts = alert_system.check_thresholds(current_values)
        
        if alerts:
            for alert in alerts:
                if alert['severity'] == 'HIGH':
                    create_futuristic_alert(
                        f"🚨 CRITICAL: {alert['metric'].upper()} at {alert['value']}", 
                        "high"
                    )
                else:
                    create_futuristic_alert(
                        f"⚠️ WARNING: {alert['metric'].upper()} at {alert['value']}", 
                        "medium"
                    )
        else:
            create_futuristic_alert("✅ ALL SYSTEMS NOMINAL", "normal")
        
        # Current values with futuristic metric cards
        st.markdown("### 📈 LIVE TELEMETRY")
        
        for metric, value in current_values.items():
            if not pd.isna(value):
                icon = metric_icons.get(metric, "📊")
                unit = {"temperature": "°C", "humidity": "%", 
                       "rainfall": "mm", "aqi": ""}[metric]
                create_futuristic_metric_card(
                    f"{icon} {metric.title()}", 
                    f"{value:.1f}", 
                    unit
                )
    
    # Enhanced data table with futuristic styling
    st.markdown("---")
    st.markdown("### 📋 NEURAL DATA MATRIX")
    
    city_data = df[df['city'] == selected_city].tail(10)
    city_data_display = city_data.copy()
    city_data_display['timestamp'] = city_data_display['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    
    st.dataframe(
        city_data_display,
        use_container_width=True,
        hide_index=True
    )
    
    # Summary statistics with enhanced layout
    st.markdown("### 📊 STATISTICAL ANALYSIS")
    
    cols = st.columns(4)
    city_data = df[df['city'] == selected_city]
    
    stats = [
        ("🌡️ Avg Temp", f"{city_data['temperature'].mean():.1f}°C"),
        ("💧 Avg Humidity", f"{city_data['humidity'].mean():.1f}%"),
        ("🌧️ Total Rain", f"{city_data['rainfall'].sum():.1f}mm"),
        ("🏭 Avg AQI", f"{city_data['aqi'].mean():.1f}" if not city_data['aqi'].isna().all() else "N/A")
    ]
    
    for i, (label, value) in enumerate(stats):
        with cols[i]:
            create_futuristic_metric_card(label, value)


if __name__ == "__main__":
    main()