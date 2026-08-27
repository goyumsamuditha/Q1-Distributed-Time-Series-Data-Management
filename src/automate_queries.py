import sys
import os
import logging
from influxdb_client import InfluxDBClient
from influxdb_client.domain.bucket_retention_rules import BucketRetentionRules

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import url, token, org

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def read_flux_file(file_path: str) -> str:
    """Reads a Flux query from a file and returns it as a string."""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','flux', file_path))
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"Flux query file not found: {file_path}")
        SYS.exit(1)
        
        
def automate_queries():
    """ Automates the execution of queries for time-series data management, including window aggregation, anomaly detection, 
    historical backfill, and task registration."""
    client = InfluxDBClient(url=url, token=token, org=org)
    query_api = client.query_api()
    bucket_api = client.buckets_api()
    tasks_api = client.tasks_api()
    org_api = client.organizations_api()
    
    org = org_api.find_organizations(org=org)[0].id
    
    bucket_name = "weather_downsampled"
    existing_buckets = bucket_api.find_bucket_by_name(bucket_name)
    
    if not existing_buckets:
        logging.info(f"Creating bucket: {bucket_name}, with retention policy of 30 days")
        retention_rules = BucketRetentionRules(type="expire", every_seconds=30 * 24 * 60 * 60)
        bucket_api.create_bucket(bucket_name=bucket_name, org_id=org, retention_rules=[retention_rules])
        logging.info(f"Bucket {bucket_name} created successfully.")
    else:
        logging.info(f"Bucket {bucket_name} already exists.")
        
        
        
        
    logging.info("\n--- Window Aggregation (Hourley Average) ---")
    query_aggregation = read_flux_file("window_aggregation.flux") 
    
    table = query_api.query(query_aggregation)
    for table in table:
        for record in table.records:
            if count < 5:  # Limit to first 5 records for logging
                print(f"Hourly Avg Temp - Time: {record.get_time()}, Temperature: {record.get_value():.2f}°C")
                count += 1
            
    
    logging.info("\n--- Running Anomaly Detection Task ---")
    query_anomaly = read_flux_file("anomaly_detection.flux")

    table = query_api.query(query_anomaly)
    count = 0
    for table in table:
        for record in table.records:
            if count < 5:  # Limit to first 5 anomalies for logging
                print(f"Anomaly Detected - Time: {record.get_time()}, Temperature: {record.get_value():.2f}°C")
                count += 1
            
    
    logging.info("\n--- Executing Historical Backfill to Downsampled Bucket ---")
    query_backfill = read_flux_file("downsampling_task.flux")
    
    query_api.query(query_backfill) 
    logging.info("Historical backfill executed successfully.")
    
    
    task_name = "downsample_weather_data"
    existing_tasks = tasks_api.find_tasks(name=task_name)
    if not existing_tasks:
        logging.info(f"\n--- Registering Background Task: {task_name} ---")
        task_flux = '''
        option task = {
            
            name: "downsample_weather_data",
            every: 1h,
        }
        from(bucket: "weather_bucket")
            |> range(start: -2h)
            |> filter(fn: (r) => r["_measurement"] == "weather_observations")
            |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
            |> to(bucket: "weather_downsampled", org: "weather_org")
        '''
        tasks_api.create_task(name=task_name, flux=task_flux, org=org, every="1h")
        logging.info(f"Background task {task_name} registered and scheduled to run every hour.")
        
    else:
        logging.info(f"Background task {task_name} already running.")
    client.close()
    
    logging.info("\n--- Automation of Queries Completed ---")
    
if __name__ == "__main__":
    automate_queries()