from telebot import types
from telebot.types import Message
from loader import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.weather_flow_service import (
    process_weather_by_location,
    process_weather_by_city,
)
import logging


# ---------------------ОБРАБОТКА КОМАНДЫ /start---------------------------
@bot.message_handler(commands=["start"])
def bot_start(message: Message):

    logging.info(f"Пользователь {message.from_user.id} запустил бота")

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


# ---------------------ОБРАБОТКА ГЕОЛОКАЦИИ---------------------------
@bot.message_handler(content_types=["location"])
def handle_location(message: Message):

    lat, lon = message.location.latitude, message.location.longitude
    user_name = message.from_user.first_name
    weather_text, advice_text = process_weather_by_location(
        message.from_user.id, user_name, lat, lon
    )

    if advice_text:
        logging.info(
            f"Пользователь {message.from_user.id} пользователь получил погоду и совет для: {lat}, {lon}"
        )
        answer = weather_text + "\n" + advice_text
    else:
        logging.error(f"Совет не получен для {message.from_user.id} в: {lat}, {lon}")
        answer = weather_text + "\n Не удалось получить советы."

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⬇️", callback_data="back_to_categories"))
    bot.send_message(message.chat.id, answer, reply_markup=markup)


# ------------ОБРАБОТКА ТЕКСТА ГОРОДА--------------------
@bot.message_handler(func=lambda msg: msg.text and not msg.text.startswith("/"))
def handle_city(message: Message):

    city = message.text.strip()
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, f"🔍 Ищу информацию по городу: {city}")
    weather_text, advice_text = process_weather_by_city(
        message.from_user.id, user_name, city
    )

    if advice_text:
        logging.info(
            f"Пользователь {message.from_user.id} получил погоду и совет для города: {city}"
        )
        answer = weather_text + "\n" + advice_text
    else:
        answer = weather_text + "\n Не удалось получить советы."
        logging.error(f"Совет не получен для {message.from_user.id} в городе: {city}")

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⬇️", callback_data="back_to_categories"))
    bot.send_message(message.chat.id, answer, reply_markup=markup)
