from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ChatType
from aiogram.dispatcher.filters import Text, CommandStart
from aiogram.types import ReplyKeyboardRemove

from keyboards.admin_kb.default_kb import admin_button, menu_button
from keyboards.admin_kb.inline_kb import ikb_admin_panel

from aiogram.types.bot_command import BotCommand
from aiogram.types import BotCommandScopeAllGroupChats


async def admin_start_process(m: Message, state: FSMContext):
    await m.answer('The same message as to user',
                   reply_markup=admin_button())
    await state.reset_state(with_data=True)


async def show_admin_panel(m: Message, state: FSMContext):
    await m.answer('Hello, Admin! Would you like to add, edit or remove the commands?',
                   reply_markup=ikb_admin_panel())
    await state.reset_state(with_data=True)


async def show_admin_panel_query(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Hello, Admin! Would you like to add, edit or remove the commands?',
                              reply_markup=ikb_admin_panel())
    await state.reset_state(with_data=True)
    await call.answer()

'''
async def set_com(m: Message, state: FSMContext):
    bot = m.bot
    print(bot)
    # комманды получаем с БД и через map либо цикл делаем инстансы каждой комманды в классе BotCommand,
    # при создании обьекта комманды `BotCommand` задаем два имменованных агрументы либо ** распаковкой
    commmands = [BotCommand(command='/обед', description='расписание на обед')]
    await bot.set_my_commands(commmands=commmands, scope=BotCommandScopeAllGroupChats())


async def process_commands(m: Message, state: FSMContext):
    print(m.date)
    print(m)
'''


def register_common_private_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_start_process, CommandStart(),
        chat_type=[ChatType.PRIVATE], is_admin=True)

    dp.register_message_handler(
        show_admin_panel, commands=['admin', 'cancel'], chat_type=[ChatType.PRIVATE],
        is_admin=True, state='*')
    dp.register_message_handler(
        show_admin_panel, Text(
            equals=['cancel', 'Main Menu'], ignore_case=True),
        chat_type=[ChatType.PRIVATE], is_admin=True, state='*')

    dp.register_callback_query_handler(
        show_admin_panel_query, text='cancel',
        chat_type=[ChatType.PRIVATE], is_admin=True, state="*")

    # dp.register_message_handler(set_com, commands='setcom')
    # dp.register_message_handler(process_commands, commands=['обед', 'стирка'])
