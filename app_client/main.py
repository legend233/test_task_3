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
import os

console = Console()

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
    table = Table(title="Книги", show_header=True)
    titles = ("id", "Название", "Автор", "Жанр", "последняя\nзапись в журнале")
    for title in titles:
        table.add_column(title, style="cyan", header_style="red")
    for row in total_count_books():
        table.add_row(*map(str, row))
    console.print(table, justify="center")

    table_comands = Table()
    titles2 = ("#", "Команда")
    commands = ["Добавить книгу", "Удалить книгу", "Изменить книгу"]
    for title in titles2:
        table_comands.add_column(title, style="cyan", header_style="red")
    for index, comand in enumerate(commands):
        table_comands.add_row(str(index + 1), comand)
    table_comands.add_row("q", "Назад")
    console.print(table_comands, justify="left")
def main():
    
    choice = None

    while True:
        os.system('clear')
        console.print("АПР БИБЛИОТЕКАРЬ", justify='center', style="Red")
        if choice == None:
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
            menu_books()
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass

        choice = input("введите # команды: ").lower()
        

if __name__ == "__main__":
    main()