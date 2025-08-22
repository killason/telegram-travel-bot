from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


# ---------------------ОБРАБОТКА КОМАНДЫ /help---------------------------
@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    help_text = (
        "ℹ️ Помощь — Путешественник-Досугатор\n\n"
        "Я помогу тебе:\n"
        "• Узнать актуальную погоду 🌤️\n"
        "• Получить совет по досугу от AI 🤖\n"
        "• Найти кафе, рестораны, музеи и другие места 🏙️\n"
        "• Сохранять историю и любимые места ⭐\n\n"
        "🗺️ Как пользоваться:\n"
        "1. Отправь мне название города или поделись геолокацией 📍\n"
        "2. Я покажу погоду и предложу идеи для отдыха\n"
        "3. Можно листать места кнопками «Далее» / «Назад» и открывать подробности 🔎\n"
        "4. Любимые места можно добавить в избранное ⭐\n\n"
        "❓Если что-то пошло не так — просто напиши заново город или нажми /start\n\n"
    )
    com = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    text = help_text + "\n".join(com)
    bot.reply_to(message, text)
