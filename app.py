import os
from flask import Flask, request, abort
from telebot.types import Update
from loader import bot
import handlers

WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/telegram/webhook")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")  # опционально

app = Flask(__name__)


@app.get("/health")
def health():
    return "ok", 200


@app.post(WEBHOOK_PATH)
def telegram_webhook():
    if WEBHOOK_SECRET:
        if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
            abort(403)
    update = Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return "", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
