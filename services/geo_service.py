import requests
from config_data.config import GOOGLE_API_KEY


def get_coordinates_by_city(city_name: str) -> tuple[float, float] | None:
    """Возвращает координаты города по его названию."""
    
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": city_name,
        "key": GOOGLE_API_KEY,
        "language": "ru"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None
