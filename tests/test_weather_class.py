import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import pytz
import json  # Ensure to import json for parsing the output
from application.services.weather_class import Weather

class TestWeather(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_weather(self, mock_get):
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "sunrise": "2025-02-19T06:30:00+00:00",
            "sunset": "2025-02-19T18:30:00+00:00",
            "temperature": {"min": -1},
            "temp_max": 3,
            "weather_desc": "Partly cloudy"
        }
        mock_get.return_value = mock_response

        weather_bot = Weather()
        weather_bot.fetch_weather()

        # Assert the API request was made with the correct URL
        mock_get.assert_called_once_with(
            "https://forecast.meteonomiqs.com/v3_1/forecast/52.5200/13.4050",
            headers={"x-api-key": "9wxowjP7pBaPpP5dx5GN5oxb4pGJm7V2hqQIFWpe"}
        )
        self.assertEqual(weather_bot.weather_data["sunrise"], "2025-02-19T06:30:00+00:00")

    def test_get_sun_hours(self):
        # Test with mock weather data
        weather_bot = Weather()
        weather_bot.weather_data = {
            "sunrise": "2025-02-19T06:30:00+00:00",
            "sunset": "2025-02-19T18:30:00+00:00"
        }

        # Mock timezone conversion (Berlin timezone is UTC +1 in winter)
        berlin_tz = pytz.timezone("Europe/Berlin")
        sunrise = datetime.fromisoformat(weather_bot.weather_data["sunrise"]).astimezone(pytz.utc).astimezone(berlin_tz)
        sunset = datetime.fromisoformat(weather_bot.weather_data["sunset"]).astimezone(pytz.utc).astimezone(berlin_tz)

        # Check sun hours calculation
        sunrise_time, sunset_time, sun_hours = weather_bot.get_sun_hours()

        # Expected results based on test data
        expected_sunrise = sunrise.strftime('%H:%M')
        expected_sunset = sunset.strftime('%H:%M')
        expected_sun_hours = (sunset - sunrise).seconds // 3600

        self.assertEqual(sunrise_time, expected_sunrise)
        self.assertEqual(sunset_time, expected_sunset)
        self.assertEqual(sun_hours, expected_sun_hours)

    @patch('requests.get')
    def test_get_weather_info(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "sunrise": "2025-02-19T06:30:00+00:00",
            "sunset": "2025-02-19T18:30:00+00:00",
            "temperature": {"min": -1},
            "temp_max": 3,
            "weather_desc": "Partly cloudy"
        }
        mock_get.return_value = mock_response

        weather_bot = Weather()
        weather_info = weather_bot.get_weather_info()

        expected_info = {
            "city": "Berlin",
            "max_temperature": "3°C",
            "min_temperature": "-1°C",
            "condition": "Partly cloudy",
            "sun_hours": "12 hours",
            "sunset_time": "18:30"
        }

        # Compare the string output directly
        self.assertEqual(weather_info, json.dumps(expected_info, indent=4))

    @patch('requests.get')
    def test_get_weather_info_error(self, mock_get):
        # Simulate an error when fetching data
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        weather_bot = Weather()
        weather_info = weather_bot.get_weather_info()

        # Check for error response in the output
        self.assertEqual(weather_info, json.dumps({"error": "Weather data not available."}))

if __name__ == '__main__':
    unittest.main()
