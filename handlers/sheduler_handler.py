from aiogram import Bot, Router, F, types
from datetime import datetime

import logging
from config_data.config_data import Config, load_config
from keyboard import admin_keyboard
from database.requests import admin_requests


config: Config = load_config()
router = Router()

admin_ids = str(config.tg_bot.admin_ids).split(',')


async def thursday_notify(bot: Bot):
    """Отправление напоминания в четверг"""
    logging.info('thursday_notify')
    day_now = datetime.now().weekday()
    if day_now == 3:
        chats_data = await admin_requests.get_chats()
        texts = await admin_requests.check_texts()
        for chat in chats_data:
            chat = chat.__dict__
            try:
                await bot.send_message(chat_id=chat['chat_id'], text=texts['thursday_text'])
            except Exception as e:
                logging.info(f'Не удалось отправить сообщение: {e}')
                pass


async def sunday_notify(bot: Bot):
    """Отпрвлка напоминания в вс"""
    logging.info('sunday_notify')
    day_now = datetime.now().weekday()
    if day_now == 6:
        chats_data = await admin_requests.get_chats()
        texts = await admin_requests.check_texts()
        for chat in chats_data:
            chat = chat.__dict__
            try:
                await bot.send_message(chat_id=chat['chat_id'], text=texts['sunday_text'])
            except Exception as e:
                logging.info(f'Не удалось отправить сообщение: {e}')
                pass


async def every_day_notify(bot: Bot):
    """Напоминание каждый день в 22:30"""
    logging.info('every_day_notify')
    chats_data = await admin_requests.get_chats()
    texts = await admin_requests.check_texts()
    for chat in chats_data:
        chat = chat.__dict__
        try:
            await bot.send_message(chat_id=chat['chat_id'], text=texts['every_day_text'])
        except Exception as e:
            logging.info(f'Не удалось отправить сообщение: {e}')
            pass


async def thirst_day_notify(bot: Bot):
    """Напоминение каждое 1 число"""
    logging.info('thirst_day_notify')
    day = datetime.now().day
    if day == 1:
        chats_data = await admin_requests.get_chats()
        texts = await admin_requests.check_texts()
        for chat in chats_data:
            chat = chat.__dict__
            try:
                await bot.send_message(chat_id=chat['chat_id'], text=texts['thirst_day_text'])
            except Exception as e:
                logging.info(f'Не удалось отправить сообщение: {e}')
                pass