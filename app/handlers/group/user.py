from aiogram import Dispatcher
from aiogram.types import Message

from app.filters.user import CommandFilter


async def process_group_commands(m: Message):
    # get data from DB by user_id and key word
    # await m.reply(data)
    await m.answer(f'Сработал хендлер на комманду: {m.text}')


def register_group_user(dp: Dispatcher):
    dp.register_message_handler(
        process_group_commands, CommandFilter()
    )
