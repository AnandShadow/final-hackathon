"""
data_preprocessing.py
Cleans and formats climate data for time-series modeling.
"""
import pandas as pd
import numpy as np
from datetime import datetime

def preprocess_realtime_data(input_path="data/realtime_climate.csv", output_path="data/processed_climate.csv"):
    df = pd.read_csv(input_path)
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    # Sort by timestamp
    df = df.sort_values('timestamp')
    # Fill missing values
    df['temperature'] = df['temperature'].fillna(method='ffill').fillna(method='bfill')
    df['humidity'] = df['humidity'].fillna(method='ffill').fillna(method='bfill')
    df['rainfall'] = df['rainfall'].fillna(0)
    df['aqi'] = df['aqi'].fillna(method='ffill').fillna(method='bfill')
    # Remove duplicates
    df = df.drop_duplicates(subset=['timestamp', 'city'])
    # Save processed data
    df.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    preprocess_realtime_data()
