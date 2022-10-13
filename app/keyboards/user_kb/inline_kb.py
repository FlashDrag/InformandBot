from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ikb_main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text='Button', callback_data='Button')
    markup.add(button)
    return markup
