from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ChatType
from aiogram.dispatcher.filters import Text, CommandStart

from aiogram import Dispatcher
from aiogram.types import Message

from app.filters.user import CommandFilter, UserExistFilter

# from app.services.repository import Repo
# from states.user import UserMain


# welcome is showing only in private chat
async def show_welcome(message: Message, state: FSMContext):
    await message.answer('Hello user. Open menu and choose what you need.')


async def process_exist_user_commands(m: Message):
    '''
    Send respond to user for command from custom menu
    Always send response to private chat avoiding unnecessary notifications of other chat participants
    '''
    bot = m.bot
    # get data from DB by user_id and key word
    # await m.reply(data)
    await bot.send_message(m.from_user.id, f'Сработал хендлер на комманду: {m.text}')

    # TODO как обрабатывать данные
    # получаем type_content и data(может быть текст или file_id) c БД и сохр в переменные
    # если type_content == text то отправляем юзеру в группе прямо data
    '''
    data = await state.get_data()
    file_id = data['content'].get('data')
    content_type = data['content'].get('content_type')
    parser = 'answer_' + content_type
    m_answer = getattr(m, parser)
    await m_answer(file_id)
    '''
    # если type_content другой то подбираем метод для отправки
    # file = InputFile(data) # data у нас file_id, получаем файл в переменную
    # await m.answer_type_content(type_content=file)
    # await m.answer_animation(animation=animation)


async def process_nonexist_user_commands(m: Message):
    '''Send reply to the message in the group chat if the user not exist
    Respond for any exist commands: a link for bot private chat'''
    await m.reply(f'Go to the bot and ask repeat the command\n'
                  f'https://t.me/InformandBot?start')


def register_user(dp: Dispatcher):
    dp.register_message_handler(
        show_welcome, CommandStart(),
        chat_type=[ChatType.PRIVATE], state=None)

    dp.register_message_handler(
        process_exist_user_commands, CommandFilter(), UserExistFilter()
    )
    dp.register_message_handler(
        process_nonexist_user_commands, CommandFilter(),
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]
    )
