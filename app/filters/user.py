import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from bot import my_commands


class CommandFilter(BoundFilter):

    async def check(self, obj: typing.Optional[Message]):
        if isinstance(obj, Message) and obj.is_command():
            data = obj.text
            if data[1:].isalnum() and len(data) <= 11:
                return data[1:] in my_commands
        return False
