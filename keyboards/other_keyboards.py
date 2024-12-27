from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon import LEXICON

def create_choice_genres(*args: str) -> InlineKeyboardMarkup: 
    kb_keyboard = InlineKeyboardBuilder() 
    for genre in args:
        kb_keyboard.row(InlineKeyboardButton(text=genre, callback_data=genre))
    kb_keyboard.row(InlineKeyboardButton(text=LEXICON['list_genre'], callback_data='list_genre'), 
                    InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel'), 
                    width=2)
    return kb_keyboard.as_markup()


def create_choice_book(*args: str) -> InlineKeyboardMarkup: 
    kb_keyboard = InlineKeyboardBuilder() 
    for book in args:
        kb_keyboard.row(InlineKeyboardButton(text=f'{book[0]}: "{book[1]}"', callback_data=book[1]))
    kb_keyboard.row( InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel'))
    return kb_keyboard.as_markup()