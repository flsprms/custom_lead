import asyncio
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.get_id_kb import get_id_kb
from keyboards.cancel_kb import get_cancel_kb
from send_to_chatter import send_to_chatter, SendMessageToChatterError


router = Router()


class GetMessage(StatesGroup):
    get_message = State()


class SendMessageError(Exception):
    pass


# обработка нажатия inline кнопки, которая запускает процесс отправки сообщения в chatter
@router.callback_query(F.data == 'send_message')
async def handle_send_message(callback_query: CallbackQuery, state: FSMContext):
    message = callback_query.message
    lead_id = message.text.split('\n')[0][1:]

    await message.answer('Введите ваше сообщение:', reply_markup=get_cancel_kb())

    # запись lead_id из сообщения в память state
    await state.update_data(lead_id=lead_id)

    await state.set_state(GetMessage.get_message)
    await callback_query.answer()


@router.message(Command("start"))
async def start(message: Message):
    user_full_name = message.from_user.full_name
    await message.answer(f'Здравствуйте, {user_full_name}!', reply_markup=get_id_kb())


@router.message(F.text.lower() == "мой telegram id")
async def get_id(message: Message):
    user_id = message.from_user.id

    await message.answer(f'Ваш teleram id:\n{user_id}')


@router.message(GetMessage.get_message, F.text.lower() == "отмена")
async def cancel(message: Message, state: FSMContext):
    await message.answer('Отмена ввода сообщения', reply_markup=get_id_kb())
    await state.clear()


# отправка сообщения в chatter
@router.message(GetMessage.get_message, F.text)
async def send_message(message: Message, state: FSMContext):
    # считывание lead id из памяти state
    data = await state.get_data()
    lead_id = data['lead_id']

    try:
        await message.answer('Отправка сообщения...')
        await send_to_chatter(lead_id, message.text)
        await message.answer(f'#{lead_id}\n\n\"{message.text}\"\n\nСообщение отправлено!', reply_markup=get_id_kb())
        await state.clear()

    except SendMessageToChatterError:
        await message.answer('Не удалось отправить сообщение!\nПопробуйте ещё раз')