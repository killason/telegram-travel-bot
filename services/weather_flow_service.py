from services.weather_service import get_weather_by_coordinates
from services.gpt_service import get_ai_advice
from services.geo_service import get_coordinates_by_city
from services.history_service import save_city_set


def process_weather_by_location(
    user_id: int, user_name: str, lat: float, lon: float
) -> tuple[str, str]:
    """
    Получает погоду по координатам и возвращает текст с погодой и советом.
    """

    weather = get_weather_by_coordinates(lat, lon)
    if not weather:
        return ("❌ Не удалось получить погоду.", "")

    city = weather["city"]

    # Сохраняем город и погоду в истории
    weather_short = f"{weather['condition']}, {weather['temperature']}°C"
    save_city_set(user_id, city, lat, lon, weather=weather_short)

    weather_text = (
        f"📍 Погода в {city}, {weather['country']}:\n"
        f"🌡 {weather['temperature']}°C (ощущается как {weather['feels_like']}°C)\n"
        f"🌥 {weather['condition']}\n"
        f"💨 Ветер: {weather['wind']} км/ч\n"
        f"💧 Влажность: {weather['humidity']}"
    )

    advice = get_ai_advice(
        city, weather["condition"], weather["temperature"], user_name=user_name
    )

    return (weather_text, f"💡 {advice}")


def process_weather_by_city(user_id: int, user_name: str, city: str) -> tuple[str, str]:
    """
    Получает координаты по названию города.
    """

    coords = get_coordinates_by_city(city)
    if not coords:
        return ("❌ Не удалось найти город. Попробуйте снова.", "")

    lat, lon = coords

    # # Сохраняем координаты в контекст
    # set_context(user_id, lat=lat, lon=lon)

    return process_weather_by_location(user_id, user_name, *coords)
