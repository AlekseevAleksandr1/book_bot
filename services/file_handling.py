import os
import sys

PAGE_SIZE = 1050

znak_prepin = [',', '.', '!',':',';','?']
def _get_part_text(text: str, start: int, size: int) -> tuple[str,int]:
    str_split = list(text[start:size+start])
    for i in range(len(str_split)-1,-1,-1):
        if str_split[i] in znak_prepin:
            if i > 0 and str_split[i-1] in znak_prepin:
                if str_split[i-2] in znak_prepin:
                    str_split[i] = ''
                    str_split[i-1] = ''
                    str_split[i-2] = ''
                    continue
                return ''.join(str_split[:i+1]), len(str_split[:i+1])
            return  ''.join(str_split[:i+1]), len(str_split[:i+1])
    return '', 0



book: dict[int, str] = {}


def prepare_book(path: str) -> None:
    book.clear()
    number_stran = 1
    with open(path, 'r', encoding='utf-8') as file:
        open_file = file.read()
        current = 0
        while current < len(open_file):
            text, lenght = _get_part_text(open_file,current,PAGE_SIZE)
            if text and lenght != 0:
                book[number_stran] = text.strip()
                current += lenght
                number_stran += 1
            else: break



#prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))



def get_books_by_genre(genre):
    genre_path = os.path.join(sys.path[0],'book', genre)
    if not os.path.exists(genre_path):
        return ["Нет доступных книг в этом жанре."]
    
    books = []
    for filename in os.listdir(genre_path):
        if filename.endswith('.txt'):
            with open(os.path.join(genre_path, filename), 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    author_name = lines[0].strip()  
                    book_title = lines[1].strip()  
                    books.append([author_name,book_title])
    return books


def author_book(path):
    author_book = []
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if len(lines) >= 2:
            author_name = lines[0].strip()  
            book_title = lines[1].strip()  # Предполагаем, что первая строка — это название книги
            author_book.append(author_name)
            author_book.append(book_title)
    return author_book





