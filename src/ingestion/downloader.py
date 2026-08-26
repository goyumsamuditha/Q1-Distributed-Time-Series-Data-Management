import os
import shutil
import kagglehub
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_dataset(dir: str = "data/raw"):
    """ Download the Szeged Weather and Weather Data datasets. """
    os.makedirs(dir, exist_ok=True)
    
    # Download the dataset from Kaggle
    logger.info("Downloading Szeged Weather dataset via kagglehub...")
    path = kagglehub.dataset_download("budincsevity/szeged-weather")
    logger.info(f"Dataset downloaded to: {path}")

    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            shutil.copy(os.path.join(path, filename),dir)
            logger.info(f"Copied {filename} to {dir}")
    
    logger.info("Downloading Weather Data repository via kagglehub...")
    weather_data_path = kagglehub.dataset_download("rohitgrewal/weather-data")
    logger.info(f"Weather Data repository downloaded to: {weather_data_path}")
    
    for filename in os.listdir(weather_data_path):
        if filename.endswith(".csv"):
            shutil.copy(os.path.join(weather_data_path, filename),dir)
            logger.info(f"Copied {filename} to {dir}")
            
if __name__ == "__main__":
    download_dataset()