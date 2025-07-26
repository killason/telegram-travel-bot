import os
import requests
from dotenv import load_dotenv

# Подгружаем .env только если он реально существует
if os.path.exists(".env"):
    load_dotenv()

FSQ_API_KEY = os.getenv("FOURSQUARE_API_KEY")
print(FSQ_API_KEY)

def get_places_by_category(lat, lon, category_id, limit=5):
    url = "https://api.foursquare.com/v3/places/search"
    headers = {
        "Accept": "application/json",
        "Authorization": FSQ_API_KEY
    }
    params = {
        "ll": f"{lat},{lon}",
        "categories": category_id,
        "limit": limit,
        "sort": "RELEVANCE"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        print("Status:", response.status_code)
        print("Raw response:", response.text)
        data = response.json()
        return [
            {
                "name": place["name"],
                "address": place.get("location", {}).get("address", "Адрес не указан")
            }
            for place in data.get("results", [])
        ]
    except Exception as e:
        print("Ошибка Foursquare:", e)
        return []
        