from flask import Flask
import requests

app = Flask(__name__)

METEONOMIQS_API_KEY = "9wxowjP7pBaPpP5dx5GN5oxb4pGJm7V2hqQIFWpe"
METEONOMIQS_URL = "https://forecast.meteonomiqs.com/v3_1/forecast/{latitude}/{longitude}"

class Weather:
    def __init__(self, lat=52.5200, lon=13.4050):
        self.lat = lat
        self.lon = lon
        self.api_url = METEONOMIQS_URL.format(latitude=self.lat, longitude=self.lo)
        self.headers = {"x-api-key": METEONOMIQS_API_KEY}


    def fetch_weather(self):
        response = requests.get(self.api_url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_weather_summary(self):
        data = self.fetch_weather()
        print(data)
        if data:
            today = data["daily"]
            return (f"Berlin♥️ Weather🌤:\n "
                    f"🌡Max {today['temperature']['max']}°C - Min {today['temperature']['min']}°C\n",
                    f"☁ Sky: {today['summary']}\n"
                    f"🌞 Sun Hours: {today['sun_hours']} hrs\n"
                    f"🌇 Sunset: {today['sunset']}")
        return "Internal Error try later again please"