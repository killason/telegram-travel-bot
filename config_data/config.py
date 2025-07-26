import os
from dotenv import load_dotenv, find_dotenv


# Загружаем .env только если он есть
if find_dotenv():
    load_dotenv()
else:
    print("Файл .env не найден — работаем с переменными окружения Render")

BOT_TOKEN = os.getenv("BOT_TOKEN")
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
#RAPID_API_KEY = os.getenv("RAPID_API_KEY")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку")
)
