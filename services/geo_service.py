import requests
from config_data.config import TOMTOM_API_KEY


def get_coordinates_by_city(city_name: str) -> tuple[float, float] | None:
    url = f"https://api.tomtom.com/search/2/geocode/{city_name}.json"
    params = {
        "key": TOMTOM_API_KEY,
        "limit": 1,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            position = data["results"][0]["position"]
            return position["lat"], position["lon"]
    return None