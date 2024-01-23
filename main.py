from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_phone()

    def validate_phone(self):
        if not self.value.isdigit() or len(self.value) != 10:
            raise ValueError

    def __str__(self):
        return str(self.value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                phone.validate_phone()
                found = True
                break

        if not found:
            raise ValueError

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Name: {self.name.value}, phones: {', '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params"
        except KeyError:
            return f"There is no contact such in phone book."
        except ValueError:
            return "Not enough params or wrong phone format"

    return inner
    
@input_error
def func_help():
    return ('Hi! If you want to start working, just enter "hello"\n' +
            'Number phone in 10 numbers, for example 0001230001\n' +
            'The representation of all commands looks as follows:\n' +
            '"hello" - start work with bot\n' +
            '"add" name phone\n' +
            '"change" name phone\n' +
            '"phone" name\n' +
            '"show all" - for show all information\n' +
            '"good bye", "close", "exit" - for end work\n'+
            '"del" - delete info of name')

@input_error
def parser(user_input: str):
    COMMANDS = {
        "Hello": func_hello,
        "Add ": func_add,
        "Change ": func_change,
        "Phone ": func_search,
        "Show All": func_show_all,
        "Del ": func_delete
    }

    user_input = user_input.title()

    for kw, command in COMMANDS.items():
        if user_input.startswith(kw):
            return command, user_input[len(kw):].strip().split()
    return func_unknown_command, []

@input_error
def func_add(*args):
    name = args[0]
    record = Record(name)
    phone_numbers = args[1:]
    for phone_number in phone_numbers:
        record.add_phone(phone_number)
    address_book.add_record(record)
    return "Info saved successfully."

@input_error
def func_change(*args):
    name = args[0]
    phone_numbers = args[1:]
    record = address_book.find(name)
    if record:
        for phone in phone_numbers:
            record.func_edit_phone(phone, phone)
        return "Info saved successfully."
    else:
        raise KeyError

@input_error
def func_delete(*args):
    name = args[0]
    address_book.delete(name)
    return f"User {name} has been deleted from the phone book"

@input_error
def func_search(*args):
    name = args[0]
    record = address_book.find(name)
    if record:
        return str(record)
    else:
        raise KeyError

@input_error
def func_show_all(*args):
    return str(address_book)

@input_error
def func_unknown_command():
    return "Unknown command. Try again."

@input_error
def func_hello():
    return "How can I help you?"
@input_error
def func_quit():
    return "Good bye!"

address_book = AddressBook()

def main():
    print(func_help())

    while True:
        user_input = input('Please, enter the valid command: ')

        if user_input.lower() in ["exit", "close", "good bye"]:
            print(func_quit())
            break
        else:
            handler, arguments = parser(user_input)
            print(handler(*arguments))

if __name__ == '__main__':
    main()
