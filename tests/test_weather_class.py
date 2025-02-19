import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
import pytz
import requests


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if "api-ninjas.com/v1/weather" in args[0]:
        return MockResponse({
            "temp": 15,
            "feels_like": 14,
            "humidity": 60,
            "wind_speed": 5,
            "sunrise": 1708406400,  # Mocked timestamp
            "sunset": 1708449600  # Mocked timestamp
        }, 200)
    return MockResponse(None, 404)


class TestWeatherAPI(unittest.TestCase):
    @patch('requests.get', side_effect=mocked_requests_get)
    def test_weather_data_fetch(self, mock_get):
        from your_script import latitude, longitude, api_url, api_key
        response = requests.get(api_url, headers={'X-Api-Key': api_key})
        self.assertEqual(response.status_code, 200)
        weather_data = response.json()
        self.assertIn("temp", weather_data)
        self.assertIn("feels_like", weather_data)
        self.assertIn("humidity", weather_data)
        self.assertIn("wind_speed", weather_data)
        self.assertIn("sunrise", weather_data)
        self.assertIn("sunset", weather_data)

    def test_sunrise_sunset_conversion(self):
        sunrise_timestamp = 1708406400  # Mocked timestamp
        sunset_timestamp = 1708449600  # Mocked timestamp
        sunrise_utc = datetime.fromtimestamp(sunrise_timestamp, timezone.utc)
        sunset_utc = datetime.fromtimestamp(sunset_timestamp, timezone.utc)
        berlin_tz = pytz.timezone("Europe/Berlin")
        sunrise_time = sunrise_utc.astimezone(berlin_tz).strftime('%H:%M:%S')
        sunset_time = sunset_utc.astimezone(berlin_tz).strftime('%H:%M:%S')
        sun_hours = (sunset_utc - sunrise_utc).seconds // 3600
        self.assertEqual(sun_hours, 12)  # 12-hour daylight period


if __name__ == '__main__':
    unittest.main()
