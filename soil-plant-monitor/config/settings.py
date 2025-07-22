import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database settings
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///soil_monitor.db')
    
    # Sensor settings
    SENSOR_READ_INTERVAL = int(os.getenv('SENSOR_READ_INTERVAL', 300))  # 5 minutes
    
    # Alert thresholds
    SOIL_PH_MIN = float(os.getenv('SOIL_PH_MIN', 6.0))
    SOIL_PH_MAX = float(os.getenv('SOIL_PH_MAX', 7.5))
    SOIL_MOISTURE_MIN = float(os.getenv('SOIL_MOISTURE_MIN', 30.0))
    SOIL_MOISTURE_MAX = float(os.getenv('SOIL_MOISTURE_MAX', 80.0))
    SOIL_TEMP_MIN = float(os.getenv('SOIL_TEMP_MIN', 15.0))
    SOIL_TEMP_MAX = float(os.getenv('SOIL_TEMP_MAX', 30.0))
    
    # NPK optimal ranges (ppm)
    NITROGEN_MIN = float(os.getenv('NITROGEN_MIN', 20.0))
    NITROGEN_MAX = float(os.getenv('NITROGEN_MAX', 50.0))
    PHOSPHORUS_MIN = float(os.getenv('PHOSPHORUS_MIN', 10.0))
    PHOSPHORUS_MAX = float(os.getenv('PHOSPHORUS_MAX', 30.0))
    POTASSIUM_MIN = float(os.getenv('POTASSIUM_MIN', 15.0))
    POTASSIUM_MAX = float(os.getenv('POTASSIUM_MAX', 40.0))
    
    # Plant health thresholds
    PLANT_HEALTH_SCORE_MIN = float(os.getenv('PLANT_HEALTH_SCORE_MIN', 70.0))
    GROWTH_RATE_MIN = float(os.getenv('GROWTH_RATE_MIN', 0.5))  # cm/week
    
    # Email settings
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    EMAIL_USER = os.getenv('EMAIL_USER', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    ALERT_RECIPIENTS = os.getenv('ALERT_RECIPIENTS', '').split(',')
    
    # Dashboard settings
    DASHBOARD_HOST = os.getenv('DASHBOARD_HOST', '127.0.0.1')
    DASHBOARD_PORT = int(os.getenv('DASHBOARD_PORT', 8050))
    
    # Data retention (days)
    DATA_RETENTION_DAYS = int(os.getenv('DATA_RETENTION_DAYS', 365))
