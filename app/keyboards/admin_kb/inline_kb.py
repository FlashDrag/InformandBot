from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ikb_admin_panel():
    markup = InlineKeyboardMarkup(row_width=1)
    add = InlineKeyboardButton(text='Добавити команду', callback_data='add_com')
    rem = InlineKeyboardButton(text='Видалити команду', callback_data='rem_com')

    markup.add(add, rem)
    return markup
