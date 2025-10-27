from typing import Any, Callable
import functools

def input_error(func: Callable[..., str]) -> Callable[..., str]:
    @functools.wraps(func)
    def inner(*args, **kwargs) -> str:
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            who = e.args[0] if e.args else ""
            return f"Contact '{who}' not found." if who else "Contact not found."
        except ValueError as e:
            return str(e).strip() or "Invalid arguments."
        except IndexError:
            return "Enter the argument for the command"
    return inner

def parse_input(user_input: str) -> tuple[str, ...]:
    parts = user_input.strip().split()  # Розділення вводу на команду та аргументи
    if not parts:
        return "", []  # Захист від порожнього вводу
    cmd, *args = parts
    cmd = cmd.lower()  # Команди не чутливі до регістру
    return cmd, *args

@input_error
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    """add <name> <phone> — додати новий контакт"""
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    """change <name> <new_phone> — змінити номер телефону існуючого контакту"""
    if len(args) != 2:
        raise ValueError("Give me name and NEW phone please.")
    name, phone = args
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    """phone <name> — показати номер телефону для вказаного контакту"""
    if len(args) < 1:
        # Імітуємо типову ситуацію IndexError за ТЗ — недостає аргумента
        raise IndexError
    name = args[0]
    if name not in contacts:
        raise KeyError(name)
    return contacts[name]

@input_error
def show_all(contacts: dict[str, str]) -> str:
    """all — вивести всі контакти"""
    if not contacts:
        return "No contacts."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())

@input_error
def help_command() -> str:
    """help — показати список доступних команд"""
    return (
        "Available commands:\n"
        "- hello\n"
        "- add <name> <phone>\n"
        "- change <name> <new_phone>\n"
        "- phone <name>\n"
        "- all\n"
        "- help\n"
        "- exit / close"
    )

def main():
    contacts: dict[str, str] = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        elif command == "":
            print("Enter a command or type 'help'.")
            continue
        elif command == "help":
            print(help_command())
        else:
            print("Invalid command.")
            print(help_command())  # Показуємо допомогу

if __name__ == "__main__":
    main()
