from telebot.types import CallbackQuery
from loader import bot
from services.history_service import get_cached_places
from utils.place_output import send_places_chunk


# ---------------------ОБРАБОТКА КНОПКИ "ДАЛЕЕ"---------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith("more_places"))
def handle_more_places(call: CallbackQuery):
    """ "Обработчик для кнопки 'Ещё места'."""
    user_id = call.from_user.id

    # Разбираем категорию из callback-data
    try:
        # payload формата: more_places:<place_type>
        _, place_type = call.data.split(":", 1)
    except ValueError:
        bot.send_message(call.message.chat.id, "❗ Сначала выбери категорию.")
        return

    # Проверяем кэш по этой категории (чтобы не листать пустое)
    places = get_cached_places(user_id, place_type=place_type) or []
    if not places:
        bot.send_message(call.message.chat.id, "❗ Пусто. Выбери категорию снова.", callback_data="back_to_categories")
        return

    send_places_chunk(
        chat_id=call.message.chat.id, user_id=user_id, place_type=place_type
    )
