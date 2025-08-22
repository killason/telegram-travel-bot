from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_place_categories_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с категориями мест для inline-кнопок.
    """
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [
        InlineKeyboardButton(
            text="🍽 Еда и напитки", callback_data="category_restaurant"
        ),
        InlineKeyboardButton(text="🏨 Отели и жилье", callback_data="category_lodging"),
        InlineKeyboardButton(text="🌳 Парки и природа", callback_data="category_park"),
        InlineKeyboardButton(
            text="🖼 Музеи и культура", callback_data="category_museum"
        ),
        InlineKeyboardButton(
            text="🏛 Достопримечательности", callback_data="category_tourist_attraction"
        ),
        InlineKeyboardButton(text="🛍 Шоппинг", callback_data="category_shopping_mall"),
        InlineKeyboardButton(text="🏧 Банкоматы", callback_data="category_atm"),
        InlineKeyboardButton(
            text="🏥 Аптеки и больницы", callback_data="category_pharmacy"
        ),
        InlineKeyboardButton(text="⭐ Избранное", callback_data="show_favorites"),
        InlineKeyboardButton(text="📜 История", callback_data="show_history"),
        InlineKeyboardButton(text="🔍 Поиск", callback_data="search"),
    ]

    markup.add(*buttons)
    return markup
