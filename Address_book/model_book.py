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
variants = {'n': ['name', 0], 'a': ['address', 1], 'p': ['phone', 2],
            'all': ''}


def tmp_dir_checker():
    """Returns system folder for temporary files"""

    tmp_path = tempfile.gettempdir()
    return tmp_path


def setting(tmp_path):
    """Start of interaction with user.

     User enters a path for address book.
     This path is saved to .txt file in temp folder
     """

    print('\nHello, user. This is your personal address book.\
    \nAll files will be contained in the path you selected.\n')

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
        command = input('Choose action: \
                        \n- write "search" to search \
                        \n- write "preview" to print all notes \
                        \n- write "add" to add new note \
                        \n- write "edit" to edit notes in the book \
                        \n- write "remove" to remove note from the book \
                        \n- write "exit" to exit the program\n').lower()
    return command


def apply_action(command, path):
    """Converts string name of function in call of function"""

    text = command + "(r'" + path + "')"
    return exec(text)


def check_word(phrase):
    """Function checks separation symbol and emptiness in string"""

    word = input(phrase)
    while '#' in word or len(word) == 0:
        word = input(phrase)
    return word


def number_check(number, max_number):
    """Checks string's properties:
    1) is it digit; 2) is it less than max_number.
    """

    if number.isdigit():
        number = int(number)
        if 1 <= number <= max_number:
            return True
    return False


def decoding(file, key=''):
    """Decode file.

    Find record(s) consisting key string.
    If key string is empty will output all records.
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
            print(f'name: {line[0]}')
            print(f'   address: {line[1]}')
            print(f'   phone: {line[2]}')
    print('')
    if search_count == 0 and key != '':
        print('There are no records with entered sequence of characters.')
    return count


def search(path):
    """Searches for a record in book using key symbols"""

    print('\nSearch is selected\n')
    key = input('Enter a sequence of characters to search a record' +
    ' containing them\n')
    with open(path, 'r') as list_of_records:
        count = decoding(list_of_records, key)
    # Empty book case
    if count == 0:
        print('There are no notes in address book, choose "add" to add some.\
        \n\n')
        return
    # User's option to repeat
    answer = input('Do you want to search something else? (y/n)\n').lower()
    if answer == 'y':
        search(path)
    else:
        return


def preview(path):
    """Prints all records of the book"""

    print('\nListing is selected\n')
    print('List of all notes in address book:\n')
    with open(path, 'r') as file:
        count = decoding(file)
        if count == 0:
            print('There are no notes in address book,',
            'choose "add" to add some.\n\n')
    return


def add(path, repeat=0, temp=None):
    """Adds new record(s) to the book"""
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
    answer = input('\nWould you like to add one more person to book? (y/n)\
    \n').lower()
    if answer == 'y':
        add(path, 1, temp)
    else:
        with open(path, 'w') as file:
            for record in temp:
                file.write(record)
        return


def edit(path):
    """Function corrects selected note"""

    print('\nCorrection is selected\n')
    # preview of records for user
    with open(path, 'r') as file:
        count = decoding(file)
        file.seek(0, 0)
        temp = file.readlines()
    # empty book case
    if count == 0:
        print('There are no notes in the book, choose "add" to add some.\n\n')
        return
    # selection of a record for editing (unwrapped book)
    number = ''
    while not number_check(number, count):
        number = input('Enter a number of record to start its correction\n')
    number = int(number)
    corr_record = temp[number - 1].split(sep='#')
    print(f'name: {corr_record[0]}')
    print(f'address: {corr_record[1]}')
    print(f'phone: {corr_record[2]}')
    # selection of record part for editing
    answer = ''
    while answer not in variants:
        if len(answer) > 0:
            print('Command not recognized.\n')
        answer = input('Choose property of record to correct it:\
                       \nn - for name edit\
                       \na - for address edit\
                       \np - for phone edit\
                       \nall - for full record edit\n').lower()
    if answer == 'all':
        corr_record[0] = check_word('Enter new name for this contact \
        (spaces allowed)\n')
        corr_record[1] = check_word('Enter new address for this contact\n')
        corr_record[2] = check_word('Enter new phone number for this \
        contact\n')
    else:
        param = variants[answer]
        corr_record[param[1]] = check_word(f'Write a new {param[0]}:\n')
    # writing edited record into file with all others
    temp[number - 1] = '#'.join(corr_record)
    print(f'New name: {corr_record[0]}')
    print(f'New address: {corr_record[1]}')
    print(f'New phone: {corr_record[2]}\n')
    with open(path, 'w') as file:
        for line in temp:
            file.write(line)
    # User's option to repeat
    answer = input('Do you need to correct something else? (y/n)\n').lower()
    if answer == 'y':
        edit(path)
    else:
        return


def remove(path):
    """Removes note from the book by its number"""

    print('\nRemoval is selected\n')
    # printing list of notes in the book
    with open(path, 'r') as file:
        count = decoding(file)
    if count == 0:
        print('There are no notes in address book, choose "add" to add some.\
        \n\n')
        return
    # checking user's intention before removing
    while True:
        answer = input('Are you sure you want to delete any record? (y/n)\
        \n').lower()
        if answer == 'y':
            break
        elif answer == 'n':
            return
    # selection of exact note for removing
    del_number = ''
    while not number_check(del_number, count):
        del_number = input('Enter a valid note number to delete it from book\
        \n')
    del_number = int(del_number)
    # removing
    with open(path, 'r') as file:
        temp = file.readlines()
    temp.pop(del_number - 1)
    with open(path, 'w') as file:
        for line in temp:
            file.write(line)
    print(f'Note № {del_number} was removed from the book.')
    # User's option to repeat
    answer = input('Do you want to remove one more record from file? (y/n)\
    \n\n').lower()
    if answer == 'y':
        remove(path)
    else:
        return
