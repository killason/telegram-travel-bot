# from telebot import TeleBot
# from telebot.storage import StateMemoryStorage
# from config_data import config

# storage = StateMemoryStorage()
# bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)

import os
from telebot import TeleBot
from telebot.storage import StateMemoryStorage

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    # локально .env подхватится вашим config.py, но на Render читаем ENV
    try:
        from config_data import config as cfg  # fallback для локалки
        BOT_TOKEN = getattr(cfg, "BOT_TOKEN", None)
    except Exception:
        BOT_TOKEN = None

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set (ENV or config_data.config)")

storage = StateMemoryStorage()
bot = TeleBot(
    token=BOT_TOKEN,
    state_storage=storage,
    parse_mode="HTML",
    threaded=False,               # важно для вебхука
    disable_web_page_preview=True
)