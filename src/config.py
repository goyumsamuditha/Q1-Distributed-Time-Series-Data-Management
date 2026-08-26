import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("influxdb_url","http://localhost:8086")
token = os.getenv("docker_influxdb_init_admin_token","my-super-secret-auth-token")
org = os.getenv("docker_influxdb_init_org","weather_org")
bucket = os.getenv("docker_influxdb_init_bucket","weather_bucket")
