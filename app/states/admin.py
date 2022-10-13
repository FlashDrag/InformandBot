from aiogram.dispatcher.filters.state import StatesGroup, State


class AddCom(StatesGroup):
    com_name = State()
    com_descr = State()
    com_text = State()


class RemoveCom(StatesGroup):
    pass