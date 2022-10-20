from importlib.resources import contents
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ChatType, InputFile
from aiogram.dispatcher.filters import Text
from magic_filter import F

from states.admin import AddData, Confirm

from keyboards.admin_kb.inline_kb import ikb_confirm, ikb_admin_panel
from keyboards.admin_kb.default_kb import menu_button

from string import ascii_letters, digits


async def add_data(call: CallbackQuery, state: FSMContext):
    photo = InputFile('content/command.png')
    await call.message.answer_photo(photo=photo)
    await call.message.answer(f'Set a command:'
                              f'a word(without /) with max lengh of 10 Latin-script letters or/and numbers',
                              reply_markup=menu_button())
    await state.set_state(AddData.com)
    await call.answer()


async def show_data(m: Message, state: FSMContext):
    await m.answer('Check the data')

    data_dict: dict = state.get_data()

    command: str = data_dict.get('command')
    description: str = data_dict.get('descr')
    content: dict = data_dict['content']  # content_type and data(text or file_id)

    content_type: str = content.get('content_type')
    data: str = content.get('data')  # file_id or text (or None)

    # display the results to user
    await m.answer(f'Command: {command}\n'
                   f'Description: {description}\n')

    # if content_type is media, get Message method by parser;
    # using special method send media to client by file_id (raw media already storaged on TG server)
    if content_type != 'text':
        parser = 'answer_' + content_type  # answer_photo, etc.
        m_answer = getattr(m, parser)
        await m_answer(data, reply_markup=ikb_confirm())  # `m_answer` same as `m.answer_photo`, etc
    else:
        # if content_type is text, send to client raw data directly from DB
        await m.answer(f'Content: {data}', reply_markup=ikb_confirm())

    state.set_state(Confirm.wait_confirm)


async def get_com(m: Message, state: FSMContext):
    command = m.text
    alnum = ascii_letters + digits
    if command.startswith("/"):
        command = command[1:]

    '''command validation'''
    if not set(command).issubset(set(alnum)) or len(command) > 10:
        await m.answer(f'An error was occurred!')
        await m.answer(f'Set a command:'
                       f'a word(without /) with max lengh of 10 Latin-script letters or/and numbers',
                       reply_markup=menu_button())
        return
    '''
    after succesful validation - add command to storage;
    request data which is not in storage yet, set state for waiting requested data
    '''
    async with state.proxy() as data:
        data['command'] = command
        # getting data or None
        description = data.get('descr')
        content = data.get('content')

        # request data from user if None
        if not description:
            photo = InputFile('description/command.png')
            await m.answer_photo(photo=photo)
            await m.answer(f'Text a command description to be displayed in the main menu.\n'
                           f'The description should reflect the essence of the next step attached content')
            await state.set_state(AddData.descr)
        elif not content:
            animation = InputFile('description/animation.gif')
            await m.answer_animation(animation=animation)
            await m.answer(f'Now you can send me a text, picture, video, audio, document or sticker\n'
                           f'which will be shown to user after the command execution')
            await state.set_state(AddData.content)
        else:
            await show_data(m, state)


async def get_descr(m: Message, state: FSMContext):
    '''description validation'''
    descr = m.text
    if 1 > len(descr) > 20:
        await m.answer(f'The description length must be between 1-20 characters.\n'
                       f'Try again', reply_markup=menu_button())
        return

    async with state.proxy() as data:
        data['descr'] = m.text

        # getting data or None
        content = data.get('content')
        if not content:
            animation = InputFile('description/animation.gif')
            await m.answer_animation(animation=animation)
            await m.answer(f'Now you can send me a text, picture, video, audio, document or sticker\n'
                           f'which will be shown to user after the command execution')
            await state.set_state(AddData.content)
        else:
            await show_data(m, state)


async def get_content(m: Message, state: FSMContext):
    '''saving file_id to data if content_type is not a text'''
    content_type = m.content_type
    # validation
    if content_type == 'text':
        if 1 > len(m.text) > 1000:
            await m.answer(f'The text lenght must be between 1-1000 characters.\nTry again')
            return

    if content_type == 'text':
        data = m.text
    elif content_type == 'photo':
        data = m.photo[-1].file_id
    else:
        data = getattr(m, content_type).file_id
        # data = m[content_type]['file_id'
    async with state.proxy() as d:
        d['content'] = {'content_type': content_type, 'data': data}

    try:
        await show_data(m, state)
    except Exception as e:
        print(f'Error with show_data() func!\n'
              f'{type(e).__name__}: {e}')
        await m.answer(f'Error. Try again', reply_markup=ikb_admin_panel())
        await state.finish()


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
        get_content, state=AddData.content,
        chat_type=[ChatType.PRIVATE], is_admin=True,
        content_types=['text', 'audio', 'document', 'animation',
                       'photo', 'sticker', 'video', 'video_note', 'voice'])
