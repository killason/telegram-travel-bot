from loader import bot
from telebot.types import CallbackQuery
from utils.user_context import set_context
from services.places_service import get_place_details
from utils.place_output import send_places_chunk
from services.places_service import search_all_places
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto
from services.history_service import (
    save_view_place,
    get_cached_places,
    set_cached_places,
    get_current_coords,
)
import logging


# ---------------------ОБРАБОТКА ВЫБОРА КАТЕГОРИИ МЕСТ---------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith("category_"))
def handle_places(call: CallbackQuery):
    """ "Обработчик для кнопки "Еда" в меню категорий мест."""

    logging.info(f"Пользователь {call.from_user.id} выбранная категория: {call.data}")
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    place_type = call.data.split("category_", 1)[1]

    coords = get_current_coords(user_id)
    if not coords:
        bot.send_message(chat_id, "⚠️ Сначала отправь город или геолокацию.")
        return
    _, lat, lon = coords
    logging.info(
        f"Пользователь {user_id} координаты: lat={lat}, lon={lon}, place_type={place_type}"
    )

    # Проверяем кэш
    places = get_cached_places(user_id, place_type=place_type)
    if places is None:
        logging.info(
            f"В кэше нет мест для user {user_id}, тип {place_type}. Ищем заново."
        )
        places = search_all_places(lat=lat, lon=lon, place_type=place_type)
        if places:
            set_cached_places(user_id, places, place_type=place_type)
            logging.info(
                f"Найдено {len(places)} мест для user {user_id}, тип {place_type}. Сохраняем в кэш."
            )

    if not places:
        bot.send_message(chat_id, "Ничего не найдено 😕")
        return

    # Сохраняем offset = 0
    set_context(user_id, offset=0)

    # Выводим первую порцию
    send_places_chunk(
        chat_id=call.message.chat.id, user_id=user_id, place_type=place_type
    )


# ---------------------ОБРАБОТКА КНОПКИ "ПОДРОБНЕЕ"---------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith("details_"))
def handle_place_details(call: CallbackQuery):
    raw = call.data.split("details_")[1]
    try:
        place_id, suffix = raw.rsplit("_", 1)
    except ValueError:
        place_id = raw
        suffix = "mid"

    details = get_place_details(place_id)
    if not details:
        bot.answer_callback_query(call.id, "❌ Не удалось получить данные.")
        return

    # Сохраняем просмотр места в истории
    save_view_place(
        user_id=call.from_user.id,
        place_type=", ".join(details["types"]) if details.get("types") else None,
        name=details["name"],
        address=details["address"],
        link=details.get("maps_link") or "",
    )

    text = f"📍 <b>{details['name']}</b>\n"
    text += f"{details['address']}\n"
    text += f"⭐ Рейтинг: {details['rating']}\n"
    if details["phone"]:
        text += f"📞 {details['phone']}\n"
    if details["website"]:
        text += f"🌐 <a href=\"{details['website']}\">Сайт</a>\n"
    if details["opening_hours"]:
        text += "\n🕒 Часы работы:\n" + "\n".join(details["opening_hours"])
    text += f"\n\n<a href=\"{details['maps_link']}\">📍 Открыть на карте</a>\n\n"

    if not details["photo_url"]:
        text = "📷 Фото нет\n\n" + text

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("⭐ Добавить в избранное", callback_data=f"fav_{place_id}")
    )

    if suffix == "last":
        markup.add(
            InlineKeyboardButton("➡️ Далее", callback_data="more_places"),
            InlineKeyboardButton("⬅️ Назад", callback_data="back_to_categories"),
        )
    elif suffix == "final":
        markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_categories"))

    # Редактируем текущее сообщение
    if details["photo_url"]:
        bot.edit_message_media(
            media=InputMediaPhoto(
                media=details["photo_url"], caption=text, parse_mode="HTML"
            ),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup,
        )
    else:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=markup,
        )
