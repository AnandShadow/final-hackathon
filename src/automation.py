"""
automation.py
Automated pipeline execution and logging for climate risk prediction system.
"""
import schedule
import time
import logging
import os
from datetime import datetime
from data_collection import collect_realtime_data
from data_preprocessing import preprocess_realtime_data
from modeling import train_prophet, save_model
from alert_system import check_forecast_alerts
import pandas as pd


# Setup logging
def setup_logging():
    """Setup logging configuration"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/climate_pipeline.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def run_data_collection():
    """Run data collection pipeline"""
    logger = logging.getLogger(__name__)
    try:
        logger.info("Starting data collection...")
        cities = ["Delhi", "Mumbai", "London", "New York"]
        collect_realtime_data(cities)
        logger.info("Data collection completed successfully")
        return True
    except Exception as e:
        logger.error(f"Data collection failed: {e}")
        return False


def run_preprocessing():
    """Run data preprocessing pipeline"""
    logger = logging.getLogger(__name__)
    try:
        logger.info("Starting data preprocessing...")
        preprocess_realtime_data()
        logger.info("Data preprocessing completed successfully")
        return True
    except Exception as e:
        logger.error(f"Data preprocessing failed: {e}")
        return False


def run_model_training():
    """Run model training for all cities and metrics"""
    logger = logging.getLogger(__name__)
    try:
        logger.info("Starting model training...")
        df = pd.read_csv("data/combined_climate.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        cities = df['city'].unique()
        metrics = ['temperature', 'humidity', 'rainfall', 'aqi']
        
        for city in cities:
            for metric in metrics:
                try:
                    city_data = df[df['city'] == city].dropna(subset=[metric])
                    if len(city_data) >= 2:  # Minimum data requirement
                        model = train_prophet(df, metric, city)
                        save_model(model, f"data/prophet_{city}_{metric}.joblib")
                        logger.info(f"Model trained for {city} - {metric}")
                    else:
                        logger.warning(f"Insufficient data for {city} - {metric}")
                except Exception as e:
                    logger.error(f"Model training failed for {city} - {metric}: {e}")
        
        logger.info("Model training completed")
        return True
    except Exception as e:
        logger.error(f"Model training pipeline failed: {e}")
        return False


def run_alert_checks():
    """Run alert checks for all cities"""
    logger = logging.getLogger(__name__)
    try:
        logger.info("Starting alert checks...")
        cities = ["Delhi", "Mumbai", "London", "New York"]
        
        for city in cities:
            alerts = check_forecast_alerts(city)
            if alerts:
                logger.warning(f"Found {len(alerts)} alerts for {city}")
            else:
                logger.info(f"No alerts for {city}")
        
        logger.info("Alert checks completed")
        return True
    except Exception as e:
        logger.error(f"Alert checks failed: {e}")
        return False


def run_full_pipeline():
    """Run the complete climate prediction pipeline"""
    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info("STARTING FULL CLIMATE PREDICTION PIPELINE")
    logger.info("=" * 50)
    
    # Step 1: Data Collection
    if not run_data_collection():
        logger.error("Pipeline failed at data collection step")
        return False
    
    # Step 2: Data Preprocessing
    if not run_preprocessing():
        logger.error("Pipeline failed at preprocessing step")
        return False
    
    # Step 3: Model Training (optional, only if models don't exist)
    model_exists = os.path.exists("data/prophet_Delhi_temperature.joblib")
    if not model_exists:
        logger.info("No existing models found, training new models...")
        if not run_model_training():
            logger.error("Pipeline failed at model training step")
            return False
    else:
        logger.info("Using existing trained models")
    
    # Step 4: Alert Checks
    if not run_alert_checks():
        logger.error("Pipeline failed at alert checks step")
        return False
    
    logger.info("=" * 50)
    logger.info("PIPELINE COMPLETED SUCCESSFULLY")
    logger.info("=" * 50)
    return True


def create_windows_task_scheduler_script():
    """Create a Windows Task Scheduler batch script"""
    batch_content = f"""@echo off
cd /d "{os.getcwd()}"
python src/automation.py --run-once
"""
    
    with open("run_climate_pipeline.bat", "w") as f:
        f.write(batch_content)
    
    print("Created run_climate_pipeline.bat for Windows Task Scheduler")
    print("To schedule:")
    print("1. Open Task Scheduler")
    print("2. Create Basic Task")
    print("3. Set schedule (e.g., daily at 6 AM)")
    print("4. Action: Start a program")
    print(f"5. Program: {os.getcwd()}\\run_climate_pipeline.bat")


def schedule_jobs():
    """Schedule automated jobs"""
    logger = logging.getLogger(__name__)
    
    # Schedule data collection every 3 hours
    schedule.every(3).hours.do(run_data_collection)
    
    # Schedule preprocessing every 3 hours (after data collection)
    schedule.every(3).hours.do(run_preprocessing)
    
    # Schedule alert checks every hour
    schedule.every().hour.do(run_alert_checks)
    
    # Schedule full pipeline once daily at 6 AM
    schedule.every().day.at("06:00").do(run_full_pipeline)
    
    logger.info("Scheduled jobs:")
    logger.info("- Data collection: Every 3 hours")
    logger.info("- Data preprocessing: Every 3 hours")
    logger.info("- Alert checks: Every hour")
    logger.info("- Full pipeline: Daily at 6:00 AM")


def main():
    """Main automation function"""
    import sys
    
    logger = setup_logging()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--run-once":
        # Run pipeline once and exit (for Task Scheduler)
        run_full_pipeline()
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == "--create-task":
        # Create Windows Task Scheduler script
        create_windows_task_scheduler_script()
        return
    
    # Run continuous scheduling
    logger.info("Starting climate prediction automation...")
    schedule_jobs()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Automation stopped by user")


if __name__ == "__main__":
    main()