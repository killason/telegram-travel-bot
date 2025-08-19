from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot
from utils.user_context import set_context, get_context


def send_places_chunk(chat_id: int, user_id: int) -> None:
    """Отправляет пользователю следующую порцию мест на основе сохраненного контекста."""

    context = get_context(user_id)
    places = context.get("places", [])
    offset = context.get("offset", 0)
    lat = context.get("lat")
    lon = context.get("lon")
    place_type = context.get("place_type")
    
    # Проверка выхода за пределы
    if offset >= len(places):
        bot.send_message(chat_id, "Больше ничего не найдено 😕")
        return

    chunk = places[offset:offset + 5]

    for idx, place in enumerate(chunk):
        name = place["name"] or "Без названия"
        address = place["address"]
        place_type = place["place_type"].capitalize()
        link = place["link"]
        place_id = place["place_id"]

        text = (
            f"<b>{name}</b>\n"
            f"📍 {address}\n"
            f"🏷 {place_type}\n"
            f"<a href=\"{link}\">📍 На карте</a>"
        )

        markup = InlineKeyboardMarkup()

        # Флаг — последнее ли это в текущей тройке и последнее ли в списке вообще
        is_last_in_chunk = idx == len(chunk) - 1
        is_last_in_list = (offset + idx + 1) >= len(places)

        # "Подробнее" с меткой позиции
        suffix = "last" if is_last_in_chunk else "mid"
        if is_last_in_list:
            suffix = "final"

        markup.add(
            InlineKeyboardButton("🔎 Подробнее", callback_data=f"details_{place_id}_{suffix}")
        )

        if is_last_in_chunk:
            buttons = []
            if not is_last_in_list:
                buttons.append(InlineKeyboardButton("➡️ Далее", callback_data="more_places"))
            buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_categories"))
            markup.add(*buttons)

        bot.send_message(chat_id, text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=markup)

    # Обновляем offset
    set_context(user_id, lat=lat, lon=lon, place_type=place_type, places=places, offset=offset + 5)

