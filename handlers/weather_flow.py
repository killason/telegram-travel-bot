from telebot.types import Message
from loader import bot
from services.geo_service import get_coordinates_by_city
from services.weather_service import get_weather_by_coordinates
from services.advice_service import get_ai_advice


def handle_city_input(city_name: str) -> str:
    coords = get_coordinates_by_city(city_name)
    if not coords:
        return "😔 Не удалось найти город. Попробуй снова."

    lat, lon = coords
    weather_info = get_weather_by_coordinates(lat, lon)
    advice = get_ai_advice(weather_info, city_name)

    return f"{weather_info}\n\n🧠 {advice}"


def handle_coordinates(lat: float, lon: float) -> str:
    weather_info = get_weather_by_coordinates(lat, lon)
    advice = get_ai_advice(weather_info)

    return f"{weather_info}\n\n🧠 {advice}"


def process_city_input(message: Message):
    
    if not message.text:
        bot.send_message(message.chat.id, "❗ Пожалуйста, введите название города текстом.")
        return
    
    city_name = message.text.strip()

    if city_name == "📍 Отправить геолокацию":
        bot.send_message(message.chat.id, "📡 Ожидаю твою геолокацию...")
        return

    bot.send_message(message.chat.id, f"🔎 Ищу информацию для: {city_name}")
    result = handle_city_input(city_name)
    bot.send_message(message.chat.id, result)


def process_location_input(message: Message):
    if not message.location:
        bot.send_message(message.chat.id, "❗ Не удалось получить координаты.")
        return

    lat = message.location.latitude
    lon = message.location.longitude
    bot.send_message(message.chat.id, f"🔎 Определено местоположение. Анализирую...")

    result = handle_coordinates(lat, lon)
    bot.send_message(message.chat.id, result)
    