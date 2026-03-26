from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import logging
from config_data.config_data import Config, load_config
from keyboard import admin_keyboard
from database.requests import admin_requests
from filters.admin_filter import IsSuperAdmin


config: Config = load_config()
router = Router()
router.message.filter(IsSuperAdmin())

admin_ids = str(config.tg_bot.admin_ids).split(',')


class FsmTexts(StatesGroup):
    thursday_text = State()
    sunday_text = State()
    every_day_text = State()
    thirst_day_text = State()

    new_text = State()


@router.message(F.text == 'Изменить текст 📄')
async def change_texts(message: types.Message, state: FSMContext):
    """Изменение текста"""
    logging.info('change_texts')
    check_texts = await admin_requests.check_texts()
    if check_texts:
        markup = await admin_keyboard.select_text_buttons()
        text = (f'🔹Четверг: {check_texts["thursday_text"]}\n\n'
                f'🔹Воскресенье: {check_texts["sunday_text"]}\n\n'
                f'🔹Каждый день в 22:00: {check_texts["every_day_text"]}\n\n'
                f'🔹Каждое 1 число месяца: {check_texts["thirst_day_text"]}\n\n'
                f'Выберите текст который вы хотите изменить 👇')
        await message.answer(text=text, reply_markup=markup)
    else:
        await state.set_state(FsmTexts.thursday_text)
        await message.answer('Добавление текста 📄\n\n'
                             'Введите текст который будет отправляться в четверг 👇')


@router.message(StateFilter(FsmTexts.thursday_text))
async def get_thursday_text(message: types.Message, state: FSMContext):
    """Получение первого текста для четверга"""
    logging.info('get_thursday_text')
    markup = await admin_keyboard.back_buttons('back-first-text_thursday')

    await state.update_data(thursday_text=str(message.text))
    await state.set_state(FsmTexts.sunday_text)
    await message.answer('Добавление текста 📄\n\n'
                         'Введите текст который будет отправляться в воскресенье 👇',
                         reply_markup=markup)


@router.message(StateFilter(FsmTexts.sunday_text))
async def get_sunday_text(message: types.Message, state: FSMContext):
    """Получение первого текста для воскрсьенья"""
    logging.info('get_sunday_text')
    markup = await admin_keyboard.back_buttons('back-first-text_sunday')

    await state.update_data(sunday_text=str(message.text))
    await state.set_state(FsmTexts.every_day_text)
    await message.answer('Добавление текста 📄\n\n'
                         'Введите текст который будет отправляться каждый день в 22:00 👇',
                         reply_markup=markup)


@router.message(StateFilter(FsmTexts.every_day_text))
async def get_every_day_text(message: types.Message, state: FSMContext):
    """Получение сообщения которое будет отправляться каждый день"""
    logging.info('get_every_day_text')
    markup = await admin_keyboard.back_buttons('back-first-text_every-day')

    await state.update_data(every_day_text=str(message.text))
    await state.set_state(FsmTexts.thirst_day_text)
    await message.answer('Добавление текста 📄\n\n'
                         'Введите текст который будет отправляться каждое 1 число 👇',
                         reply_markup=markup)


@router.message(StateFilter(FsmTexts.thirst_day_text))
async def get_thirst_day_text(message: types.Message, state: FSMContext):
    """Получение текста который будет отправляться каждое 1 число"""
    logging.info('get_thirst_day_text')
    await state.update_data(thirst_day_text=str(message.text))
    await state.set_state(default_state)

    state_data = await state.get_data()
    await admin_requests.add_text(
        state_data['thursday_text'],
        state_data['sunday_text'],
        state_data['every_day_text'],
        state_data['thirst_day_text']
    )

    await message.answer('Тексты успешно добавлены ✅\n'
                         'Вы можете в любой момент их изменить нажав на кнопку "Изменить текст 📄"')


@router.callback_query(F.data.startswith('back-first-text_'))
async def back_buttons(callback: types.CallbackQuery, state: FSMContext):
    """Обработка кнопок назад"""
    logging.info('back_buttons')
    flag = str(callback.data).split('_')[1]
    if flag == 'thursday':
        await state.set_state(FsmTexts.thursday_text)
        await callback.message.edit_text('Добавление текста 📄\n\n'
                                         'Введите текст который будет отправляться в четверг 👇')

    if flag == 'sunday':
        markup = await admin_keyboard.back_buttons('back-first-text_thursday')
        await state.set_state(FsmTexts.sunday_text)
        await callback.message.edit_text('Добавление текста 📄\n\n'
                                            'Введите текст который будет отправляться в воскресенье 👇',
                                            reply_markup=markup)

    if flag == 'every-day':
        markup = await admin_keyboard.back_buttons('back-first-text_sunday')
        await state.set_state(FsmTexts.every_day_text)
        await callback.message.edit_text('Добавление текста 📄\n\n'
                                            'Введите текст который будет отправляться каждый день в 22:00 👇',
                                            reply_markup=markup)

    if flag == 'select-day':
        markup = await admin_keyboard.select_text_buttons()
        check_texts = await admin_requests.check_texts()
        text = (f'🔹Четверг: {check_texts["thursday_text"]}\n\n'
                f'🔹Воскресенье: {check_texts["sunday_text"]}\n\n'
                f'🔹Каждый день в 22:00: {check_texts["every_day_text"]}\n\n'
                f'🔹Каждое 1 число месяца: {check_texts["thirst_day_text"]}\n\n'
                f'Выберите текст который вы хотите изменить 👇')
        await state.set_state(default_state)
        await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data.startswith('edit-text_'))
async def select_text_to_edit(callback: types.CallbackQuery, state: FSMContext):
    """Выбор текста для изменения"""
    logging.info('select_text_to_edit')
    flag = str(callback.data).split('_')[1]
    markup = await admin_keyboard.back_buttons('back-first-text_select-day')

    if flag == 'thursday-text':
        text = 'Изменение текста 📄\n\nВведите текст который будет отправляться в четверг 👇'
    if flag == 'sunday-text':
        text = 'Изменение текста 📄\n\nВведите текст который будет отправляться в воскресенье 👇'
    if flag == 'every-day-text':
        text = 'Изменение текста 📄\n\nВведите текст который будет отправляться каждый день в 22:00 👇'
    if flag == 'thirst-day-text':
        text = 'Изменение текста 📄\n\nВведите текст который будет отправляться каждое 1 число 👇'

    await state.update_data(flag=flag)
    await state.set_state(FsmTexts.new_text)
    await callback.message.edit_text(text=text, reply_markup=markup)


@router.message(StateFilter(FsmTexts.new_text))
async def get_new_text(message: types.Message, state: FSMContext):
    """Получение нового текста"""
    logging.info('get_new_text')
    new_text = str(message.text)
    state_data = await state.get_data()
    markup = await admin_keyboard.select_text_buttons()

    await admin_requests.update_text(state_data['flag'], new_text)

    check_texts = await admin_requests.check_texts()
    text = (f'🔹Четверг: {check_texts["thursday_text"]}\n\n'
            f'🔹Воскресенье: {check_texts["sunday_text"]}\n\n'
            f'🔹Каждый день в 22:00: {check_texts["every_day_text"]}\n\n'
            f'🔹Каждое 1 число месяца: {check_texts["thirst_day_text"]}\n\n'
            f'Выберите текст который вы хотите изменить 👇')
    await state.set_state(default_state)
    await message.answer(text=text, reply_markup=markup)





