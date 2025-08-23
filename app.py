# app.py
import os
import logging
from flask import Flask, request, abort
from telebot.types import Update
from loader import bot

# Логи Flask + TeleBot
logging.basicConfig(level=logging.INFO)
telebot_logger = logging.getLogger("telebot")
telebot_logger.setLevel(logging.INFO)

WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/telegram/webhook")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")  # можно не задавать

# ВАЖНО: импортируем хэндлеры, чтобы они зарегистрировались декораторами
try:
    import handlers  # noqa: F401
    logging.info("Handlers imported successfully")
except Exception:
    logging.exception("Handlers import failed")

app = Flask(__name__)

@app.get("/")
def root():
    return "service up", 200

@app.get("/health")
def health():
    return "ok", 200

@app.post(WEBHOOK_PATH)
def telegram_webhook():
    # Проверка секрета (если задан)
    if WEBHOOK_SECRET:
        hdr = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if hdr != WEBHOOK_SECRET:
            logging.warning("Forbidden: bad secret header")
            abort(403)

    raw = request.get_data(as_text=True)  # str
    logging.info("Webhook hit: %s", raw[:400])

    try:
        update = Update.de_json(raw)
        bot.process_new_updates([update])
    except Exception:
        logging.exception("process_new_updates failed")

    return "", 200

