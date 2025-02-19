import requests
from datetime import datetime, timezone
import json
import pytz  # Import pytz for timezone handling

class Weather:
    API_URL = "https://forecast.meteonomiqs.com/v3_1/forecast/{latitude}/{longitude}"
    API_KEY = "9wxowjP7pBaPpP5dx5GN5oxb4pGJm7V2hqQIFWpe"
    LAT = 52.5200  # Berlin
    LON = 13.4050

    def __init__(self):
        self.weather_data = None
        self.fetch_weather()

    def fetch_weather(self):  # Fetch weather data
        url = self.API_URL.format(latitude=self.LAT, longitude=self.LON)
        headers = {"x-api-key": self.API_KEY}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            return

        self.weather_data = response.json()

    def get_sun_hours(self):
        if not self.weather_data:
            return None, None, None

        try:
            # Get sunrise and sunset times from the response and parse them into datetime objects
            sunrise = datetime.fromisoformat(self.weather_data["sunrise"]).replace(tzinfo=timezone.utc)
            sunset = datetime.fromisoformat(self.weather_data["sunset"]).replace(tzinfo=timezone.utc)

            # Convert to Berlin time using pytz
            berlin_tz = pytz.timezone("Europe/Berlin")
            sunrise = sunrise.astimezone(berlin_tz)
            sunset = sunset.astimezone(berlin_tz)

            # Calculate sun hours
            sun_hours = (sunset - sunrise).seconds // 3600  # Convert seconds to hours
            return sunrise.strftime('%H:%M'), sunset.strftime('%H:%M'), sun_hours
        except KeyError:
            return None, None, None
        except ValueError:
            # Handle cases where datetime parsing fails
            return None, None, None

    def get_weather_info(self):
        # Return a JSON response for chatbot integration
        if not self.weather_data:
            return json.dumps({"error": "Weather data not available."})

        try:
            # Extract necessary data from the weather response
            temp_min = self.weather_data["temperature"]["min"]
            temp_max = self.weather_data["temp_max"]
            weather_desc = self.weather_data["weather_desc"]
            sunrise, sunset, sun_hours = self.get_sun_hours()

            response = {
                "city": "Berlin",
                "max_temperature": f"{temp_max}°C",
                "min_temperature": f"{temp_min}°C",
                "condition": weather_desc,
                "sun_hours": f"{sun_hours} hours" if sun_hours else "N/A",
                "sunset_time": sunset if sunset else "N/A"
            }

            return json.dumps(response, indent=4)

        except KeyError:
            return json.dumps({"error": "Error parsing weather data."})

if __name__ == "__main__":
    weather_bot = Weather()
    print(weather_bot.get_weather_info())
