from typing import Callable
import functools


def input_error(func: Callable[..., str]) -> Callable[..., str]:
    """
    Обгортає хендлер команди та перехоплює типові помилки введення
    користувача, повертаючи дружні повідомлення замість падіння програми.
    """
    @functools.wraps(func)
    def inner(*args, **kwargs) -> str:
        try:
            return func(*args, **kwargs)

        except KeyError as e:
            name = (e.args[0] if e.args else "").strip() or "<?>"
            return f"Contact '{name}' not found."

        except IndexError:
            return "Enter the argument for the command"

        except ValueError as e:
            msg = (str(e).strip() or "Invalid arguments.")
            return msg

    return inner


def parse_input(user_input: str) -> tuple[str, ...]:
    """
    Повертає кортеж: (команда, *аргументи).
    Порожній ввід → ("", []).
    """
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd, *args = parts
    return cmd.lower(), *args


def help_command() -> str:
    """
    Довідка по доступним командам бота.
    """
    return (
        "Available commands:\n"
        "- hello — greeting\n"
        "- add <name> <phone> — add a new contact\n"
        "- change <name> <new_phone> — update existing contact\n"
        "- phone <name> — show phone number\n"
        "- all — show all contacts\n"
        "- help — show this message\n"
        "- exit / close — quit"
    )


@input_error
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    """
    add <name> <phone> — додати новий контакт.
    ValueError виникне автоматично, якщо args не містить рівно 2 елементи.
    """
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    """
    change <name> <new_phone> — змінити номер існуючого контакту.
    ValueError виникне при неправильній кількості аргументів.
    KeyError виникне при спробі отримати неіснуючий контакт.
    """
    name, new_phone = args
    contacts[name]  # Перевірка існування через доступ до ключа
    contacts[name] = new_phone
    return "Contact updated."


@input_error
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    """
    phone <name> — показати номер телефону контакту.
    IndexError виникне при спробі отримати args[0] з порожнього списку.
    KeyError виникне при доступі до неіснуючого ключа.
    """
    name = args[0]
    return contacts[name]


@input_error
def show_all(contacts: dict[str, str]) -> str:
    """
    all — вивести всі контакти у форматі 'Name: Phone' по одному в рядку.
    Порожній словник → повідомлення 'No contacts.' (це не помилка).
    """
    output = "\n".join(f"{n}: {p}" for n, p in contacts.items())
    return output or "No contacts."


def main():
    """
    Основний цикл
    """
    contacts: dict[str, str] = {}
    print("Welcome to the assistant bot!")
    while True:
        command, *args = parse_input(input("Enter a command: "))

        if command in ("close", "exit"):
            print("Good bye!")
            break

        if command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(show_phone(args, contacts))

        elif command == "all":
            print(show_all(contacts))

        elif command == "help":
            print(help_command())

        elif command == "":
            print("Enter a command or type 'help'.")

        else:
            print(f"Unknown command: '{command}'")
            print(help_command())


if __name__ == "__main__":
    main()
