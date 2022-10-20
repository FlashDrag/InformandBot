from sys import ps1
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ChatType

from states.admin import Confirm, EditData

from keyboards.admin_kb.inline_kb import ikb_edit

# TODO Это меню можно вызвать в двух случаях:
# 1. С главного меню ikb_admin_panel();
# Здесь хедлер вызывается только по callback_data='edit_data', state=None
# 2. С меню подтверждения ввода данных ikb_confirm();
# Здесь также callback_data='edit_data', но state=Confirm.wait_confirm


async def edit_data(call: CallbackQuery, state: FSMContext):
    data = state.get_data()
    if data:
        await call.message.answer('What you need to edit?', reply_markup=ikb_edit())
        await state.set_state(EditData.wait_edit)
        await call.answer()
# TODO Если storage пустой, сначала админ должен выбрать комманду к которой привязаны остальные данные
# а потом уже выбирать что он хочет отредачить


async def edit_command(call: CallbackQuery, state: FSMContext):
    pass


async def edit_description(call: CallbackQuery, state: FSMContext):
    pass


async def edit_content(call: CallbackQuery, state: FSMContext):
    pass


# TODO Add to main
def register_edit_data_admin(dp: Dispatcher):
    dp.register_callback_query_handler(
        edit_data, text='edit_data', state=Confirm.wait_confirm,
        chat_type=[ChatType.PRIVATE], is_admin=True)
    dp.register_callback_query_handler(
        edit_data, text='edit_data',
        chat_type=[ChatType.PRIVATE], is_admin=True)
