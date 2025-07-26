from services.geo_service import get_coordinates_by_city
from services.weather_service import get_weather
from services.advice_service import get_weather_advice
from telebot import types
from telebot.types import Message
from loader import bot

def handle_city_input(city_name: str) -> str:
    coords = get_coordinates_by_city(city_name)
    if not coords:
        return "⚠️ Не удалось найти координаты для указанного города."

    lat, lon = coords
    weather_info = get_weather(lat, lon)
    if not weather_info:
        return "⚠️ Не удалось получить данные о погоде."

    condition = weather_info["condition"]
    temp = weather_info["temp_c"]
    summary = weather_info["text"]

    advice = get_weather_advice(city_name, condition, temp)

    return (
        f"📍 Город: {city_name}\n"
        f"{summary}\n\n"
        f"💡 Совет:\n{advice}"
    )

def process_city_input(message: Message):
    city_name = message.text.strip()

    # Проверка: не выбрал ли он геолокацию вместо текста
    if city_name == "📍 Отправить геолокацию":
        bot.send_message(message.chat.id, "📡 Ожидаю твою геолокацию...")
        return

    bot.send_message(message.chat.id, f"🔎 Ищу погоду и идеи для города: {city_name}")
    
    # Основной обработчик
    try:
        result = handle_city_input(city_name)
        bot.send_message(message.chat.id, result)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка обработки: {e}")