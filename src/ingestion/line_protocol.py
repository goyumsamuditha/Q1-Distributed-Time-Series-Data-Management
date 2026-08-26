from influxdb_client import point

def record_to_line_protocol(record: dict) -> Point:
    """ Convert a weather observation record to InfluxDB line protocol format."""
    
    return Point("weather_observations").tag("summary", record['summary']) \
        .tag("precip_type", record['precip_type']) \
        .field("temperature", record['temperature']) \
        .field("apparent_temperature", record['apparent_temperature']) \
        .field("humidity", record['humidity']) \
        .field("wind_speed", record['wind_speed']) \
        .field("wind_bearing", record['wind_bearing']) \
        .field("visibility", record['visibility']) \
        .field("pressure", record['pressure']) \
        .time(record['timestamp'])
        
        