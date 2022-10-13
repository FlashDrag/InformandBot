from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ChatType
from aiogram.dispatcher.filters import Text, CommandStart

# from app.services.repository import Repo
# from states.user import UserMain


async def show_welcome(message: Message, state: FSMContext):
    await message.answer('Welcome')


def register_private_user(dp: Dispatcher):
    dp.register_message_handler(
        show_welcome, CommandStart(),
        chat_type=[ChatType.PRIVATE], state=None)  # TODO
