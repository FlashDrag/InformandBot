import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from app.utils.set_bot_commands import my_commands


class CommandFilter(BoundFilter):
    '''
    Обрабатывает получаемый апдейт на Комманду
    Проводит валидацию на длину и наличие в глобальном словаре кастомных комманд админа,
    которые сохранены в БД периодически загружаються в этот словарь
    '''
    async def check(self, obj: typing.Optional[Message]):
        if isinstance(obj, Message) and obj.is_command():
            data = obj.text
            if data[1:].isalnum() and len(data) <= 11:
                return data[1:] in my_commands
        return False


class UserExistFilter(BoundFilter):
    '''
    Return True if the user already exist in the DB
    '''
    async def check(self, obj: typing.Optional[Message]):
        user_id = obj.from_user.id
        return user_id in "DB"  # TODO
