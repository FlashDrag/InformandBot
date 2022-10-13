from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ChatType
from aiogram.dispatcher.filters import Text, CommandStart
from aiogram.types import ReplyKeyboardRemove

from keyboards.admin_kb.default_kb import admin_button, menu_button
from keyboards.admin_kb.inline_kb import ikb_admin_panel


async def admin_start_process(m: Message):
    await m.answer('The same message as to user',
                   reply_markup=admin_button())


async def show_admin_panel(m: Message, state: FSMContext):
    await m.answer('Hello, Admin! Would you like to add, edit or remove any data?',
                   reply_markup=ikb_admin_panel())
    await state.reset_state(with_data=True)


def register_start_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_start_process, CommandStart(),
        chat_type=[ChatType.PRIVATE], is_admin=True)
    dp.register_message_handler(
        show_admin_panel, Text(
            equals=['/admin', 'cancel', 'Main Menu'], ignore_case=True),
        chat_type=[ChatType.PRIVATE], is_admin=True, state='*')
