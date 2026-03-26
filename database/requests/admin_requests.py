from database.models import async_session, Texts, Chats
from sqlalchemy import select, or_, and_, delete, func, case, cast, Integer, String
import logging


async def add_text(thursday_text: str, sunday_text: str, every_day_text: str, thirst_day_text: str) -> None:
    """Заполнение текста для напоминания"""
    logging.info('add_or_update_text')
    async with async_session() as session:
        new_texts = Texts(
            thursday_text=thursday_text,
            sunday_text=sunday_text,
            every_day_text=every_day_text,
            thirst_day_text=thirst_day_text
        )
        session.add(new_texts)
        await session.commit()


async def update_text(type_: str, value: str) -> None:
    """Обновление текста для напоминаний"""
    logging.info('update_text')
    async with async_session() as session:
        texts = await session.scalar(select(Texts).where(Texts.id == 1))
        if type_ == 'thursday-text':
            texts.thursday_text = value
        if type_ == 'sunday-text':
            texts.sunday_text = value
        if type_ == 'every-day-text':
            texts.every_day_text = value
        if type_ == 'thirst-day-text':
            texts.thirst_day_text = value
        await session.commit()


async def check_texts() -> bool:
    """Проверка наличия текстов"""
    logging.info('check_texts')
    async with async_session() as session:
        texts = await session.scalar(select(Texts).where(Texts.id == 1))
        if texts:
            return texts.__dict__
        else:
            return False


async def add_new_group(chat_id: int, chat_name: str) -> None:
    """Добавление новой группы"""
    logging.info('add_new_group')
    async with async_session() as session:
        new_chat = Chats(
            chat_id=chat_id,
            chat_name=chat_name
        )
        session.add(new_chat)
        await session.commit()


async def delete_chat(chat_id: int) -> None:
    """Удаление группы"""
    logging.info('delete_chat')
    async with async_session() as session:
        chat = await session.scalar(select(Chats).where(Chats.chat_id == chat_id))
        if chat:
            await session.delete(chat)
            await session.commit()


async def get_chats() -> list:
    """Получение всех чатов"""
    logging.info('get_chats')
    async with async_session() as session:
        chats = await session.scalars(select(Chats))
        if chats:
            return chats.all()
        else:
            return []























