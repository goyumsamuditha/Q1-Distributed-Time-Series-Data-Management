import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_csv(file_path: str):
    """ Parse a CSV file and return a pandas DataFrame. """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Failed to read CSV file {file_path}: {e}")
        raise e
    
    for index, row in df.iterrows():
        try:
            dt = pd.to_datetime(row['Formatted Date'])
            if pd.isna(dt):
                continue
            yield = {
                'timestamp': dt,
                'summary': str(row.get('Summary', 'Unknown')),
                'precip_type': str(row.get('Precip Type', 'Unknown')),
                'temperature': float(row.get('Temperature (C)', 0.0)),
                'apparent_temperature': float(row.get('Apparent Temperature (C)', 0.0)),
                'humidity': float(row.get('Humidity', 0.0)),
                'wind_speed': float(row.get('Wind Speed (km/h)', 0.0)),
                'wind_bearing': float(row.get('Wind Bearing (degrees)', 0.0)),
                'visibility': float(row.get('Visibility (km)', 0.0)),
                'pressure': float(row.get('Pressure (millibars)', 0.0))
            }
        except Exception as e:
            logger.error(f"Error processing row {index}: {e}")
            continue