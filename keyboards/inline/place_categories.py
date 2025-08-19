from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_place_categories_keyboard() -> InlineKeyboardMarkup:
    """Возвращает клавиатуру с категориями мест для inline-кнопок."""
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [
        InlineKeyboardButton(text="🍽 Еда и напитки", callback_data="category_food"),
        InlineKeyboardButton(text="🌳 Парки и природа", callback_data="category_parks"),
        InlineKeyboardButton(text="🖼 Музеи и культура", callback_data="category_museums"),
        InlineKeyboardButton(text="🏛 Достопримечательности", callback_data="category_sights"),
        InlineKeyboardButton(text="🛍 Покупки", callback_data="category_shops"),
        InlineKeyboardButton(text="🏧 Банки и банкоматы", callback_data="category_banks"),
        InlineKeyboardButton(text="🏥 Медицина", callback_data="category_medical"),
        InlineKeyboardButton(text="⭐ Избранное", callback_data="show_favorites"),
        InlineKeyboardButton(text="📜 История", callback_data="category_history"),
        InlineKeyboardButton(text="🔍 Поиск", callback_data="category_search"),
    ]

    markup.add(*buttons)
    return markup
