from aiogram.dispatcher.filters.state import StatesGroup, State


class AddData(StatesGroup):
    com = State()
    descr = State()
    content = State()


class EditData(StatesGroup):
    wait_edit = State()
    com = State()
    descr = State()
    text = State()


class RemoveData(StatesGroup):
    com = State()


class Confirm(StatesGroup):
    wait_confirm = State()