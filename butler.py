import pickle
import re
from collections import UserDict
from datetime import datetime
from copy import deepcopy


class Name():
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f'{self.name}'


class Address():
    def __init__(self, address: str) -> None:
        self.address = address

    def __str__(self) -> str:
        return f'{self.address}'


class Phone():
    def __init__(self, phone: str) -> None:
        self.phone = phone

    def __str__(self) -> str:
        return f'{self.phone}'


class Email():
    def __init__(self, email: str) -> None:
        self.email = email

    def __str__(self) -> str:
        return f'{self.email}'


class Birthday():
    def __init__(self, birthday: str) -> None:
        self.birthday = birthday

    def __str__(self) -> str:
        return f'{self.birthday}'


class Hashtag():
    def __init__(self, hashtag: str) -> None:
        self.hashtag = hashtag

    def __str__(self) -> str:
        return f'{self.hashtag}'


class Note():
    def __init__(self, note: str) -> None:
        self.note = note

    def __str__(self) -> str:
        return f'{self.note}'


class Record:
    def __init__(self, name: Name, address: Address = None, phone: Phone = None, email: Email = None, birthday: Birthday = None):
        self.name = name

        self.address = address
        if address is not None:
            self.add_address(address)

        self.phones = []
        if phone is not None:
            self.add_phone(phone)

        self.email = email
        if email is not None:
            self.add_email(phone)

        self.birthday = birthday
        if email is not None:
            self.add_email(phone)

    def add_address(self, address: Address):
        self.address = address

    def add_phone(self, phone: Phone | str):
        if isinstance(phone, str):
            phone = self.create_phone(phone)
        self.phones.append(phone)

    def add_email(self, email: Email):
        self.email = email

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def create_phone(self, phone: str):
        return Phone(phone)

    def show(self):         # returns phones in beautiful formating
        if self.phones:
            result = ''
            for inx, p in enumerate(self.phones):
                result += f' {inx+1}: {p}'
        else:
            result = None
        return result

    def __str__(self) -> str:
        return f'Contact Name: {self.name},\nAddress: {self.address},\nPhones: {self.show()},\nEmail: {self.email},\nBirthday: {self.birthday}\n'


class Notice:
    def __init__(self, hashtag: Hashtag, note: Note = None):

        self.hashtag = hashtag

        self.notes = []
        if note is not None:
            self.add_note(note)

    def add_hashtag(self, hashtag: Hashtag):
        self.hashtag = hashtag

    def add_note(self, note: Note | str):
        if isinstance(note, str):
            note = self.create_note(note)
        self.notes.append(note)

    def create_note(self, note: str):
        return Note(note)

    def show(self):         # returns notes in beautiful formating
        if self.notes:
            result = ''
            for inx, n in enumerate(self.notes):
                result += f' {inx+1}: {n}'
        else:
            result = None
        return result

    def __str__(self) -> str:
        return f'Hashtag: {self.hashtag},\nNotes: {self.show()}\n'


class AddressBook(UserDict):

    def __init__(self, record: Record | None = None, notice: Notice | None = None) -> None:
        self.records = {}
        if record is not None:
            self.add_record(record)

        self.notes = {}
        if notice is not None:
            self.add_notice(notice)

    def add_record(self, record: Record):
        self.records[record.name] = record

    def add_notice(self, notice: Notice):
        self.notes[notice.hashtag] = notice

    def iterator(self, N, essence):
        counter = 0
        result = f'\nPrinting {N} records'
        for item, record in self.essence.items():
            result += f'\n{str(record)}'
            counter += 1
            if counter >= N:
                yield result
                counter = 0
                result = f'\nPrinting next {N} records'

    def __str__(self) -> str:
        return '\n'.join(str(record) for record in self.records.values())

    def __deepcopy__(self, memodict={}):
        copy_ab = AddressBook(self, self.records, self.notes)
        memodict[id(self)] = copy_ab
        for el in self.records:
            copy_ab.append(deepcopy(el, memodict))
        for el in self.notes:
            copy_ab.append(deepcopy(el, memodict))
        return copy_ab


address_book = AddressBook()


def copy_class_addressbook(address_book):
    return deepcopy(address_book)


def unknown_command(command: str) -> str:
    return f'\nUnknown command "{command}"'


def hello_user() -> str:
    return '\nHow can I help you?\n'


def exit_func() -> str:
    a = input('Would you like to save changes (Y/N)? ')
    if a == 'Y' or a == 'y':
        print(saver())
    return 'Goodbye!'


def contact_adder() -> str:
    name = input('Enter contact name (obligatory field): ')
    if name in address_book.records.keys():
        return f'Contact {name} already exists'

    record = Record(Name(name))

    address = input('Enter address or press Enter to skip: ')
    if address:
        record.add_address(address)

    phone = input('Enter phone (ex. +38(099)9119119) or press Enter to skip: ')
    if phone:
        record.add_phone(phone)

    email = input('Enter email or press Enter to skip: ')
    if email:
        record.add_email(email)

    birthday = input(
        'Enter birthday (ex. 2023.12.25) or press Enter to skip: ')
    if birthday:
        record.add_birthday(birthday)

    address_book.add_record(record)

    return f'\nAdded {record}'


def show_all_contacts() -> str:
    if address_book.records:
        N = int(input('How many contacts to show? '))
        if N < 1:
            return 'Input cannot be less that 1'
        elif N >= len(address_book.records):
            result = '\nPrintting all records:\n'
            for key, value in address_book.records.items():
                result += f'\n{value}'
            result += '\nEnd of address book\n'
            return result
        else:
            iter = address_book.iterator(N, address_book.records)
            for i in iter:
                print(i)
                input('Press any key to continue: ')
            if len(address_book.records) % 2 == 0:
                return '\nEnd of address book\n'
            else:
                return f'{str(list(address_book.records.values())[-1])}\nEnd of address book\n'
    else:
        return 'No contacts, please add\n'


def saver() -> str:
    if address_book.records:
        with open('backup.dat', 'wb') as file:
            pickle.dump(address_book, file)
        return '\nAddress Book successfully saved to backup.dat\n'
    else:
        return '\nAddress Book is empty, no data to be saved to file\n'


def loader() -> str:
    try:
        with open('backup.dat', 'rb') as file:
            global address_book
            address_book = pickle.load(file)
        return '\nAddress Book successfully loaded from backup.dat\n'
    except:
        return ''


def helper():
    result = 'List of all supported commands:\n\n'
    for key in commands:
        result += '{:<13} {:<50}\n'.format(key, commands[key][1])
    return result


def note_adder():
    hashtag = input('Enter hashtag for your note (ex. #todo): ')
    if hashtag in address_book.notes.keys():
        return f'Note with hashtag {hashtag} already exists'

    if not hashtag:
        hashtag = '#None'

    notice = Notice(Note(hashtag))

    note = input('Enter note: ')
    if note:
        notice.add_note(note)

    address_book.add_notice(notice)

    return f'\nAdded reccord with {notice}'


def show_all_notes() -> str:
    if address_book.notes:
        N = int(input('How many records to show? '))
        if N < 1:
            return 'Input cannot be less that 1'
        elif N >= len(address_book.notes):
            result = '\nPrintting all records:\n'
            for key, value in address_book.notes.items():
                result += f'\n{value}'
            result += '\nEnd of records\n'
            return result
        else:
            iter = address_book.iterator(N, address_book.notes)
            for i in iter:
                print(i)
                input('Press any key to continue: ')
            if len(address_book.notes) % 2 == 0:
                return '\nEnd of records\n'
            else:
                return f'{str(list(address_book.notes.values())[-1])}\nEnd of records\n'
    else:
        return 'No records, please add\n'


commands = {
    'hello':        (hello_user,            ' -> just greating'),
    'add contact':  (contact_adder,         ' -> adds new contact'),
    '+c':           (contact_adder,         ' -> adds new contact (short command)'),
    'show contacts': (show_all_contacts,    ' -> shows all contacts'),
    '?c':           (show_all_contacts,     ' -> shows all contacts (short command)'),
    'exit':         (exit_func,             ' -> exit from the bot with or without saving'),
    'close':        (exit_func,             ' -> exit from the bot with or without saving'),
    'save':         (saver,                 ' -> saves to file all changes'),
    'load':         (loader,                ' -> loads last version of the Address Book'),
    'help':         (helper,                ' -> shows the list of all supported commands'),
    'add note':     (note_adder,            ' -> adds note with o without hashtag'),
    '+n':           (note_adder,            ' -> adds note with o without hashtag (short command)'),
    'show notes':   (show_all_notes,        ' -> shows all notes'),
    '?n':           (show_all_notes,        ' -> shows all notes (short command)'),
}


def main():
    print(loader())
    while True:
        phrase = input('Please enter command or type "help": ').strip()
        command = None
        for key in commands:
            if phrase.lower() == key:
                command = key
                break

        if not command:
            result = unknown_command(phrase)
        else:
            handler = commands.get(command)[0]
            result = handler()
            if result == 'Goodbye!':
                print(result)
                break
        print(result)


if __name__ == '__main__':
    main()
