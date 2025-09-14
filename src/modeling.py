"""
modeling.py
Trains Prophet model for short-term climate forecasts. Optionally supports LSTM for advanced modeling.
"""
import pandas as pd
from prophet import Prophet
import joblib
from sklearn.metrics import mean_absolute_error

# --- Prophet Modeling ---
def train_prophet(df, target, city):
    # Prepare data for Prophet
    df_city = df[df['city'] == city].copy()
    df_city = df_city.dropna(subset=[target])
    df_city.rename(columns={'timestamp': 'ds', target: 'y'}, inplace=True)
    model = Prophet()
    model.fit(df_city[['ds', 'y']])
    return model

def forecast_prophet(model, periods=24):
    future = model.make_future_dataframe(periods=periods, freq='H')
    forecast = model.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

def evaluate_model(model, df_city):
    future = model.make_future_dataframe(periods=0)
    forecast = model.predict(future)
    y_true = df_city['y'].values
    y_pred = forecast['yhat'].values[:len(y_true)]
    mae = mean_absolute_error(y_true, y_pred)
    return mae

def save_model(model, filename):
    joblib.dump(model, filename)
    print(f"Model saved to {filename}")

def load_model(filename):
    return joblib.load(filename)

if __name__ == "__main__":
    df = pd.read_csv("data/combined_climate.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    target = 'temperature'  # You can change to 'humidity', 'rainfall', or 'aqi'
    city = 'Delhi'  # Example city
    
    print(f"Training Prophet model for {target} in {city}")
    print(f"Dataset shape: {df.shape}")
    print(f"Available data points for {city}: {len(df[df['city'] == city])}")
    
    model = train_prophet(df, target, city)
    forecast = forecast_prophet(model, periods=24)
    print("\nForecast for next 24 hours:")
    print(forecast.tail(10))
    
    city_data = df[df['city'] == city].dropna(subset=[target])
    city_data = city_data.rename(columns={'timestamp': 'ds', target: 'y'})
    mae = evaluate_model(model, city_data)
    print(f"\nModel MAE: {mae:.2f}")
    save_model(model, f"data/prophet_{city}_{target}.joblib")
