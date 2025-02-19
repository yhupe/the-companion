import requests
from datetime import datetime, timezone
import json
import pytz  # Import pytz for timezone handling

class Weather:
    latitude = 52.5200  # Berlin
    longitude = 13.4050

    api_url = f'https://api.api-ninjas.com/v1/weather?lat={latitude}&lon={longitude}'
    response = requests.get(api_url, headers={'X-Api-Key': 'bSxUN/7vt5nlYjC0uxBbGg==SfAh0QrK6qmqVYv6'})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.__dict__)

    def __init__(self):
        self.weather_data = None
        self.fetch_weather()

    def fetch_weather(self):
        latitude = 52.5200  # Berlin
        longitude = 13.4050
                             # Fetch weather data
        api_url =  f'https://api.api-ninjas.com/v1/weather?lat={latitude}&lon={longitude}'
        headers = {'X-Api-Key': 'bSxUN/7vt5nlYjC0uxBbGg==SfAh0QrK6qmqVYv6'}

        try:
            response = requests.get(api_url, headers=headers)
            print("Raw response:", response.text)  # Print raw response for debugging

            if response.status_code != 200:
                print("Error:", response.status_code, response.text)
                return

            self.weather_data = response.json()

        except requests.RequestException as e:
            print("Request failed:", e)

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
            # Handle cases where datetime parsing fails!!!!!!!
            return None, None, None

    def get_weather_info(self):
        # Return a JSON response for chatbot integration
        if not self.weather_data:
            return json.dumps({"error": "Weather data not available."})

        try:
            # Extract necessary data from the weather response
            temp_min = self.weather_data["min_temp"]
            temp_max = self.weather_data["max_temp"]
            temperature = self.weather_data["temp"]
            sunrise, sunset, sun_hours = self.get_sun_hours()

            response = f"""
            Temperature:{temperature}
            Mini temperature: {temp_min}
            Max temperature: {temp_max}
            Sunrise: {sunrise}
            Sunset:{sunset}
            Sun hours: {sun_hours}
            """


            return response

        except KeyError:
            return None

if __name__ == "__main__":
    weather_bot = Weather()
    print(weather_bot.get_weather_info())
