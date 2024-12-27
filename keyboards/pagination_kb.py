from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON

def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=LEXICON[button] if button in LEXICON else button, 
                                          callback_data=button) for button in buttons])
    kb_builder.row(InlineKeyboardButton(text=LEXICON['list_genre'], callback_data='list_genre'))
    return kb_builder.as_markup()