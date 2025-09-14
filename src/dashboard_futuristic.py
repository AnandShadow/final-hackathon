"""
dashboard_futuristic.py
Clean futuristic dashboard without problematic font configurations.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
from alert_system import ClimateAlertSystem


def apply_futuristic_theme():
    """Apply futuristic CSS styling"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #00ffff;
    }
    
    .main-header {
        background: linear-gradient(90deg, #00ffff, #0080ff, #8000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 3rem;
        text-align: center;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(128, 0, 255, 0.1));
        border: 1px solid #00ffff;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
    }
    
    .alert-high {
        background: linear-gradient(135deg, rgba(255, 0, 100, 0.2), rgba(255, 50, 50, 0.2));
        border: 2px solid #ff0066;
        border-radius: 10px;
        padding: 15px;
        animation: pulse 1.5s infinite;
    }
    
    .alert-normal {
        background: linear-gradient(135deg, rgba(0, 255, 100, 0.2), rgba(50, 255, 50, 0.2));
        border: 2px solid #00ff66;
        border-radius: 10px;
        padding: 15px;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(0, 255, 255, 0.5); }
        to { text-shadow: 0 0 30px rgba(0, 255, 255, 0.8); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 20px rgba(255, 0, 102, 0.5); }
        50% { box-shadow: 0 0 40px rgba(255, 0, 102, 0.8); }
        100% { box-shadow: 0 0 20px rgba(255, 0, 102, 0.5); }
    }
    
    .stSelectbox > div > div {
        background: rgba(26, 26, 46, 0.8);
        border: 1px solid #00ffff;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


def create_futuristic_metric_card(title, value, unit=""):
    """Create a futuristic metric display card"""
    st.markdown(f"""
    <div class="metric-card">
        <h4 style='color: #00ffff; margin: 0;'>{title}</h4>
        <h2 style='color: #ffffff; margin: 5px 0;'>{value}{unit}</h2>
    </div>
    """, unsafe_allow_html=True)


def create_futuristic_alert(message, alert_type="normal"):
    """Create futuristic alert display"""
    st.markdown(f"""
    <div class="alert-{alert_type}">
        <p style='margin: 0; font-weight: 700;'>{message}</p>
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
        st.warning(f"Model not found for {city} {metric}.")
        return None


def create_futuristic_plot(df, city, metric, forecast_df=None):
    """Create futuristic forecast plot"""
    city_data = df[df['city'] == city].copy()
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=city_data['timestamp'],
        y=city_data[metric],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='#00ffff', width=3),
        marker=dict(color='#00ffff', size=6)
    ))
    
    # Forecast data
    if forecast_df is not None:
        forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
        
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'],
            y=forecast_df['yhat'],
            mode='lines+markers',
            name='AI Forecast',
            line=dict(color='#ff0080', width=4, dash='dot'),
            marker=dict(color='#ff0080', size=8)
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'],
            y=forecast_df['yhat_upper'],
            mode='lines',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'],
            y=forecast_df['yhat_lower'],
            mode='lines',
            fill='tonexty',
            line=dict(width=0),
            name='Confidence Zone',
            fillcolor='rgba(255, 0, 128, 0.2)'
        ))
    
    # Simple styling without problematic font configs
    fig.update_layout(
        title=f'🌐 {metric.upper()} NEURAL FORECAST - {city.upper()}',
        xaxis_title='TEMPORAL AXIS',
        yaxis_title=f'{metric.upper()} READINGS',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ffff'),
        hovermode='x unified'
    )
    
    fig.update_xaxes(gridcolor='rgba(0, 255, 255, 0.2)')
    fig.update_yaxes(gridcolor='rgba(0, 255, 255, 0.2)')
    
    return fig


def main():
    """Main futuristic dashboard"""
    st.set_page_config(
        page_title="🌐 CLIMATE.AI Neural System",
        page_icon="🌡️",
        layout="wide"
    )
    
    apply_futuristic_theme()
    
    st.markdown('<h1 class="main-header">🌐 CLIMATE.AI NEURAL PREDICTION SYSTEM</h1>', 
                unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar
    st.sidebar.markdown("## 🎛️ CONTROL PANEL")
    
    cities = df['city'].unique()
    selected_city = st.sidebar.selectbox("🏙️ Neural Node", cities)
    
    metrics = ['temperature', 'humidity', 'rainfall', 'aqi']
    metric_icons = {'temperature': '🌡️', 'humidity': '💧', 
                   'rainfall': '🌧️', 'aqi': '🏭'}
    
    selected_metric = st.sidebar.selectbox(
        "📊 Data Stream", 
        [f"{metric_icons[m]} {m.title()}" for m in metrics]
    )
    selected_metric = selected_metric.split(' ')[1].lower()
    
    forecast_hours = st.sidebar.slider("⏱️ Forecast Horizon", 6, 72, 24)
    
    # System status
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔴 SYSTEM STATUS")
    st.sidebar.markdown("🟢 **NEURAL NETWORK**: ONLINE")
    st.sidebar.markdown("🟢 **DATA STREAMS**: ACTIVE")
    st.sidebar.markdown("🟢 **PREDICTION ENGINE**: OPERATIONAL")
    
    # Main layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 📊 NEURAL ANALYSIS MATRIX")
        
        # Load model and forecast
        model = load_model(selected_city, selected_metric)
        forecast_df = None
        
        if model:
            try:
                future = model.make_future_dataframe(periods=forecast_hours, freq='H')
                forecast_df = model.predict(future)
                forecast_df = forecast_df[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
            except Exception as e:
                st.error(f"Neural prediction failed: {e}")
        
        # Display plot
        fig = create_futuristic_plot(df, selected_city, selected_metric, forecast_df)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🚨 THREAT ASSESSMENT")
        
        # Get latest data
        latest_data = df[df['city'] == selected_city].iloc[-1]
        current_values = {
            'temperature': latest_data['temperature'],
            'humidity': latest_data['humidity'],
            'rainfall': latest_data['rainfall'],
            'aqi': latest_data['aqi']
        }
        
        # Check alerts
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
                        "normal"
                    )
        else:
            create_futuristic_alert("✅ ALL SYSTEMS NOMINAL", "normal")
        
        # Live telemetry
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
    
    # Data table
    st.markdown("---")
    st.markdown("### 📋 NEURAL DATA MATRIX")
    
    city_data = df[df['city'] == selected_city].tail(10)
    city_data_display = city_data.copy()
    city_data_display['timestamp'] = city_data_display['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    
    st.dataframe(city_data_display, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()