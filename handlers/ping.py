from loader import bot

@bot.message_handler(commands=["ping", "start", "help"])
def _ping(m):
    bot.reply_to(m, "pong ✅ (handler)")
