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


def tmp_dir_checker():
    """Returns system folder for temporary files"""

    tmp_path = tempfile.gettempdir()
    return tmp_path


def setting(tmp_path):
    """Start of interaction with user.

     User enter a path for address book. This path is saved to .txt file in temp folder
     """

    print('\nHello, user. This is your personal address book.\
    All files will be contained in the path you selected.\n')

    tmp_path = tmp_path + os.sep + 'path_to_book.txt'
    # checking of creation of .txt file for path to the book
    if not os.path.isfile(tmp_path):
        file = open(tmp_path, 'w')
        file.close()
    # reading path to the book
    file = open(tmp_path, 'r')
    path = file.read()
    file.close()
    # if .txt have a valid path checks existence of the book
    if os.path.exists(path):
        check = open(path, 'r')
        check.close()
    # if .txt is empty user creates new path to it
    else:
        path = input('Enter usable path for address book in format:\
                        \n      "C:\\files\\...\\folder_for_book" - example for Windows\
                        \n      "/home/user/.../docs/folder_for_book" - example for UNIX\
                        \n      "/Users/User/.../folder_for_book" - example for Mac OS\n')
        path = path + os.sep + 'address_book.txt'
        book = open(path, 'w')
        book.close()
        if os.name == 'nt':
            path = path.replace('\\', '\\\\')
    file = open(tmp_path, 'w')
    file.write(path)
    return path


def choosing_action():
    """User choose action for execution"""
    command_list = ['search', 'preview', 'add', 'edit', 'remove', 'exit']
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


def word_check(phrase):
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
            return 1
    return 0


def decoding(file, key=''):
    """Decode file.

    Find record(s) consisting key string. If key string is empty will output all records.
    Returns count of records in file.
    """
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
    if temp is None:
        temp = []
    print('\nAddition is selected\n')
    if repeat == 0:
        file = open(path, 'r')
        temp = file.readlines()
        file.close()
    name = word_check('Enter a name for new contact (spaces allowed)\n')
    address = word_check('Enter an address for new contact\n')
    phone = word_check('Enter a phone number for new contact\n')
    temp.append('#'.join([name, address, phone]) + '\n')
    # User's option to repeat
    answer = input('\nWould you like to add one more person to address book? (y/n)\n')
    if answer == 'y' or answer == 'Y':
        add(path, 1, temp)
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
    variants = ['n', 'a', 'p', 'all']
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
        corr_record[0] = word_check('Enter new name for this contact (spaces allowed)\n')
        corr_record[1] = word_check('Enter new address for this contact\n')
        corr_record[2] = word_check('Enter new phone number for this contact\n')
    else:
        num = variants.index(answer)
        prop_name = ['name', 'address', 'phone']
        corr_record[num] = word_check('Write a new ' + prop_name[num] + '\n')
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
    print('Note № {0} was removed from the book'.format(del_number))
    # User's option to repeat
    answer = input('Do you want to remove one more record from file? (y/n)\n\n')
    if answer == 'y' or answer == 'Y':
        remove(path)
    else:
        return
