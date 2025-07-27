from telebot import types
from telebot.types import Message
from loader import bot
from services.geo_service import get_coordinates_by_city
from services.weather_service import get_weather_by_coordinates
from services.advice_service import get_ai_advice


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    welcome_text = (
        f"👋 Привет, {message.from_user.full_name}! Я — твой Путешественник-Досугатор 🗺️\n\n"
        "Я помогу тебе:\n"
        "• Узнать актуальную погоду 🌤️\n"
        "• Найти, чем заняться в городе 🏙️\n"
        "• Получить идеи для прогулок, кафе, музеев и не только 🎭\n"
        "• Составить план досуга по настроению 🧘‍♂️\n\n"
        "📍 Давай начнём с выбора твоего местоположения:\n"
        "• 🔘 Нажми кнопку ниже, чтобы отправить геолокацию\n"
        "• 📝 Или просто напиши название города вручную"
    )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    geo_button = types.KeyboardButton("📍 Отправить геолокацию", request_location=True)
    markup.add(geo_button)

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


# ⛳ ОБРАБОТКА ГЕОЛОКАЦИИ
@bot.message_handler(content_types=["location"])
def handle_location(message: Message):
    loc = message.location
    if not loc:
        bot.send_message(message.chat.id, "❗ Геолокация не получена.")
        return

    lat, lon = loc.latitude, loc.longitude

    weather = get_weather_by_coordinates(lat, lon)
    if not weather:
        bot.send_message(message.chat.id, "❌ Не удалось получить погоду.")
        return

    # Формируем текст погоды
    weather_text = (
        f"📍 Погода в {weather['city']}, {weather['country']}:\n"
        f"🌡 {weather['temperature']}°C (ощущается как {weather['feels_like']}°C)\n"
        f"🌥 {weather['condition']}\n"
        f"💨 Ветер: {weather['wind']} км/ч\n"
        f"💧 Влажность: {weather['humidity']}%"
    )
    bot.send_message(message.chat.id, weather_text)

    # Запрашиваем совет у ИИ
    advice = get_ai_advice(weather['city'], weather["condition"], weather['temperature'])
    bot.send_message(message.chat.id, f"💡 Совет:\n{advice}")


# ⛳ ОБРАБОТКА ТЕКСТА ГОРОДА
@bot.message_handler(func=lambda msg: msg.text and not msg.text.startswith('/'))
def handle_city(message: Message):
    city = message.text.strip()
    bot.send_message(message.chat.id, f"🔍 Ищу информацию по городу: {city}")

    coords = get_coordinates_by_city(city)
    if not coords:
        bot.send_message(message.chat.id, "❌ Не удалось найти город. Попробуйте снова.")
        return

    lat, lon = coords
    weather = get_weather_by_coordinates(lat, lon)
    if not weather:
        bot.send_message(message.chat.id, "❌ Не удалось получить погоду.")
        return

    weather_text = (
        f"📍 Погода в {weather['city']}, {weather['country']}:\n"
        f"🌡 {weather['temperature']}°C (ощущается как {weather['feels_like']}°C)\n"
        f"🌥 {weather['condition']}\n"
        f"💨 Ветер: {weather['wind']} км/ч\n"
        f"💧 Влажность: {weather['humidity']}%"
    )
    bot.send_message(message.chat.id, weather_text)

    advice = get_ai_advice(weather["condition"])
    bot.send_message(message.chat.id, f"💡 Совет:\n{advice}")
