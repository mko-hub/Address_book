"""
This is a model (MVP-pattern) for address book.

List of functions:
- tmp_dir_checker
- setting
- choosing_action (interact with user)
- apply_action
- word_check
- number_check
- decoding
- search
- preview
- add
- edit
- remove
 """
import tempfile
import os

command_list = ('search', 'preview', 'add', 'edit', 'remove', 'exit')

def tmp_dir_checker():
    """Returns system folder for temporary files"""

    tmp_path = tempfile.gettempdir()
    return tmp_path


def setting(tmp_path):
    """Start of interaction with user.

     User enters a path for address book. This path is saved to .txt file in temp folder
     """

    print('\nHello, user. This is your personal address book.\
    All files will be contained in the path you selected.\n')

    tmp_path = os.path.join(tmp_path, 'path_to_book.txt')
    # checking of creation of .txt file for path to the book
    if not os.path.isfile(tmp_path):
        with open(tmp_path, 'w') as file:
            pass
    # reading path to the book
    with open(tmp_path, 'r') as file:
        path = file.read()
    # if .txt have a valid path checks existence of the book
    if os.path.exists(path):
        with open(path, 'r') as file:
            pass
    # if .txt is empty user creates new path to it
    else:
        while not os.path.exists(path):
            path = input('Enter usable path for address book in format:\
                    \n      "C:\\files\\...\\folder_for_book" - example for Windows\
                    \n      "/home/user/.../docs/folder_for_book" - example for UNIX\
                    \n      "/Users/User/.../folder_for_book" - example for Mac OS\n')
        path = os.path.join(path, 'address_book.txt')
        print(path)
        with open(path, 'w') as file:
            pass
    with open(tmp_path, 'w') as file:
        file.write(path)
    return path


def choosing_action():
    """User choose action for execution"""

    command = ''
    while command not in command_list:
        if len(command) > 0:
            print('Command not recognized.\n')
        command = input('Choose action: \n- write "search" to search \
                                        \n- write "preview" to print all notes \
                                        \n- write "add" to add new note \
                                        \n- write "edit" to edit notes in the book \
                                        \n- write "remove" to remove note from the book \
                                        \n- write "exit" to exit the program\n')
    return command


def apply_action(command, path):
    """Converts string name of function in call of function"""

    text = command + "('" + path + "')"
    return exec(text)


def check_word(phrase):
    """Function checks separation symbol and emptiness in string"""

    word = input(phrase)
    while '#' in word or len(word) == 0:
        word = input(phrase)
    return word


def number_check(number, max_number):
    """Checks string's properties: is it digit and is it less than max_number"""

    if number.isdigit():
        number = int(number)
        if 1 <= number <= max_number:
            return True
    return False


def decoding(file, key=''):
    """Decode file.

    Find record(s) consisting key string. If key string is empty will output all records.
    Returns count of records in file."""

    file = file.readlines()
    count = 0
    search_count = 0
    for line in file:
        count += 1
        if key in line:
            search_count += 1
            line = line.split(sep='#')
            print(count, end='. ')
            print('name: ' + line[0])
            print('   address: ' + line[1])
            print('   phone: ' + line[2])
    print('')
    if search_count == 0 and key != '':
        print('There are no records with entered sequence of characters.')
    return count


def search(path):
    """Searches for a record in book using key symbols"""

    print('\nSearch is selected\n')
    key = input('Enter a sequence of characters to search a record containing them\n')
    list_of_records = open(path, 'r')
    count = decoding(list_of_records, key)
    list_of_records.close()
    # Empty book case
    if count == 0:
        print('There is no notes in address book, choose "add" to add some.\n\n')
        return
    # User's option to repeat
    answer = input('Do you want to search something else? (y/n)\n')
    if answer == 'y' or answer == 'Y':
        search(path)
    else:
        return


def preview(path):
    """Prints all records of the book"""

    print('\nListing is selected\n')
    print('List of all notes in address book:\n')
    file = open(path, 'r')
    count = decoding(file)
    if count == 0:
        print('There is no notes in address book, choose "add" to add some.\n\n')
    file.close()
    return


def add(path, repeat=0, temp=None):
    """Adds new record(s) to the book"""
    print(path)
    if temp is None:
        temp = []
    print('\nAddition is selected\n')
    if repeat == 0:
        with open(path, 'r') as file:
            temp = file.readlines()
    name = check_word('Enter a name for new contact (spaces allowed)\n')
    address = check_word('Enter an address for new contact\n')
    phone = check_word('Enter a phone number for new contact\n')
    temp.append('#'.join([name, address, phone]) + '\n')
    # User's option to repeat
    answer = input('\nWould you like to add one more person to address book? (y/n)\n')
    if answer == 'y' or answer == 'Y':
        add(path, 1, temp)  # хорошо, что рекурсия освоена, но для улучшения читаемости лучше от неё избавиться
                                   # и переделать в обычную функцию. При рекурсии есть риск переполнения стека
    else:
        file = open(path, 'w')
        for record in temp:
            file.write(record)
        file.close()
        return


def edit(path):
    """Function corrects selected note"""

    print('\nCorrection is selected\n')
    # preview of records for user
    file = open(path, 'r')
    count = decoding(file)
    file.close()
    # Empty book case
    if count == 0:
        print('There is no notes in address book, choose "add" to add some.\n\n')
        file.close()
        return
    file = open(path, 'r')
    temp = file.readlines()
    # selection of record for editing (unwrapped book)
    number = ''
    while not number_check(number, count):
        number = input('Enter a number of record to start its correction\n')
    number = int(number)
    corr_record = temp[number - 1]
    corr_record = corr_record.split(sep='#')
    print('name: ' + corr_record[0])
    print('address: ' + corr_record[1])
    print('phone: ' + corr_record[2])
    # selection of record part for editing
    variants = ['n', 'a', 'p', 'all']  # вынести константные команды
    answer = ''
    while answer not in variants:
        if len(answer) > 0:
            print('Command not recognized.')
        answer = input('Choose property of record to correct it:\
                       \nn - for name edit\
                       \na - for address edit\
                       \np - for phone edit\
                       \nall - for full record edit\n')
    if answer == 'all':
        corr_record[0] = check_word('Enter new name for this contact (spaces allowed)\n')
        corr_record[1] = check_word('Enter new address for this contact\n')
        corr_record[2] = check_word('Enter new phone number for this contact\n')
    else:
        num = variants.index(answer)
        prop_name = ['name', 'address', 'phone']
        corr_record[num] = check_word('Write a new ' + prop_name[num] + '\n')
    # writing edited record into file with all others
    temp[number - 1] = '#'.join(corr_record)
    print('new name: ' + corr_record[0])
    print('new address: ' + corr_record[1])
    print('new phone: ' + corr_record[2] + '\n')
    file.close()
    file = open(path, 'w')
    for line in temp:
        file.write(line)
    file.close()
    # User's option to repeat
    # Повторяемый из другой функции блок с репитом команды, стоит её вынести в общую функцию
    answer = input('Do you need to correct something else? (y/n)\n')
    if answer == 'y' or answer == 'Y':
        edit(path)
    else:
        return


def remove(path):
    """Removes note from the book by its number"""

    print('\nRemoval is selected\n')
    # printing list of notes in the book
    file = open(path, 'r')
    count = decoding(file)
    file.close()
    if count == 0:
        print('There is no notes in address book, choose "add" to add some.\n\n')
        return
    # checking user's intention before removing
    while True:
        answer = input('Are you sure you want to delete any record? (y/n)\n')
        if answer == 'y' or answer == 'Y':
            break
        elif answer == 'n' or answer == 'N':
            return
    # selection of exact note for removing
    del_number = ''
    while not number_check(del_number, count):
        del_number = input('Enter a valid number of note to delete it from book\n')
    del_number = int(del_number)
    # removing
    file = open(path, 'r')
    temp = file.readlines()
    file.close()
    temp.pop(del_number - 1)
    file = open(path, 'w')
    for line in temp:
        file.write(line)
    file.close()
    # Конкатенацию и форматирование строк можно заменить на f-строки
    print(f'Note № {del_number} was removed from the book')
    # User's option to repeat
    answer = input('Do you want to remove one more record from file? (y/n)\n\n')
    if answer == 'y' or answer == 'Y':
        remove(path)
    else:
        return

