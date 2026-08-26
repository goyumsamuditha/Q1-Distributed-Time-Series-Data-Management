import sys
import os
import logging
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.config import url, token, org, bucket
from src.ingestion.line_protocol import record_to_line_protocol
from src.ingestion.parser import parse_csv


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_ingestion(file_path:str, batch_size:int=5000):
    
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    points = []
    total = 0
    
    logger.info(f"Starting ingestion form file: {file_path} into InfluxDB bucket: {bucket} with batch size: {batch_size}")
    
    for record in parse_csv(file_path):
        points.append(record_to_line_protocol(record))
        if len(points) >= batch_size:
            write_api.write(bucket=bucket, org=org, record=points)
            total += len(points)
            logger.info(f"Wrote {len(points)} points to InfluxDB. Total points written: {total}")
            points = []
            
    if points:
        write_api.write(bucket=bucket, org=org, record=points)
        total += len(points)
        logger.info(f"Wrote {len(points)} points to InfluxDB. Total points written: {total}")
        
    client.close()
    logger.info(f"Ingestion completed. Total points written: {total}")
    
if __name__ == "__main__":
    csv_file_path = sys.argv[1] if len(sys.argv) > 1 else "data/raw/weatherHistory.csv"
    run_ingestion(csv_file_path)