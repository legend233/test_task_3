from functions import (add_book, delete_book, edit_book,
                        add_user, delete_user, edit_user,
                        add_getbook_to_journal, add_returnbook_to_journal,
                        total_count_books, total_count_users,
                        total_count_rent, total_count_notreturn,
                        total_last_date, max_reading_author, top_genres,
                        top_genres_for_users, total_delays)

from rich.table import Table
from rich.console import Console
from rich import print

def main():
    for _ in total_count_users():
        print(_)


if __name__ == "__main__":
    main()