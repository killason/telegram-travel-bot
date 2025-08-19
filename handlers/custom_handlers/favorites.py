from telebot.types import CallbackQuery
from loader import bot
from database.models import FavoritePlace
from utils.user_context import get_context
from services.history_service import save_add_favorite

@bot.callback_query_handler(func=lambda call: call.data.startswith("fav_"))
def handle_add_favorite(call: CallbackQuery):
    user_id = call.from_user.id
    place_id = call.data.split("fav_")[1]
    context = get_context(user_id)

    # Поиск места в контексте
    places = context.get("places", [])
    place = next((p for p in places if p["place_id"] == place_id), None)

    if not place:
        bot.answer_callback_query(call.id, "❌ Место не найдено в контексте.")
        return

    # Сохраняем в БД
    FavoritePlace.create(
        user_id=user_id,
        place_id=place_id,
        name=place["name"],
        address=place["address"],
        place_type=place["place_type"],
        link=place["link"]
    )

    # Сохраняем в истории
    save_add_favorite(
    user_id=user_id,
    place_type=place.get("place_type") or place.get("category") or "",
    name=place["name"],
    address=place["address"],
    link=place["link"]
)

    bot.answer_callback_query(call.id, "✅ Добавлено в избранное!")
