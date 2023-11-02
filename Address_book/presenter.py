"""
Presenter (MVP-pattern) for address book.

1. Generates system link to temp folder.
2. Gets path to address book from user, stores it to temp file in temp folder.
3. Generates .txt file (book) at the path entered by user.
4. User can fill the book with his own records and manipulate them further.
"""
from model_book import *

tmp_dir = tmp_dir_checker()
book_path = setting(tmp_dir)
print('\n' + 'Path to the book is {0}'.format(book_path).replace('\\\\', '\\') + '\n')
while True:
    command = choosing_action()
    if command == 'exit':
        print('Bye bye!')
        break
    apply_action(command, book_path)
