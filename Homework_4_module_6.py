from collections import UserDict
import re
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field): # клас ім'я
    def __init__(self, value):
        if not value:
            raise ValueError("Ім'я обов'язкове.")
        super().__init__(value)

class Phone(Field): # клас телефон
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Номер повинен мати 10 цифр")
        super().__init__(value)

    @staticmethod
    def is_valid_phone(value):
        return bool(re.match(r'^\d{10}$', value))

class Record: # клас запис
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number): # додавання телефону
        self.phones.append(Phone(phone_number))

    def remove_phone (self, phone_number): # видалення телефону
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return
            raise ValueError("Телефон не було знайдено")

    def edit_phone (self, old_number, new_number): # зміна телефону
        self.remove_phone(old_number)
        self.add_phone(new_number)

    def find_phone(self, phone_number): # знайти телефон
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict): # клас сама книжка
    def add_record(self, record): # додавання телефону у книзі
        self.data[record.name.value] = record

    def find(self, name): # знаходження телефону у книзі
        return self.data.get(name)

    def delete(self, name): # видалення телефону у книзі
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Запис не знайдено.")

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

# Створення тестової адресної книги
if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print(book)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    book.delete("Jane")