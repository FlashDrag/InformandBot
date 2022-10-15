from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ChatType
from aiogram.dispatcher.filters import Text

from states.admin import AddData, Confirm

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
    # obj Message must have text
    # get text from obj Message
    # if text.startswith("/"):
    # if data[1:].isalnum() and len(data) <= 11:

    # if isinstance(obj, Message) and obj.is_command():
    #         data = obj.text

    async with state.proxy() as data:
        data['command'] = m.text

    await m.answer(f'Text a short command description to be displayed '
                   f'in front of the command in main menu')
    await state.set_state(AddData.descr)


async def get_descr(m: Message, state: FSMContext):
    # TODO process comm_decsr
    # validation:isinstance() 0 < len < ~10, is_printable

    # if validation false:
    #     await m.answer('send coorect descr')
    #     return

    async with state.proxy() as data:
        data['descr'] = m.text

    await m.answer(f'Now send me the text which will be shown '
                   f'to user after the command execution')
    await state.set_state(AddData.text)


async def get_data(m: Message, state: FSMContext):
    # TODO process data
    # validation: len > 0, can be picture, text etc.
    # if data not a text, it cant be saved to fsm-storage
    async with state.proxy() as data:
        data['text'] = m.text

    await m.answer('Check the data', reply_markup=ikb_confirm())
    # TODO show all data
    state.set_state(Confirm.wait_confirm)


async def confirm_data(m: Message, state: FSMContext):
    from bot import my_commands
    data = state.get_data()
    # лучше не добавлять через аппенд,
    # а после добавления в бд получать все ключи-значения
    # и полностью обновлять list my_command,
    # a также переустанавливать комманды
    my_commands.append({'command': data['command'], 'decsription': data['descr']})


# TODO After user confiramtion, all data must save to db
# Keys copies will be saved to list or set for filter
# which will be check bot_update for keys and give permision for handler.
# Keys must copy from DB to list periodicly and by startup (check in aiogram long handler)
# All custom commands must to load from db and set up by app startup
# The command must to be set


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
        get_data, state=AddData.text,
        chat_type=[ChatType.PRIVATE], is_admin=True)

    dp.register_message_handler(
        confirm_data, state=Confirm.wait_confirm,
        chat_type=[ChatType.PRIVATE], is_admin=True)
