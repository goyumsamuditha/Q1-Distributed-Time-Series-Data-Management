import pytest
import pandas as pd
from src.ingestion.line_protocol import record_to_line_protocol


def test_parse_line_protocol():
    """ Unit test for the parse_line_protocol function."""
    sample_record = {
        'timestamp': pd.to_datetime('2006-04-01 00:00:00.000+0200'),
        'summary': 'Clear',
        'precip_type': 'rain',
        'temperature': 9.47,
        'apparent_temperature': 7.38,
        'humidity': 0.89,
        'wind_speed': 14.12,
        'wind_bearing': 251.0,
        'visibility': 15.82,
        'pressure': 1015.13
    }
    point = record_to_line_protocol(sample_record)
    line_protocol = point.to_line_protocol()
    
    assert "weather_observations" in line_protocol
    assert "summary=Clear" in line_protocol
    assert "temperature=9.47" in line_protocol
    print("Unit test for parse_line_protocol passed successfully.")