from telebot.types import CallbackQuery
from loader import bot
from utils.user_context import get_context
from utils.place_output import send_places_chunk

@bot.callback_query_handler(func=lambda call: call.data == "more_places")
def handle_more_places(call: CallbackQuery):
    """"Обработчик для кнопки 'Ещё места'."""
    user_id = call.from_user.id
    context = get_context(user_id)

    if not context or "places" not in context:
        bot.send_message(call.message.chat.id, "❗ Нечего отображать. Сначала выбери категорию.")
        return

    send_places_chunk(chat_id=call.message.chat.id, user_id=user_id)
