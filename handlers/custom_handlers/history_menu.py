from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot
from services.history_service import get_months_with_data, get_history_by_month, delete_history_by_month, RU_MONTHS

@bot.callback_query_handler(func=lambda call: call.data == "category_history")
def handle_history_root(call: CallbackQuery):
    user_id = call.from_user.id
    months = get_months_with_data(user_id)
    if not months:
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_categories"))
        bot.send_message(call.message.chat.id, "Пока нет истории.", reply_markup=kb)
        return

    kb = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for year, month, cnt in months:
        label = f"{RU_MONTHS[month]} {year} ({cnt})"
        buttons.append(InlineKeyboardButton(label, callback_data=f"hist_month:{year}-{month:02d}"))
    kb.add(*buttons)
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_categories"))

    bot.send_message(call.message.chat.id, "Выбери месяц:", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("hist_month:"))
def handle_history_month(call: CallbackQuery):
    _, ym = call.data.split(":")
    year_s, month_s = ym.split("-")
    year, month = int(year_s), int(month_s)

    entries = get_history_by_month(call.from_user.id, year, month)

    if not entries:
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="history_root"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Записей нет.",
            reply_markup=kb
        )
        return

    lines = [f"🗓 <b>{RU_MONTHS[month]} {year}</b>\n"]
    for e in entries:
        when = e.created_at.strftime("%d.%m %H:%M")
        if e.action == "city_set":
            lines.append(f"• {when} — Город: <b>{e.city}</b>  ({e.weather or '-'})")
        elif e.action == "view_place":
            row = f"• {when} — Просмотр: <b>{e.name}</b> — {e.address or ''}"
            if e.link:
                row += f'\n   <a href="{e.link}">📍 На карте</a>'
            lines.append(row)
        elif e.action == "add_favorite":
            row = f"• {when} — ★ В избранное: <b>{e.name}</b> — {e.address or ''}"
            if e.link:
                row += f'\n   <a href="{e.link}">📍 На карте</a>'
            lines.append(row)
        else:
            lines.append(f"• {when} — {e.action}")

    text = "\n".join(lines)

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🗑 Удалить этот месяц", callback_data=f"hist_del:{year}-{month:02d}"),
        InlineKeyboardButton("⬅️ Назад", callback_data="category_history")
    )
    # редактируем текущее сообщение (без спама новыми)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        parse_mode="HTML",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("hist_del:"))
def handle_history_delete_month(call: CallbackQuery):
    _, ym = call.data.split(":")
    year_s, month_s = ym.split("-")
    year, month = int(year_s), int(month_s)

    delete_history_by_month(call.from_user.id, year, month)

    # всплывающее уведомление (toast)
    bot.answer_callback_query(call.id, "🧹 История за месяц удалена", show_alert=False)

    # удаляем сообщение со списком истории
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    bot.delete_message(chat_id, msg_id)

    # обновим меню месяцев
    months = get_months_with_data(call.from_user.id)
    if months:
        kb = InlineKeyboardMarkup(row_width=2)
        buttons = []
        for y, m, cnt in months:
            label = f"{RU_MONTHS[m]} {y} ({cnt})"
            buttons.append(InlineKeyboardButton(label, callback_data=f"hist_month:{y}-{m:02d}"))
        kb.add(*buttons)
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_categories"))
        bot.send_message(chat_id, "Выбери месяц:", reply_markup=kb)
    else:
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_categories"))
        bot.send_message(chat_id, "История пуста.", reply_markup=kb)

