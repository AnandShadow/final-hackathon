"""
alert_system.py
Sends email and SMS alerts when climate risk thresholds are exceeded.
"""
import os
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from twilio.rest import Client
import joblib
from datetime import datetime

# Load environment variables
load_dotenv()
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_PHONE = os.getenv('TWILIO_PHONE')


class ClimateAlertSystem:
    def __init__(self):
        self.thresholds = {
            'temperature': {'high': 40, 'low': 0},  # Celsius
            'aqi': {'high': 200, 'low': 0},         # AQI index
            'rainfall': {'high': 50, 'low': 0},     # mm
            'humidity': {'high': 95, 'low': 10}     # percentage
        }
        self.alert_log = []

    def check_thresholds(self, data):
        """Check if any values exceed defined thresholds"""
        alerts = []
        
        for metric, values in self.thresholds.items():
            if metric in data:
                current_value = data[metric]
                if current_value > values['high']:
                    alerts.append({
                        'metric': metric,
                        'value': current_value,
                        'threshold': values['high'],
                        'type': 'high',
                        'severity': 'HIGH',
                        'timestamp': datetime.now()
                    })
                elif current_value < values['low']:
                    alerts.append({
                        'metric': metric,
                        'value': current_value,
                        'threshold': values['low'],
                        'type': 'low',
                        'severity': 'MEDIUM',
                        'timestamp': datetime.now()
                    })
        
        return alerts

    def send_email_alert(self, alert, recipient_email):
        """Send email alert for climate risk"""
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_USER
            msg['To'] = recipient_email
            msg['Subject'] = f"🚨 Climate Risk Alert - {alert['severity']}"
            
            body = f"""
            Climate Risk Alert
            
            Metric: {alert['metric'].title()}
            Current Value: {alert['value']}
            Threshold: {alert['threshold']} ({alert['type']})
            Severity: {alert['severity']}
            Time: {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
            
            Please take appropriate action.
            
            Automated Climate Risk Prediction System
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            text = msg.as_string()
            server.sendmail(EMAIL_USER, recipient_email, text)
            server.quit()
            
            print(f"Email alert sent for {alert['metric']}")
            return True
            
        except Exception as e:
            print(f"Email alert failed: {e}")
            return False

    def send_sms_alert(self, alert, recipient_phone):
        """Send SMS alert using Twilio"""
        try:
            client = Client(TWILIO_SID, TWILIO_TOKEN)
            
            message_body = f"🚨 Climate Alert: {alert['metric'].title()} is {alert['value']} (threshold: {alert['threshold']}). Severity: {alert['severity']}"
            
            message = client.messages.create(
                body=message_body,
                from_=TWILIO_PHONE,
                to=recipient_phone
            )
            
            print(f"SMS alert sent for {alert['metric']}")
            return True
            
        except Exception as e:
            print(f"SMS alert failed: {e}")
            return False

    def process_alerts(self, data, email=None, phone=None):
        """Process data and send alerts if thresholds are exceeded"""
        alerts = self.check_thresholds(data)
        
        for alert in alerts:
            # Log the alert
            self.alert_log.append(alert)
            
            # Send email alert
            if email and EMAIL_USER and EMAIL_PASS:
                self.send_email_alert(alert, email)
            
            # Send SMS alert
            if phone and TWILIO_SID and TWILIO_TOKEN:
                self.send_sms_alert(alert, phone)
        
        return alerts

    def save_alert_log(self, filename="data/alert_log.csv"):
        """Save alert log to CSV file"""
        if self.alert_log:
            df = pd.DataFrame(self.alert_log)
            df.to_csv(filename, index=False)
            print(f"Alert log saved to {filename}")


def check_forecast_alerts(city='Delhi', email=None, phone=None):
    """Check forecast data for potential alerts"""
    try:
        # Load the trained model
        model = joblib.load(f"data/prophet_{city}_temperature.joblib")
        
        # Get forecast
        future = model.make_future_dataframe(periods=24, freq='H')
        forecast = model.predict(future)
        
        # Get the latest forecast values
        latest_forecast = forecast.iloc[-1]
        
        # Check for temperature alerts
        alert_system = ClimateAlertSystem()
        forecast_data = {
            'temperature': latest_forecast['yhat'],
            'city': city
        }
        
        alerts = alert_system.process_alerts(forecast_data, email, phone)
        
        if alerts:
            print(f"Found {len(alerts)} forecast alerts for {city}")
            alert_system.save_alert_log()
        else:
            print(f"No forecast alerts for {city}")
            
        return alerts
        
    except Exception as e:
        print(f"Forecast alert check failed: {e}")
        return []


if __name__ == "__main__":
    # Example usage
    alert_system = ClimateAlertSystem()
    
    # Test with sample data
    test_data = {
        'temperature': 42,  # High temperature
        'aqi': 250,         # High AQI
        'rainfall': 5,      # Normal rainfall
        'humidity': 70      # Normal humidity
    }
    
    print("Testing alert system with sample data:")
    alerts = alert_system.process_alerts(
        test_data, 
        email="your_email@example.com",  # Replace with actual email
        phone="+1234567890"              # Replace with actual phone
    )
    
    if alerts:
        print(f"Generated {len(alerts)} alerts")
        for alert in alerts:
            print(f"- {alert['severity']} alert for {alert['metric']}: {alert['value']}")
    
    # Test forecast alerts
    print("\nChecking forecast alerts:")
    check_forecast_alerts('Delhi')