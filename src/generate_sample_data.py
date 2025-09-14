"""
generate_sample_data.py
Generates synthetic historical climate data for modeling when real data is insufficient.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_synthetic_data(days=30, cities=['Delhi', 'Mumbai', 'London', 'New York']):
    """Generate synthetic climate data for the past 'days' days"""
    data = []
    base_date = datetime.now() - timedelta(days=days)
    
    # City-specific temperature ranges and patterns
    city_params = {
        'Delhi': {'temp_base': 30, 'temp_var': 8, 'humidity_base': 65, 'aqi_base': 150},
        'Mumbai': {'temp_base': 28, 'temp_var': 5, 'humidity_base': 80, 'aqi_base': 120},
        'London': {'temp_base': 15, 'temp_var': 6, 'humidity_base': 70, 'aqi_base': 50},
        'New York': {'temp_base': 22, 'temp_var': 7, 'humidity_base': 65, 'aqi_base': 80}
    }
    
    for day in range(days):
        for hour in range(0, 24, 3):  # Every 3 hours
            timestamp = base_date + timedelta(days=day, hours=hour)
            
            for city in cities:
                params = city_params[city]
                
                # Generate temperature with daily and seasonal patterns
                daily_pattern = 3 * np.sin(2 * np.pi * hour / 24)  # Daily temperature cycle
                seasonal_pattern = 2 * np.sin(2 * np.pi * day / 365)  # Seasonal pattern
                temp_noise = np.random.normal(0, 2)
                temperature = params['temp_base'] + daily_pattern + seasonal_pattern + temp_noise
                
                # Generate humidity
                humidity = params['humidity_base'] + np.random.normal(0, 10)
                humidity = max(30, min(100, humidity))  # Clamp between 30-100%
                
                # Generate rainfall (sporadic)
                rainfall = np.random.exponential(0.5) if np.random.random() < 0.1 else 0
                
                # Generate AQI
                aqi = params['aqi_base'] + np.random.normal(0, 30)
                aqi = max(10, aqi)  # Minimum AQI of 10
                
                data.append({
                    'timestamp': timestamp,
                    'city': city,
                    'temperature': round(temperature, 2),
                    'humidity': round(humidity, 1),
                    'rainfall': round(rainfall, 2),
                    'aqi': round(aqi, 1)
                })
    
    df = pd.DataFrame(data)
    return df


def combine_with_realtime_data():
    """Combine synthetic historical data with real-time data"""
    # Generate synthetic historical data
    synthetic_df = generate_synthetic_data(days=30)
    
    # Try to load real-time data
    try:
        realtime_df = pd.read_csv("data/realtime_climate.csv")
        realtime_df['timestamp'] = pd.to_datetime(realtime_df['timestamp'])
        # Combine both datasets
        combined_df = pd.concat([synthetic_df, realtime_df], ignore_index=True)
    except FileNotFoundError:
        print("No real-time data found, using only synthetic data")
        combined_df = synthetic_df
    
    # Sort by timestamp and remove duplicates
    combined_df = combined_df.sort_values('timestamp')
    combined_df = combined_df.drop_duplicates(subset=['timestamp', 'city'])
    
    # Save combined data
    combined_df.to_csv("data/combined_climate.csv", index=False)
    print(f"Generated {len(combined_df)} data points and saved to data/combined_climate.csv")
    
    return combined_df


if __name__ == "__main__":
    df = combine_with_realtime_data()
    print(f"Data shape: {df.shape}")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"Cities: {df['city'].unique()}")