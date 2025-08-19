from telebot.types import CallbackQuery
from loader import bot
from keyboards.inline.place_categories import get_place_categories_keyboard


@bot.callback_query_handler(func=lambda call: call.data == "back_to_categories")
def handle_back_to_categories(call: CallbackQuery):
    """"Обработчик для кнопки "Назад к категориям". Возвращает пользователя к клавиатуре с категориями мест."""
    
    bot.edit_message_reply_markup(
    chat_id=call.message.chat.id,
    message_id=call.message.message_id,
    reply_markup=get_place_categories_keyboard()
)

@bot.message_handler(content_types=["back_to_categories"])
def handle_back_to_categories(call: CallbackQuery):
    """"Обработчик для кнопки "Назад к категориям". Возвращает пользователя к клавиатуре с категориями мест."""
    
    bot.edit_message_reply_markup(
    chat_id=call.message.chat.id,
    message_id=call.message.message_id,
    reply_markup=get_place_categories_keyboard()
)
