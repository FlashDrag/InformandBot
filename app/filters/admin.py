import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from app.config import Config


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        if self.is_admin is None:
            return False
        config: Config = obj.bot.get('config')
        return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_admin


'''
class LettersInMessageFilter(BoundFilter):
    """
    Checking for the number of characters in a message/callback_data
    """

    key = "letters"

    def __init__(self, letters: int):
        if isinstance(letters, int):
            self.letters = letters
        else:
            raise ValueError(
                f"filter letters must be a int, not {type(letters).__name__}"
            )

    async def check(self, obj: Union[types.Message, types.CallbackQuery]):
        data = obj.text or obj.data
        if data:
            letters_in_message = len(data)
            if letters_in_message > self.letters:
                return False  # or {"Too long"}
            return {"letters": letters_in_message}
        return False


@dp.message_handler(letters=5)
async def handle_letters_in_message(message: types.Message, letters: int):
    await message.answer(f"Message too short!\nYou sent only {letters} letters")
'''
