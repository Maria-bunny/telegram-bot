from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

import logging
from config_data.config_data import Config, load_config
from keyboard import admin_keyboard
from database.requests import admin_requests
from filters.admin_filter import IsSuperAdmin


config: Config = load_config()
router = Router()
router.message.filter(IsSuperAdmin())


@router.message(F.text == 'Список чатов 💬')
async def chats(message: types.Message, state: FSMContext):
    """Выводить список чатов"""
    logging.info('chats')
    chats_data = await admin_requests.get_chats()
    if chats_data:
        text = 'Список ваших чатов 👇\n\n'
        for chat in chats_data:
            chat = chat.__dict__
            text += (f'🔸Название: {chat["chat_name"]}\n'
                     f'🔸Chat_id: {chat["chat_id"]}\n\n')
        await message.answer(text=text)
    else:
        await message.answer('Вы еще не добавили ни одного чата ❌')