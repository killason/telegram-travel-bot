import requests
from config_data.config import WEATHER_API_KEY


def get_weather_by_coordinates(lat: float, lon: float) -> str:
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

        city = location["name"]
        country = location["country"]
        temp_c = current["temp_c"]
        condition = current["condition"]["text"]
        feelslike_c = current["feelslike_c"]
        wind_kph = current["wind_kph"]
        humidity = current["humidity"]

        return (
            f"📍 Погода в {city}, {country}:\n"
            f"🌡 Температура: {temp_c}°C (ощущается как {feelslike_c}°C)\n"
            f"🌥 Условия: {condition}\n"
            f"💨 Ветер: {wind_kph} км/ч\n"
            f"💧 Влажность: {humidity}%"
        )
    else:
        return "❌ Не удалось получить данные о погоде."
    