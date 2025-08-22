from telebot import TeleBot
from telebot.types import BotCommand


def set_default_commands(bot: TeleBot):
    """ "
    Выставляет команды по умолчанию для бота.
    """

    bot.set_my_commands(
        [
            BotCommand("start", "Запустить бота"),
            BotCommand("help", "Вывести справку по командам"),
        ]
    )
