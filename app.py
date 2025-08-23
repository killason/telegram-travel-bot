# app.py
import os
import json
import logging
import importlib
import pkgutil
from flask import Flask, request, abort
from telebot.types import Update
import telebot

from loader import bot

# логи
logging.basicConfig(level=logging.INFO)
telebot.logger.setLevel(logging.INFO)

WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/telegram/webhook")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")  # можно не задавать

# гарантированно подгрузить все модули из handlers/*
def _import_all_handlers():
    try:
        import handlers as _pkg
    except Exception:
        logging.exception("Cannot import 'handlers' package")
        return
    for m in pkgutil.iter_modules(_pkg.__path__):
        mod = f"{_pkg.__name__}.{m.name}"
        try:
            importlib.import_module(mod)
            logging.info("Handler module loaded: %s", mod)
        except Exception:
            logging.exception("Failed to load handler module: %s", mod)

_import_all_handlers()

app = Flask(__name__)

@app.get("/")
def root():
    return "service up", 200

@app.get("/health")
def health():
    return "ok", 200

@app.post(WEBHOOK_PATH)
def telegram_webhook():
    if WEBHOOK_SECRET:
        if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
            logging.warning("Forbidden: bad secret header")
            abort(403)

    raw = request.get_data(as_text=True)
    logging.info("Webhook hit: %s", raw[:400])

    # быстрый прямой ответ на /ping — оставь временно для верификации
    try:
        upd = json.loads(raw)
        msg = upd.get("message") or upd.get("edited_message")
        if msg:
            text = (msg.get("text") or "").strip()
            chat_id = msg["chat"]["id"]
            if text.startswith("/ping"):
                bot.send_message(chat_id, "pong ✅ (direct)")
                return "", 200
    except Exception:
        logging.exception("Direct reply failed")

    try:
        update = Update.de_json(raw)
        bot.process_new_updates([update])
        logging.info("Update processed ok")
    except Exception:
        logging.exception("process_new_updates failed")

    return "", 200


