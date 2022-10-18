from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ChatType

# TODO Confirm state will be set for confirm_data, edit and remove handlers
from states.admin import AddData, Confirm

from keyboards.admin_kb.default_kb import menu_button


# TODO Doble check the func
async def confirm_data(call: CallbackQuery, state: FSMContext):
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
        await call.message.answer(f'An error was occurred!')
        await call.message.answer(f'Set a command:'
                                  f'a word(without /) with max lengh of 10 Latin-script letters or/and numbers',
                                  reply_markup=menu_button())
        await state.set_state(AddData.com)
    elif not description:
        await call.message.answer('An error was occurred!')
        await call.message.answer(f'Text a command description to be displayed in the main menu '
                                  f'The description should reflect the essence of the text',
                                  reply_markup=menu_button())
        await state.set_state(AddData.descr)
    elif not text:
        await call.message.answer('An error was occurred!')
        await call.message.answer(f'Now you can send me a text, picture, video, audio, document or sticker\n'
                                  f'which will be shown to user after the command execution',
                                  reply_markup=menu_button())
        await state.set_state(AddData.content)
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

# TODO register in bot.py
def register_add_data_admin(dp: Dispatcher):
    dp.register_callback_query_handler(
        confirm_data, text='confirm', state=Confirm.wait_confirm,
        chat_type=[ChatType.PRIVATE], is_admin=True)
