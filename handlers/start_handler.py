from aiogram import Bot, Router, F, types
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter, Command
from aiogram.types import ChatMemberUpdated, ChatMemberAdministrator
from aiogram.enums import ChatMemberStatus

import logging
from config_data.config_data import Config, load_config
from keyboard import admin_keyboard
from database.requests import admin_requests


config: Config = load_config()
router = Router()

admin_ids = str(config.tg_bot.admin_ids).split(',')


@router.message(Command('start'))
async def start(message: types.Message):
    """Старт"""
    logging.info('start')
    user_id = str(message.from_user.id)
    if user_id in admin_ids:
        markup = await admin_keyboard.main_buttons()
        await message.answer('Вы администратор, выберите действие 👇', reply_markup=markup)
    else:
        await message.answer('Ботом может пользоваться только администратор ❌')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def bots_group(event: ChatMemberUpdated, bot: Bot):
    """
    Добавление и удаление бота в группу
    :param event:
    :param bot:
    :return:
    """
    logging.info('bots_group')
    if str(event.from_user.id) in admin_ids:
        if event.new_chat_member.user.id == bot.id:
            if event.new_chat_member.status == ChatMemberStatus.ADMINISTRATOR:
                chat_id = event.chat.id
                chat_name = event.chat.title
                await admin_requests.add_new_group(chat_id, chat_name)
                for id_ in admin_ids:
                    try:
                        markup = await admin_keyboard.main_buttons()
                        await bot.send_message(chat_id=int(id_), text=f'✅ Боту успешно выданы права администратора в группe: "{event.chat.title}"', reply_markup=markup)
                    except:
                        pass
            else:
                for id_ in admin_ids:
                    try:
                        await bot.send_message(chat_id=int(id_), text=f'📍 Бот добавлен в канал: "{event.chat.title}"\n\n'
                                                                  f'Сделайте вашего бота админом в канале')
                    except:
                        pass
    else:
        await bot.send_message(chat_id=int(event.chat.id), text='Добавлять нашего бота в другие ресурсы запрещено')
        await bot.leave_chat(chat_id=event.chat.id)
        await bot.send_message(chat_id=1067420041 ,text=f'Кто-то хотел добавить бота в чат: \n'
                                                        f'{event.chat.title}\n'
                                                        f'@{event.from_user.username}')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION))
async def leave_group(event: ChatMemberUpdated, bot: Bot):
    """
    Удавление бота из группы
    :param event:
    :param bot:
    :return:
    """
    logging.info('leave_group')
    if event.old_chat_member.user.id == bot.id:
        chat_id = event.chat.id
        await admin_requests.delete_chat(chat_id)
        for id_ in admin_ids:
            try:
                await bot.send_message(chat_id=int(id_), text=f'❌ Бот исключен из канала: "{event.chat.title}"\n\n'
                                                              f'username: {event.from_user.username}\n'
                                                              f'chat_id: {event.chat.id}')
            except:
                pass


@router.my_chat_member()
async def get_admin_rights(event: ChatMemberUpdated, bot: Bot):
    """
    Выдача боту прав админа
    :param event:
    :param bot:
    :return:
    """
    logging.info('get_admin_rights')
    if event.old_chat_member.user.id == bot.id:
        if event.new_chat_member.status == ChatMemberStatus.ADMINISTRATOR:
            chat_id = event.chat.id
            chat_name = event.chat.title
            await admin_requests.add_new_group(chat_id, chat_name)
            for id_ in admin_ids:
                try:
                    await bot.send_message(chat_id=int(id_), text=f'✅ Боту успешно выданы права администратора в группe: "{event.chat.title}"')
                except:
                    pass
        else:
            chat_id = event.chat.id
            await admin_requests.delete_chat(chat_id)
            for id_ in admin_ids:
                try:
                    await bot.send_message(chat_id=int(id_), text=f'❌ Бот был ограничен в правах в канале: "{event.chat.title}"\n\n')
                except:
                    pass