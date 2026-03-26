from aiogram import types


async def main_buttons():
    markup = types.ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True)
    btn_1 = types.KeyboardButton(text='Изменить текст 📄')
    btn_2 = types.KeyboardButton(text='Список чатов 💬')
    markup.keyboard.append([btn_1])
    markup.keyboard.append([btn_2])
    return markup


async def select_text_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Четверг', callback_data='edit-text_thursday-text')
    btn_2 = types.InlineKeyboardButton(text='Воскресенье', callback_data='edit-text_sunday-text')
    btn_3 = types.InlineKeyboardButton(text='Каждый день', callback_data='edit-text_every-day-text')
    btn_4 = types.InlineKeyboardButton(text='Первый день месяца', callback_data='edit-text_thirst-day-text')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_4])
    return markup


async def back_buttons(callback: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn = types.InlineKeyboardButton(text='Назад ◀️', callback_data=callback)
    markup.inline_keyboard.append([btn])
    return markup
