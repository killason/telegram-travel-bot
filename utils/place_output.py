from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot
from utils.user_context import set_context, get_context
from services.history_service import get_cached_places


def send_places_chunk(chat_id: int, user_id: int, place_type: str) -> None:
    """
    Отправляет пользователю следующую порцию мест на основе сохраненного контекста.
    """

    places = get_cached_places(user_id, place_type=place_type) or []
    if not places:
        bot.send_message(chat_id, "Пока пусто. Выбери категорию снова.")
        return

    ctx = get_context(user_id) or {}
    offset = int(ctx.get("offset", 0))

    # Проверка выхода за пределы
    if offset >= len(places):
        bot.send_message(chat_id, "Больше ничего не найдено 😕")
        return

    chunk = places[offset : offset + 3]

    for idx, place in enumerate(chunk):
        name = place["name"] or "Без названия"
        address = place["address"]
        place_type_label = place["place_type"].capitalize()
        link = place["link"]
        place_id = place["place_id"]

        text = (
            f"<b>{name}</b>\n"
            f"📍 {address}\n"
            f"🏷 {place_type_label}\n"
            f'<a href="{link}">📍 На карте</a>'
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
            InlineKeyboardButton(
                "🔎 Подробнее", callback_data=f"details_{place_id}_{suffix}"
            )
        )

        if is_last_in_chunk:
            buttons = []
            if not is_last_in_list:
                buttons.append(
                    InlineKeyboardButton(
                        "➡️ Далее", callback_data=f"more_places:{place_type}"
                    )
                )
            buttons.append(
                InlineKeyboardButton("⬅️ Назад", callback_data="back_to_categories")
            )
            markup.add(*buttons)

        bot.send_message(
            chat_id,
            text,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=markup,
        )

    # Обновляем offset
    set_context(user_id, offset=offset + 3)
