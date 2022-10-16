from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ChatType, InputFile
from aiogram.dispatcher.filters import Text

from states.admin import AddData, Confirm

from keyboards.admin_kb.inline_kb import ikb_confirm, ikb_admin_panel
from keyboards.admin_kb.default_kb import menu_button

from string import ascii_letters, digits


async def add_data(call: CallbackQuery, state: FSMContext):
    photo = InputFile('content/command.png')
    await call.message.answer_photo(photo=photo)
    await call.message.answer(f'Set a command:'
                              f'a word(without /) with max lengh of 10 Latin-script letters or / and numbers',
                              reply_markup=menu_button())
    await call.answer()
    await state.set_state(AddData.com)


async def get_com(m: Message, state: FSMContext):
    command = m.text
    alnum = ascii_letters + digits
    if command.startswith("/"):
        command = command[1:]
    if not set(command).issubset(set(alnum)) or not len(command) <= 10:
        await m.answer(f'An error was occurred!')
        await m.answer('Set a command: a word with max lengh of 10 Latin-script letters or numbers',
                       reply_markup=menu_button())
        return

    async with state.proxy() as data:
        data['command'] = command
        description = data.get('descr')
        text = data.get('text')
        if not description:
            photo = InputFile('description/command.png')
            await m.answer_photo(photo=photo)
            await m.answer(f'Text a command description to be displayed in the main menu.\n'
                           f'The description should reflect the essence of the text')
            await state.set_state(AddData.descr)
        elif not text:
            animation = InputFile('description/animation.gif')
            await m.answer_animation(animation=animation)
            await m.answer(f'Now send me a text or picture\n'
                           f'which will be shown to user after the command execution')
            await state.set_state(AddData.text)
        else:
            # TODO
            pass


async def get_descr(m: Message, state: FSMContext):
    # TODO process comm_decsr
    # validation:isinstance() 0 < len < ~10, is_printable

    # if validation false:
    #     await m.answer('send coorect descr')
    #     return

    async with state.proxy() as data:
        data['descr'] = m.text

    animation = InputFile('description/animation.gif')
    await m.answer_animation(animation=animation)
    await m.answer(f'Now send me a text or picture\n'
                   f'which will be shown to user after the command execution')
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
    command, description, text = \
        data.get('command'), data.get('descr'), data.get('text')
    # checker = {'command': bool(command), 'description': bool(description), 'text': bool(text)}
    # if not all(checker.values()):
    #     text = ', '.join(filter(lambda key: checker[key] is False, checker))
    #     await m.answer(f'An error was occurred in: {text}', reply_markup=ikb_admin_panel())
    #     await state.finish()
    # or
    if not command:
        await m.answer(f'An error was occurred!')
        await m.answer('Set a command: a word with max lengh of 10 Latin-script letters or numbers',
                       reply_markup=menu_button())
        await state.set_state(AddData.com)
    elif not description:
        await m.answer('An error was occurred!')
        await m.answer(f'Text a command description to be displayed in the main menu '
                       f'The description should reflect the essence of the text',
                       reply_markup=menu_button())
        await state.set_state(AddData.descr)
    elif not text:
        await m.answer('An error was occurred!')
        await m.answer(f'Send me a text or picture\n'
                       f'which will be shown to user after the command execution',
                       reply_markup=menu_button())
        await state.set_state(AddData.text)
    else:
        # save data to DB (данные должны быть привязаны к id админа и его группе для которой он задал эти комманды)
        # лучше не добавлять через аппенд,
        # а после добавления в бд получать все ключи-значения
        # и полностью обновлять list my_command,
        # a также переустанавливать комманды
        my_commands[data['command']] = data['descr']


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
