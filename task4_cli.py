def parse_input(user_input: str) -> tuple[str, ...]:
    
    
    parts = user_input.strip().split() # Розділення вводу на команду та аргументи

    if not parts:
        return "", [] # Захист від орожного вводу
        
    cmd, *args = parts
    cmd = cmd.lower() # Команди не чутливі до регістру
   
    ''' debug print
    # Для тестування виводимо команду та аргументи
    test_user_input = f"--- User Command: {cmd}" + (f", Arguments: {args}" if args else "")    
    print(test_user_input) 
    '''    
    return cmd, *args 

def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    '''add <name> <phone> — додати новий контакт'''

    if len(args) != 2: # Перевірка на коректну кількість аргументів
        return "Usage: add <name> <phone>"
    name, phone = args
#    if name in contacts:
#        return f"Contact '{name}' already exists."
    contacts[name] = phone
    return "Contact added."

def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    """change <name> <new_phone> — змінити номер телефону існуючого контакту"""
    if len(args) != 2:
        return "Usage: change <name> <new_phone>"
    name, phone = args
    if name not in contacts:
        return "Contact not found."
    contacts[name] = phone
    return "Contact updated."

def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    """phone <name> — показати номер телефону для вказаного контакту"""
    if len(args) != 1:
        return "Usage: phone <name>"
    name = args[0]
    if name not in contacts:
        return "Contact not found."
    return contacts[name]

def show_all(contacts: dict[str, str]) -> str:
    """all — вывести все контакты"""
    if not contacts:
        return "No contacts."
    # Формат: по одному на строку
    lines = [f"{name}: {phone}" for name, phone in contacts.items()]
    return "\n".join(lines)

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

        # Обробка команд
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
            continue  # Ігноруємо порожній ввід
        elif command == "help":
            print(help_command())
        else:
            print("Invalid command.")
            print(help_command()) # Не відома команда, показуємо допомогу

if __name__ == "__main__":
    main()
