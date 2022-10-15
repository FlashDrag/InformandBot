from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def admin_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    admin = KeyboardButton(text='/admin')

    markup.add(admin)
    return markup


def menu_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    menu = KeyboardButton(text='Main Menu')

    markup.add(menu)
    return markup
