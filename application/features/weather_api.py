import requests
from datetime import datetime, UTC
import pytz


def get_weather():
    latitude = 52.5200
    longitude = 13.4050

    api_url = f'https://api.api-ninjas.com/v1/weather?lat={latitude}&lon={longitude}'
    api_key = 'bSxUN/7vt5nlYjC0uxBbGg==SfAh0QrK6qmqVYv6'

    response = requests.get(api_url, headers={'X-Api-Key': api_key})

    if response.status_code == requests.codes.ok:
        weather_data = response.json()

        temp = weather_data.get("temp", "N/A")
        feels_like = weather_data.get("feels_like", "N/A")
        humidity = weather_data.get("humidity", "N/A")
        wind_speed = weather_data.get("wind_speed", "N/A")

        sunrise_timestamp = weather_data.get("sunrise")
        sunset_timestamp = weather_data.get("sunset")

        if sunrise_timestamp and sunset_timestamp:
            sunrise_utc = datetime.fromtimestamp(sunrise_timestamp, UTC)
            sunset_utc = datetime.fromtimestamp(sunset_timestamp, UTC)

            berlin_tz = pytz.timezone("Europe/Berlin")
            sunrise_time = sunrise_utc.astimezone(berlin_tz).strftime('%H:%M:%S')
            sunset_time = sunset_utc.astimezone(berlin_tz).strftime('%H:%M:%S')

            sun_hours = (sunset_utc - sunrise_utc).seconds // 3600
        else:
            sunrise_time, sunset_time, sun_hours = "N/A", "N/A", "N/A"

        weather_summary = f"""   
📍 City: Berlin
🌡 Temperature: {temp}°C (Feels like: {feels_like}°C)
💧 Humidity: {humidity}%
🌬 Wind speed: {wind_speed} m/s
🌅 Sunrise: {sunrise_time}
🌇 Sunset: {sunset_time}
☀️ Sun hours: {sun_hours}h """

        return weather_summary

    else:
        print("No weather data")
        return None


