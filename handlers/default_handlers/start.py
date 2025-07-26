from telebot import types
from telebot.types import Message
from loader import bot
from handlers.weather_flow import process_city_input, process_location_input


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

        # Регистрируем следующий шаг, если пользователь введёт город вручную
    bot.register_next_step_handler(message, process_city_input)

    # Отдельный хендлер на геолокацию
@bot.message_handler(content_types=["location"])
def handle_geo(message: Message):
    process_location_input(message)

@bot.message_handler(content_types=["text"])
def handle_text_city(message: Message):
    process_city_input(message)