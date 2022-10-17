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
                              f'a word(without /) with max lengh of 10 Latin-script letters or/and numbers',
                              reply_markup=menu_button())
    await state.set_state(AddData.com)
    await call.answer()


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
    after succesful validation - adding command to storage;
    request data which is not in storage yet, set state for waiting requested data
    '''
    async with state.proxy() as data:
        data['command'] = command
        # getting data or None
        description = data.get('descr')
        text = data.get('text')

        # request data if None
        if not description:
            photo = InputFile('description/command.png')
            await m.answer_photo(photo=photo)
            await m.answer(f'Text a command description to be displayed in the main menu.\n'
                           f'The description should reflect the essence of the text')
            await state.set_state(AddData.descr)
        elif not text:
            animation = InputFile('description/animation.gif')
            await m.answer_animation(animation=animation)
            await m.answer(f'Now you can send me a text, picture, video, audio, document or sticker\n'
                           f'which will be shown to user after the command execution')
            await state.set_state(AddData.text)
        else:
            # TODO confirm
            pass


async def get_descr(m: Message, state: FSMContext):
    '''description validation'''
    descr = m.text
    if 1 > len(descr) > 20:
        await m.answer(f'The description length must be minimum 1 and max 20 symbols.\n'
                       f'Try again', reply_markup=menu_button())
        return

    async with state.proxy() as data:
        data['descr'] = m.text

        # getting data or None
        text = data.get('text')
        if not text:
            animation = InputFile('description/animation.gif')
            await m.answer_animation(animation=animation)
            await m.answer(f'Now you can send me a text, picture, video, audio, document or sticker\n'
                           f'which will be shown to user after the command execution')
            await state.set_state(AddData.text)
        else:
            # TODO confirm
            pass


async def get_data(m: Message, state: FSMContext):
    '''saving file_id to data if content_type is not a text'''
    content_type = m.content_type

    if content_type == 'text':
        data = m.text
    elif content_type == 'photo':
        data = m.photo[-1].file_id  # TODO doble check the method of getting file_id
    else:
        data = m[content_type]['file_id']
    async with state.proxy() as d:
        d['content'] = {'content_type': content_type, 'data': data}

    await m.answer('Check the data', reply_markup=ikb_confirm())
    # TODO show all data
    state.set_state(Confirm.wait_confirm)  # TODO confirm_data, edit and remove handlers shoud set for the state


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
        chat_type=[ChatType.PRIVATE], is_admin=True,
        content_types=['text', 'audio', 'document', 'animation',
                       'photo', 'sticker', 'video', 'video_note', 'voice'])
