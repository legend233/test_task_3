from functions import (create_tables, add_book, delete_book, edit_book,
                        add_user, delete_user, edit_user,
                        add_getbook_to_journal, add_returnbook_to_journal,
                        total_count_books, total_count_users,
                        total_count_rent, total_count_notreturn,
                        total_last_date, max_reading_author, top_genres,
                        top_genres_for_users, total_delays, check_db)

from rich.table import Table
from rich.console import Console
from rich import print
from rich.prompt import Prompt, Confirm
import os

console = Console()
count_rows = 10


def utf_valid(new_data):
    return True

def menu_create_tables():
    table = Table(title="БАЗЫ ДАННЫХ НЕ ОБНАРУЖЕНО", show_header=True)
    comands = ["Создать пустую базу", "Создать базу с тестовыми данными"]
    titles = ("#", "Команда")
    for title in titles:
        table.add_column(title, style="cyan", header_style="red")
    for index, comand in enumerate(comands):
        table.add_row(str(index + 1), comand)
    table.add_row("q", "Назад")
    console.print(table, justify="center")
    choice = input("введите # команды: ").lower()
    if choice == "1":
        create_tables()
    elif choice == "2":
        pass
    return None
def menu_start():
    table = Table(title="МЕНЮ", show_header=True)
    comands = ["Добавить/Удалить/Изменить книгу",
                "Добавить/Удалить/Изменить пользователя",
                "Добавить Факт взятия/возврата книги",
                "Просмотр отчетов"]
    titles = ("#", "Команда")
    for title in titles:
        table.add_column(title, style="cyan", header_style="red")
    for index, comand in enumerate(comands):
        table.add_row(str(index + 1), comand)
    table.add_row("q", "Выход")
    console.print(table, justify="center")


def menu_books():
    """Отображает все книги в таблице и вводит команды о редактировании"""
    cur_page = 0
    choice = None
    while True:
        os.system('clear')
        table = Table(title=f"-- Книги -- стр.{cur_page+1}", show_header=True)
        titles = ("id", "Название", "Автор", "Жанр", "последняя\nзапись в журнале")
        for title in titles:
            table.add_column(title, style="cyan", header_style="red")
        books = total_count_books()
        start_p = cur_page*count_rows
        for row in books[start_p:start_p+count_rows]:
            table.add_row(*map(str, row))
        console.print(table, justify="center")

        table_comands = Table()
        titles2 = ("#", "Команда")
        commands = ["Следующая страница", "Предыдущая страница", "Добавить книгу", "Удалить книгу", "Изменить книгу"]
        for title in titles2:
            table_comands.add_column(title, style="cyan", header_style="red")
        for index, comand in enumerate(commands):
            table_comands.add_row(str(index + 1), comand)
        table_comands.add_row("q", "Назад")
        console.print(table_comands, justify="left")
    
        choice = Prompt.ask("введите # команды:", choices=["1", "2", "3", "4", "5", "q"])
        if choice == "1" and (cur_page+1)*count_rows < len(books):
            cur_page += 1
        elif choice == "2" and (cur_page-1)*count_rows >= 0:
            cur_page -= 1
        elif choice == "3":
            book = menu_add_book()
            if book:
                add_book(*book)
        elif choice == "4":
            book_id = menu_delete_book()
            if book_id:
                delete_book(book_id)
        elif choice == "5":
            new_book = menu_edit_book(books)
            if new_book:
                edit_book(*new_book)
        elif choice == "q":
            cur_page = 0
            return ""
        

def menu_add_book():
    os.system('clear')
    console.print("ДОБАВЛЕНИЕ НОВОЙ КНИГИ", style="red")
    console.print("Нажми Enter, чтобы пропустить")
    book = []
    titles = ["Название книги", "Автор", "Жанр"]
    for title in titles:
        new_data = input(f"\rВведите - {title}: ")
        if new_data and utf_valid(new_data):
            book.append(new_data)
        else:
            book.append("None")
    # рисуем табличку
    table = Table()
    for title in titles:
        table.add_column(title, header_style="red")
    table.add_row(*book)
    console.print(table, justify="center")

    if Confirm.ask("Добавить книгу?"):
        return book
    else:
        return None


def menu_delete_book():
    console.print("УДАЛЕНИЕ КНИГИ", style="red")
    console.print("Нажми Enter, чтобы пропустить")

    answer = input(f"Введите ID книги: ")
    while not answer.isdigit() or answer == "":
        print("Неверный ввод. Попробуйте снова.")
        answer = input(f"Введите ID книги: ")
    
    book_id = int(answer)

    if Confirm.ask(f"Удалить книгу с id = {book_id}?"):
        return book_id
    else:
        return None


def menu_edit_book(books):
    console.print("РЕДАКТИРОВАНИЕ КНИГИ", style="red")
    console.print("Нажми Enter, чтобы пропустить")

    answer = input(f"Введите ID книги: ")
    while not answer.isdigit():
        print(f"Неверный ввод: {answer}. Попробуйте снова.")
        answer = input(f"Введите ID книги: ")
    
    if not answer:
        return None

    book_id = answer
    old_book = list(filter(lambda x: x[0] == int(book_id), books))[0]
    new_book = [book_id,]
    titles = ["Название книги", "Автор", "Жанр"]
    for title, old_data in zip(titles, old_book[1:]):
        new_data = input(f"\rВведите - {title}: ")
        if new_data and utf_valid(new_data):
            new_book.append(new_data)
        else:
            new_book.append(old_data)
    # рисуем табличку
    table = Table()
    for title in titles:
        table.add_column(title, header_style="red")
    table.add_row(*new_book[1:])
    console.print(table, justify="center")


    if Confirm.ask("Редактировать книгу?"):
        return new_book
    else:
        return None


def menu_users():
    """Отображает всех посетителей в таблице и вводит команды о редактировании"""
    cur_page = 0
    choice = None
    while True:
        os.system('clear')
        table = Table(title=f"-- Посетители -- стр.{cur_page+1}", show_header=True)
        titles = ("id", "Имя", "Фамилия")
        for title in titles:
            table.add_column(title, style="cyan", header_style="red")
        users = total_count_users()
        start_p = cur_page*count_rows
        for row in users[start_p:start_p+count_rows]:
            table.add_row(*map(str, row))
        console.print(table, justify="center")

        table_comands = Table()
        titles2 = ("#", "Команда")
        commands = ["Следующая страница", "Предыдущая страница", "Добавить посетителя", "Удалить посетителя", "Изменить посетителя"]
        for title in titles2:
            table_comands.add_column(title, style="cyan", header_style="red")
        for index, comand in enumerate(commands):
            table_comands.add_row(str(index + 1), comand)
        table_comands.add_row("q", "Назад")
        console.print(table_comands, justify="left")
    
        choice = Prompt.ask("введите # команды: ", choices=["1", "2", "3", "4", "5", "q"])
        if choice == "1" and (cur_page+1)*count_rows < len(users):
            cur_page += 1
        elif choice == "2" and (cur_page-1)*count_rows >= 0:
            cur_page -= 1
        elif choice == "3":
            user = menu_add_user()
            if user:
                add_user(*user)
        elif choice == "4":
            user_id = menu_delete_user()
            if user_id:
                delete_user(user_id)
        elif choice == "5":
            new_user = menu_edit_user(users)
            if new_user:
                edit_user(*new_user)
        elif choice == "q":
            cur_page = 0
            return ""


def menu_add_user():
    os.system('clear')
    console.print("ДОБАВЛЕНИЕ НОВОГО ПОСЕТИТЕЛЯ", style="red")
    console.print("Нажми Enter, чтобы пропустить")
    user = []
    titles = ["Имя", "Фамилия"]
    for title in titles:
        new_data = input(f"\rВведите - {title}: ")
        if new_data and utf_valid(new_data):
            user.append(new_data)
        else:
            user.append("None")
    # рисуем табличку
    table = Table()
    for title in titles:
        table.add_column(title, header_style="red")
    table.add_row(*user)
    console.print(table, justify="center")

    if Confirm.ask("Добавить посетителя?: "):
        return user
    else:
        return None


def menu_delete_user():
    console.print("УДАЛЕНИЕ ПОСЕТИТЕЛЯ", style="red")
    console.print("Нажми Enter, чтобы пропустить")

    answer = input("Введите ID посетителя: ")
    while not answer.isdigit() or answer == "":
        print("Неверный ввод. Попробуйте снова.")
        answer = input("Введите ID посетителя: ")
    
    user_id = int(answer)

    if Confirm.ask(f"Удалить посетителя с id = {user_id}? "):
        return user_id
    else:
        return None


def menu_edit_user(users):
    console.print("РЕДАКТИРОВАНИЕ ПОСЕТИТЕЛЯ", style="red")
    console.print("Нажми Enter, чтобы пропустить")

    answer = input(f"Введите ID пользователя: ")
    while not answer.isdigit():
        print(f"Неверный ввод: {answer}. Попробуйте снова.")
        answer = input(f"Введите ID пользователя: ")
    
    if not answer:
        return None

    user_id = answer
    old_user = list(filter(lambda x: x[0] == int(user_id), users))[0]
    new_user = [user_id,]
    titles = ["Имя", "Фамилия"]
    for title, old_data in zip(titles, old_user[1:]):
        new_data = input(f"\rВведите - {title}: ")
        if new_data and utf_valid(new_data):
            new_user.append(new_data)
        else:
            new_user.append(old_data)
    # рисуем табличку
    table = Table()
    for title in titles:
        table.add_column(title, header_style="red")
    table.add_row(*new_user[1:])
    console.print(table, justify="center")


    if Confirm.ask("Редактировать книгу?: "):
        return new_user
    else:
        return None


def menu_journal():
    """Отображает все книги в таблице и вводит команды о редактировании"""
    choice = None
    
    os.system('clear')
    table_comands = Table()
    titles2 = ("#", "Команда")
    commands = ["Выдать книгу в аренду", "Вернуть книгу в библиотеку"]
    for title in titles2:
        table_comands.add_column(title, style="cyan", header_style="red")
    for index, comand in enumerate(commands):
        table_comands.add_row(str(index + 1), comand)
    table_comands.add_row("q", "Назад")
    console.print(table_comands, justify="center")
    choice = Prompt.ask("введите # команды:", choices=["1", "2", "q"])
    if choice == "1":
        book_id = menu_search_book_id()
        if not book_id:
            return ""
        user_id = menu_search_user_id()
        if book_id and user_id:
            answer = ""
        while not answer.isdigit():
            answer = input("На какой срок выдать книгу(в днях): ")
        days = int(answer)
        add_getbook_to_journal(book_id, user_id, days_to_return=days)

    elif choice == "2":
        book_id = menu_search_book_id()
        if not book_id:
            return ""
        add_returnbook_to_journal(book_id)

    return ""

def menu_search_book_id():
    books = total_count_books()
    while True:
        books = search_books(books)
        table_comands = Table()
        titles2 = ("#", "Команда")
        commands = ["Выдать книгу в аренду(ввести ID)", "Продолжить поиск"]
        for title in titles2:
            table_comands.add_column(title, style="cyan", header_style="red")
        for index, comand in enumerate(commands):
            table_comands.add_row(str(index + 1), comand)
        table_comands.add_row("q", "Назад")
        console.print(table_comands, justify="left")

        choice = Prompt.ask("введите # команды:", choices=["1", "2", "q"])
        if choice == "1":
            answer = ""
            while not answer.isdigit():
                answer = input("Введите ID книги: ")
            book_id = answer
            return book_id
        elif choice == "2":
            continue
        elif choice == "q":
            return ""


def search_books(books):
    os.system('clear')
    req = input("Введите название книги для поиска: ")
    indexs = []
    for index, book in enumerate(books):
        if req in book[1]:
            indexs.append(index)
    new_books = []
    for index in indexs:
        new_books.append(books[index])

    table = Table(title=f"-- Результат поиска -- ", show_header=True)
    titles = ("id", "Название", "Автор", "Жанр", "последняя\nзапись в журнале")
    for title in titles:
        table.add_column(title, style="cyan", header_style="red")
    for row in new_books:
        table.add_row(*map(str, row))
    console.print(table, justify="center")
    return new_books


def menu_search_user_id():
    users = total_count_users()
    while True:
        users = search_users(users)

        table_comands = Table()
        titles2 = ("#", "Команда")
        commands = ["Выдать посетителю книгу(ввести ID)", "Продолжить поиск"]
        for title in titles2:
            table_comands.add_column(title, style="cyan", header_style="red")
        for index, comand in enumerate(commands):
            table_comands.add_row(str(index + 1), comand)
        table_comands.add_row("q", "Назад")
        console.print(table_comands, justify="left")

        choice = Prompt.ask("введите # команды:", choices=["1", "2", "q"])
        if choice == "1":
            answer = ""
            while not answer.isdigit():
                answer = input("Введите ID посетителя: ")
            user_id = answer
            return user_id
        elif choice == "2":
            continue
        elif choice == "q":
            return ""


def search_users(users):
    os.system('clear')
    req = input("Введите Фамилию посетителя для поиска: ")
    indexs = []
    for index, user in enumerate(users):
        if req in user[-1]:
            indexs.append(index)
    new_users = []
    for index in indexs:
        new_users.append(users[index])

    table = Table(title=f"-- Результат поиска -- ", show_header=True)
    titles = ("id", "Имя", "Фамилия")
    for title in titles:
        table.add_column(title, style="cyan", header_style="red")
    for row in new_users:
        table.add_row(*map(str, row))
    console.print(table, justify="center")
    return new_users

def main():
    choice = ""
    while True:
        os.system('clear')
        console.print("АПР БИБЛИОТЕКАРЬ", justify='center', style="Red")
        if choice == "":
            if check_db():
                menu_start()
            else:
                choice = menu_create_tables()
                continue
        elif choice == "q":
            os.system('clear')
            console.print("\nДо свидания!", justify='center', style="Red")
            break
        elif choice == "1":
            choice = menu_books()
            continue
        elif choice == "2":
            choice = menu_users()
            continue
        elif choice == "3":
            choice = menu_journal()
            continue
        elif choice == "4":
            pass
        else:
            menu_start()
            print("Неверный ввод. Попробуйте снова.")
        choice = Prompt.ask("Введите # команды:", choices=["1", "2", "3", "4", "q"], )
        
        
if __name__ == "__main__":
    main()