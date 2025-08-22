from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | — %(message)s"
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    set_default_commands(bot)
    logger.info("Бот запущен...")
    bot.infinity_polling()
