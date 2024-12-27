from copy import deepcopy

from aiogram import Router, F
from aiogram.filters import Command, CommandStart,StateFilter
from aiogram.types import Message, CallbackQuery
from database.database import user_dict_template, users_dp
from filters.filters import  IsDelBookmarkCallbackData
from keyboards.pagination_kb import create_pagination_keyboard
from keyboards.bookmarks_kb import create_bookmarks_keyboard,create_edit_keyboard
from keyboards.other_keyboards import create_choice_genres,create_choice_book
from lexicon.lexicon import LEXICON
from services.file_handling import book, get_books_by_genre, prepare_book, get_books_by_genre, author_book

import os,sys
import uuid

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup

class FSMFillForm(StatesGroup):
    choice_genre = State()      
    choice_book = State()
    switch_bk = State()



router = Router()

@router.message(CommandStart())
async def start_command(msg: Message):
    await msg.answer(text=LEXICON['/start'], reply_markup=create_choice_genres(*LEXICON['genres']))
    if msg.from_user.id not in users_dp:
        users_dp[msg.from_user.id] = deepcopy(user_dict_template)
    
@router.callback_query(F.data == 'cancel')
async def cancel_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Список Твоих ЖАНРОВ 📖',reply_markup=create_choice_genres(*users_dp[callback.from_user.id]['genres']))
    await state.set_state(FSMFillForm.choice_genre)


@router.callback_query(F.data.in_(['Фантастика','Фэнтези','Детектив','Романтика','Приключения','Исторический роман','Научная литература','Литература для молодежи','Поэзия']), StateFilter(FSMFillForm.choice_genre))
async def send_books(callback: CallbackQuery, state: FSMContext):
    genre = callback.data
    users_dp[callback.from_user.id]['current_genere'] = genre
    books_author_list = get_books_by_genre(genre)
    await callback.message.answer(text=f"Книги в жанре {genre}:", reply_markup=create_choice_book(*books_author_list))
    await state.set_state(FSMFillForm.choice_book)


@router.callback_query(F.data.in_(['Фантастика','Фэнтези','Детектив','Романтика','Ужасы','Приключения','Исторический роман','Научная литература','Литература для молодежи','Поэзия']))
async def add_ganre_bd(callback: CallbackQuery):
    users_dp[callback.from_user.id]['genres'].add(callback.data)
    await callback.answer(f'Жанр {callback.data} добавлен!')



@router.callback_query(F.data == 'list_genre')
async def switch_main_menu(callback: CallbackQuery, state:FSMContext):
    await callback.message.edit_text(text=LEXICON['/choice_genre'], reply_markup=create_choice_genres(*users_dp[callback.from_user.id]['genres']))
    await state.set_state(FSMFillForm.choice_genre)



@router.callback_query(StateFilter(FSMFillForm.choice_book))
async def open_book(callback: CallbackQuery, state: FSMContext):
    try:
        users_dp[callback.from_user.id]['current_author'] = ''
        users_dp[callback.from_user.id]['cuurent_title'] = ''
        users_dp[callback.from_user.id]['page'] = 1
        bookes = f'{callback.data}.txt'
        current_genre = users_dp[callback.from_user.id]['current_genere']
        path = os.path.join(sys.path[0], 'book', current_genre, bookes)
        if not os.path.exists(path):
            await callback.message.answer(text='Файл не найден')
            return
        prepare_book(path)
        text=book[users_dp[callback.from_user.id]['page']]
        author_name = author_book(path)
        users_dp[callback.from_user.id]['current_author'] = author_name[0]
        users_dp[callback.from_user.id]['cuurent_title'] = author_name[1]
        await callback.message.edit_text(text=text, reply_markup=create_pagination_keyboard('backward',
                                                                       f'{users_dp[callback.from_user.id]['page']}/{len(book)}',
                                                                       'forward'))
    except Exception as e:
        print(f"Ошибка: {e}")
        await callback.message.answer(text='Перезапустите бота /start если книга не открылась')
    finally:
        await state.set_state(default_state)


@router.callback_query(F.data == 'forward')
async def forward_callback(callback: CallbackQuery):
    if users_dp[callback.from_user.id]['page'] < len(book):
        users_dp[callback.from_user.id]['page'] += 1
        text = book[users_dp[callback.from_user.id]['page']]
        await callback.message.edit_text(text=text, reply_markup=create_pagination_keyboard('backward',
                                                                                            f'{users_dp[callback.from_user.id]['page']}/{len(book)}',
                                                                                            'forward'))
        
    else: await callback.answer()

@router.callback_query(F.data == 'backward')
async def backward_callback(callback: CallbackQuery):
    if users_dp[callback.from_user.id]['page'] > 1:
        users_dp[callback.from_user.id]['page'] -= 1
        text = book[users_dp[callback.from_user.id]['page']]
        await callback.message.edit_text(text=text,reply_markup=create_pagination_keyboard('backward',
                                                                                           f'{users_dp[callback.from_user.id]['page']}/{len(book)}',
                                                                                           'forward'))
    else: await callback.answer()



@router.message(Command(commands='help'))
async def help_command(msg: Message):
    await msg.answer(text=LEXICON[msg.text])

@router.message(Command(commands='bookmarks'))
async def bookmarks_command(msg: Message, state: FSMContext):
    if users_dp[msg.from_user.id]['bookmarks']:
        await msg.answer(text=LEXICON[msg.text], 
                        reply_markup=create_bookmarks_keyboard(msg.from_user.id,**users_dp[msg.from_user.id]['bookmarks']))
        await state.set_state(FSMFillForm.switch_bk)
    else: await msg.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(lambda x: '/' in x.data and x.data.replace('/','').isdigit())
async def add_bookmarks_callback(callback: CallbackQuery):
    add_bookmark(callback.from_user.id,users_dp[callback.from_user.id]['current_author'],users_dp[callback.from_user.id]['current_genere'],users_dp[callback.from_user.id]['cuurent_title'],users_dp[callback.from_user.id]['page'])
    await callback.answer('Страница успешно добавлена в закладки')

def add_bookmark(user_id, author, genre, book_title, page):
    user_data = users_dp[user_id]
    book_id = str(uuid.uuid4())
    user_data['bookmarks'][book_id] ={
        'genre': genre,
        'author': author,
        'title': book_title,
        'page': page
    }
    

    
@router.message(Command(commands='continue'))
async def continue_command(msg: Message):
    try:
        text = book[users_dp[msg.from_user.id]['page']]
        await msg.answer(text=text, reply_markup=create_pagination_keyboard('backward',
                                                                        f'{users_dp[msg.from_user.id]['page']}/{len(book)}',
                                                                        'forward'))
    except Exception:
        await msg.answer(text='Нажмите на кнопу /start')



@router.callback_query(F.data == 'edit_bookmarks')
async def edit_bookmarks_callback(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON[callback.data], reply_markup=create_edit_keyboard(callback.from_user.id,**users_dp[callback.from_user.id]['bookmarks']))

@router.callback_query(IsDelBookmarkCallbackData())
async def del_bookmarks_callback(callback: CallbackQuery):
    del users_dp[callback.from_user.id]['bookmarks'][callback.data[:-3]]
    if users_dp[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(text=LEXICON['/bookmarks'], reply_markup=create_edit_keyboard(callback.from_user.id,**users_dp[callback.from_user.id]['bookmarks']))
    else: await callback.message.answer(text=LEXICON['no_bookmarks'])

@router.callback_query(StateFilter(FSMFillForm.switch_bk))
async def switching_bookmarks_callback(callback:CallbackQuery,state: FSMContext):
    users_dp[callback.from_user.id]['page'] = users_dp[callback.from_user.id]['bookmarks'][callback.data]['page']
    users_dp[callback.from_user.id]['current_genere'] = users_dp[callback.from_user.id]['bookmarks'][callback.data]['genre']
    users_dp[callback.from_user.id]['current_author'] = users_dp[callback.from_user.id]['bookmarks'][callback.data]['author']
    users_dp[callback.from_user.id]['cuurent_title'] = users_dp[callback.from_user.id]['bookmarks'][callback.data]['title']
    genre = users_dp[callback.from_user.id]['bookmarks'][callback.data]['genre']
    title = f'{users_dp[callback.from_user.id]['bookmarks'][callback.data]['title']}.txt'
    path = os.path.join(sys.path[0], 'book', genre, title)
    prepare_book(path)
    text = book[users_dp[callback.from_user.id]['bookmarks'][callback.data]['page']]
    await state.set_state(default_state)
    await callback.message.edit_text(text=text, reply_markup=create_pagination_keyboard('backward',
                                                                    f'{users_dp[callback.from_user.id]['bookmarks'][callback.data]['page']}/{len(book)}',
                                                                    'forward'))
    


