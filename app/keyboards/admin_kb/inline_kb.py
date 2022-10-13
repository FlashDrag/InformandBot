from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ikb_admin_panel():
    markup = InlineKeyboardMarkup(row_width=1)
    add = InlineKeyboardButton(text='Add data', callback_data='add_data')
    edit = InlineKeyboardButton(text='Edit data', callback_data='edit_data')
    rem = InlineKeyboardButton(text='Remove data', callback_data='rem_data')

    markup.add(add, edit, rem)
    return markup


def ikb_confirm():
    markup = InlineKeyboardMarkup()
    confirm = InlineKeyboardButton(text='Confirm', callback_data='confirm')
    edit = InlineKeyboardButton(text='Edit', callback_data='edit_data')
    cancel = InlineKeyboardButton(text='Cancel', callback_data='cancel')

    markup.row(confirm)
    markup.row(edit, cancel)
    return markup


def ikb_edit():
    markup = InlineKeyboardMarkup(row_width=1)
    com = InlineKeyboardButton(text='Edit Command', callback_data='edit_com')
    descr = InlineKeyboardButton(text='Edit Description', callback_data='edit_descr')
    text = InlineKeyboardButton(text='Edit Main text', callback_data='edit_text')

    markup.add(com, descr, text)
    return markup
