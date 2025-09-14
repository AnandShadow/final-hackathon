"""
weather_demo.py
Demo script to showcase different weather animations in the dashboard.
"""
import streamlit as st
import time


def weather_condition_demo():
    """Demo different weather conditions and their animations"""
    st.set_page_config(
        page_title="Weather Animation Demo",
        page_icon="🌦️",
        layout="wide"
    )
    
    # Weather conditions to demo
    weather_conditions = {
        'clear': {'emoji': '☀️', 'name': 'Sunny Clear Sky', 'temp': 28},
        'rain': {'emoji': '🌧️', 'name': 'Heavy Rain', 'temp': 18},
        'snow': {'emoji': '❄️', 'name': 'Snowing', 'temp': -5},
        'thunderstorm': {'emoji': '⛈️', 'name': 'Thunderstorm', 'temp': 22},
        'fog': {'emoji': '🌫️', 'name': 'Foggy', 'temp': 12},
        'clouds': {'emoji': '☁️', 'name': 'Cloudy', 'temp': 20}
    }
    
    st.title("🌦️ Weather Animation Demo")
    st.write("Select different weather conditions to see dynamic animations!")
    
    # Weather selector
    selected_weather = st.selectbox(
        "Choose Weather Condition:",
        options=list(weather_conditions.keys()),
        format_func=lambda x: f"{weather_conditions[x]['emoji']} {weather_conditions[x]['name']}"
    )
    
    weather_info = weather_conditions[selected_weather]
    
    # Apply dynamic theme based on selection
    from src.dashboard_weather_responsive import apply_weather_responsive_theme
    apply_weather_responsive_theme(
        selected_weather, 
        weather_info['temp']
    )
    
    # Display current weather info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🌡️ Temperature", f"{weather_info['temp']}°C")
    
    with col2:
        st.metric("🌤️ Condition", weather_info['name'])
    
    with col3:
        st.metric("🎨 Animation", selected_weather.title())
    
    # Animation description
    animation_descriptions = {
        'clear': "☀️ Animated sun rays with golden glow and pulsing light effects",
        'rain': "🌧️ Falling raindrops with blue color scheme and water effects",
        'snow': "❄️ Snowflakes falling and rotating with white/blue winter theme",
        'thunderstorm': "⛈️ Lightning flashes with purple/orange storm colors",
        'fog': "🌫️ Drifting fog layers with gray misty atmosphere",
        'clouds': "☁️ Floating clouds with soft blue-gray color palette"
    }
    
    st.info(f"**Current Animation:** {animation_descriptions[selected_weather]}")
    
    # Demo features
    st.markdown("### 🎮 Interactive Features")
    
    features = [
        "🎨 **Dynamic Color Schemes** - Background and UI colors change with weather",
        "✨ **Animated Particles** - Weather-specific particle effects (rain, snow, etc.)",
        "🌡️ **Temperature Responsiveness** - Animation intensity changes with temperature",
        "⚡ **Real-time Updates** - Animations respond to live weather data",
        "🎯 **Smart Indicators** - Visual cues for different weather conditions",
        "📱 **Mobile Responsive** - Animations work on all screen sizes"
    ]
    
    for feature in features:
        st.markdown(feature)
    
    # Code example
    with st.expander("🔧 How It Works"):
        st.code("""
# Weather-responsive animations in action:

1. Get current weather condition
weather_condition = get_weather_condition(city)

2. Apply dynamic theme
apply_weather_responsive_theme(weather_condition, temperature)

3. Render weather particles
if weather_condition == 'rain':
    # Show animated raindrops
elif weather_condition == 'snow':
    # Show falling snowflakes
elif weather_condition == 'thunderstorm':
    # Show lightning effects

4. Update colors and styling based on conditions
        """, language='python')
    
    # Auto-refresh button
    if st.button("🔄 Refresh Animation"):
        st.experimental_rerun()
    
    st.markdown("---")
    st.markdown("**🌍 Experience real weather animations in the main Climate AI dashboard!**")


if __name__ == "__main__":
    weather_condition_demo()