from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ChatType
from aiogram.dispatcher.filters import Text

from states.admin import AddData

from keyboards.admin_kb.inline_kb import ikb_confirm
from keyboards.admin_kb.default_kb import menu_button


async def add_data(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Text a command to be displayed in the main menu',
                              reply_markup=menu_button())
    await call.answer('The command should reflect the essence of the text',
                      show_alert=True)
    await state.set_state(AddData.com)


async def get_com(m: Message, state: FSMContext):
    # TODO process comm_name: validation for str; no punctuation, no digits; check for len
    # save to redis
    await m.answer(f'Text a short command description to be displayed '
                   f'in front of the command in main menu')
    await state.set_state(AddData.descr)


async def get_descr(m: Message, state: FSMContext):
    # TODO process comm_decsr
    # save to redis
    await m.answer(f'Now send me the text which will be shown '
                   f'to user after the command execution')
    await state.set_state(AddData.text)


async def get_text(m: Message, state: FSMContext):
    # TODO process data_text
    # save to redis
    await m.answer('Check the data', reply_markup=ikb_confirm())
    # show all data
    # TODO: state.set_state(Confirm)

# TODO After user confiramtion, all data must save to db
# And the command must to be set


def register_add_data_admin(dp: Dispatcher):
    dp.register_callback_query_handler(
        add_data, text='add_data',
        chat_type=[ChatType.PRIVATE], is_admin=True)
    dp.register_message_handler(
        get_com, state=AddData.com,
        chat_type=[ChatType.PRIVATE], is_admin=True)
    dp.register_message_handler(
        get_descr, state=AddData.descr,
        chat_type=[ChatType.PRIVATE], is_admin=True)
    dp.register_message_handler(
        get_text, state=AddData.text,
        chat_type=[ChatType.PRIVATE], is_admin=True)
