from telebot import types
from telebot.types import Message
from loader import bot


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
        "Можешь отправить геолокацию или ввести город вручную 👇"
    )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    geo_button = types.KeyboardButton("📍 Отправить геолокацию", request_location=True)
    manual_button = types.KeyboardButton("✏️ Ввести город вручную")
    markup.add(geo_button, manual_button)

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
