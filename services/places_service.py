import os
import time
import requests
from config_data.config import GOOGLE_API_KEY


def search_all_places(query: str, lat: float, lon: float, place_type: str, radius: int = 5000) -> list[dict]:
    """Поиск всех мест по запросу с использованием Google Places API."""

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    all_results = []
    page_token = None

    for _ in range(3):  # Максимум 3 страницы (Google ограничивает)
        if page_token:
            params = {
                "key": GOOGLE_API_KEY,
                "pagetoken": page_token,
                "language": "ru"
            }
        else:
            params = {
                "key": GOOGLE_API_KEY,
                "location": f"{lat},{lon}",
                "radius": radius,
                "type": place_type,
                "keyword": query,
                "language": "ru"
            }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("status") not in ("OK", "ZERO_RESULTS"):
                print("Ошибка запроса:", data.get("status"), "|", data.get("error_message"))
                break

            for item in data.get("results", []):
                name = item.get("name", "Без названия")
                address = item.get("vicinity", "Адрес неизвестен")
                types = item.get("types", [])
                place_type = types[0] if types else "неизвестно"
                location = item.get("geometry", {}).get("location", {})
                lat_str = location.get("lat")
                lon_str = location.get("lng")
                maps_link = f"https://www.google.com/maps/search/?api=1&query={lat_str},{lon_str}"

                all_results.append({
                    "name": name,
                    "place_type": place_type,
                    "address": address,
                    "link": maps_link,
                    "place_id": item.get("place_id")
                })

            page_token = data.get("next_page_token")
            if not page_token:
                break

            time.sleep(2)

        except Exception as e:
            print("Ошибка запроса Google Places:", e)
            break

    return all_results



def get_place_details(place_id: str) -> dict | None:
    """Получение подробной информации о месте по его ID с использованием Google Places API."""
    
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "key": GOOGLE_API_KEY,
        "place_id": place_id,
        "language": "ru",
        "fields": "name,rating,formatted_address,formatted_phone_number,website,opening_hours,photos,types,geometry"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "OK":
            print("Ошибка Google Place Details:", data.get("error_message"))
            return None

        result = data["result"]

        location = result.get("geometry", {}).get("location", {})
        lat = location.get("lat")
        lon = location.get("lng")

        maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat and lon else ""

        photo_url = ""
        if "photos" in result:
            photo_ref = result["photos"][0]["photo_reference"]
            photo_url = (
                f"https://maps.googleapis.com/maps/api/place/photo"
                f"?maxwidth=600&photo_reference={photo_ref}&key={GOOGLE_API_KEY}"
            )

        return {
            "name": result.get("name", "Без названия"),
            "address": result.get("formatted_address", "Адрес неизвестен"),
            "phone": result.get("formatted_phone_number", "Не указан"),
            "website": result.get("website", ""),
            "rating": result.get("rating", "Нет оценки"),
            "types": result.get("types", []),
            "photo_url": photo_url,
            "opening_hours": result.get("opening_hours", {}).get("weekday_text", []),
            "maps_link": maps_link
        }

    except Exception as e:
        print("Ошибка запроса Google Place Details:", e)
        return None
