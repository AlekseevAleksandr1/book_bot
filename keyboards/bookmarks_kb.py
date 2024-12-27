#закладки

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon import LEXICON
from database.database import users_dp
from services.file_handling import book

def create_bookmarks_keyboard(id,**kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for book_id in kwargs.keys():
        kb_builder.row(InlineKeyboardButton(text=f'{users_dp[id]['bookmarks'][book_id]['author']}:{users_dp[id]['bookmarks'][book_id]['title']}--{users_dp[id]['bookmarks'][book_id]['page']}',
                                            callback_data=book_id))
    
    kb_builder.row(InlineKeyboardButton(text=LEXICON['edit_bookmarks_button'],callback_data='edit_bookmarks'), 
                    InlineKeyboardButton(text=LEXICON['cancel'],callback_data='cancel'),width=2)
        
    return kb_builder.as_markup()
    
def create_edit_keyboard(id,**kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for book_id in kwargs.keys():
        kb_builder.row(InlineKeyboardButton(text=f'{LEXICON['del']} {users_dp[id]['bookmarks'][book_id]['title']}--{users_dp[id]['bookmarks'][book_id]['page']}',
                                            callback_data=f'{book_id}del'))
        
    kb_builder.row(InlineKeyboardButton(text=LEXICON['cancel'],
                                        callback_data='cancel'))

    return kb_builder.as_markup()