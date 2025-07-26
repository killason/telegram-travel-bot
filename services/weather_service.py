import requests
from config_data.config import WEATHER_API_KEY


def get_weather_by_coordinates(lat: float, lon: float) -> dict | None:
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": f"{lat},{lon}",
        "lang": "ru"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        location = data["location"]
        current = data["current"]

        return {
            "city": location["name"],
            "country": location["country"],
            "temperature": current["temp_c"],
            "feels_like": current["feelslike_c"],
            "condition": current["condition"]["text"],
            "wind": current["wind_kph"],
            "humidity": current["humidity"]
        }
    return None