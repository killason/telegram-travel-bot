import requests
from config_data.config import WEATHER_API_KEY

def get_weather(lat: float, lon: float) -> str:
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": f"{lat},{lon}",
        "lang": "ru"  # Можно 'en', если хочешь на английском
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        location = data["location"]["name"]
        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        feelslike = data["current"]["feelslike_c"]

        return f"🌍 {location}\n🌡 Температура: {temp_c}°C (ощущается как {feelslike}°C)\n🌤 Состояние: {condition}"
    else:
        return "Не удалось получить данные о погоде."