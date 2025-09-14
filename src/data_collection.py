"""
data_collection.py
Collects real-time climate data from OpenWeatherMap and AQICN APIs,
and downloads historical datasets from Kaggle/NASA.
"""
import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
AQICN_API_KEY = os.getenv('AQICN_API_KEY')

# --- Real-time Data Collection ---
def fetch_openweather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        return {
            'timestamp': datetime.utcnow(),
            'city': city,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'rainfall': data.get('rain', {}).get('1h', 0),
        }
    except Exception as e:
        print(f"OpenWeatherMap error: {e}")
        return None

def fetch_aqicn(city):
    url = f"https://api.waqi.info/feed/{city}/?token={AQICN_API_KEY}"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        aqi = data['data']['aqi'] if 'data' in data and 'aqi' in data['data'] else None
        return {
            'timestamp': datetime.utcnow(),
            'city': city,
            'aqi': aqi
        }
    except Exception as e:
        print(f"AQICN error: {e}")
        return None

def collect_realtime_data(cities):
    records = []
    for city in cities:
        weather = fetch_openweather(city)
        aqi = fetch_aqicn(city)
        if weather and aqi:
            record = {**weather, **aqi}
            records.append(record)
    df = pd.DataFrame(records)
    df.to_csv("data/realtime_climate.csv", index=False)
    print("Saved real-time data to data/realtime_climate.csv")

# --- Historical Data Download (Placeholder) ---
def download_historical_data():
    # Download from Kaggle/NASA manually or via API
    print("Please download historical datasets from Kaggle/NASA and place in data/historical/")

if __name__ == "__main__":
    cities = ["Delhi", "Mumbai", "London", "New York"]
    collect_realtime_data(cities)
    download_historical_data()
