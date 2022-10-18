from aiogram import Dispatcher
from aiogram.types import Message

from app.filters.user import CommandFilter


async def process_group_commands(m: Message):
    # get data from DB by user_id and key word
    # await m.reply(data)
    await m.answer(f'Сработал хендлер на комманду: {m.text}')

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


def register_group_user(dp: Dispatcher):
    dp.register_message_handler(
        process_group_commands, CommandFilter()
    )
