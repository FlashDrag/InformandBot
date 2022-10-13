from aiogram.dispatcher.filters import BoundFilter


class AdminFilter(BoundFilter):
    key = 'private_chat'

    def __init__(self, chat_type=None):
        self.chat_type = chat_type