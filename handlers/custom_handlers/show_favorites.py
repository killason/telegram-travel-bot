from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot
from database.models import FavoritePlace

@bot.callback_query_handler(func=lambda call: call.data == "show_favorites")
def handle_show_favorites(call: CallbackQuery):
    user_id = call.from_user.id
    favorites = FavoritePlace.select().where(FavoritePlace.user_id == user_id)

    if not favorites.exists():
        bot.send_message(call.message.chat.id, "⭐ У тебя пока нет избранных мест.")
        return

    text = "⭐ <b>Твои избранные места:</b>"
    for fav in favorites:
        text += (
            f"\n\nДобавлено в {fav.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            f"<b>{fav.name}</b>\n"
            f"📍 {fav.address}\n"
            f"🏷 {fav.place_type.capitalize()}\n"
            f"<a href=\"{fav.link}\">📍 На карте</a>"
        )

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_categories"))

    bot.send_message(call.message.chat.id, text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=markup)
