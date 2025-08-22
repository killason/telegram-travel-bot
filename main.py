import os
import handlers
from utils.set_bot_commands import set_default_commands
import logging


if __name__ == "__main__":
    if os.getenv("RUN_MODE", "polling") == "polling":
        from loader import bot

        set_default_commands(bot)
        logging.info("Бот запущен...")
        bot.infinity_polling(skip_pending=True, timeout=20)
