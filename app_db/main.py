from typing import Union

from fastapi import FastAPI

from functions import (create_tables, add_book, delete_book, edit_book, 
                    add_user, delete_user, edit_user, 
                    add_getbook_to_journal, add_returnbook_to_journal, 
                    total_count_books, total_count_users, 
                    total_count_rent, total_count_notreturn,
                    total_last_date, max_reading_author, top_genres,
                    top_genres_for_users, total_delays,
                    create_test_data)
from settings import DB
import os

app = FastAPI()


@app.get("/create_tables")
def create_tables_():
    return create_tables()

@app.get("/add_book")
def add_book_(title: str, author: str, genre: str):
    return add_book(title, author, genre)

@app.get("/delete_book")
def delete_book_(id: int):
    return delete_book(id)

@app.get("/edit_book")
def edit_book_(id: int, title: str = None, author: str = None, genre: str = None):
    return edit_book(id, title, author, genre)

@app.get("/add_user")
def add_user_(first_name: str, last_name: str):
    return add_user(first_name, last_name)

@app.get("/delete_user")
def delete_user_(id: int):
    return delete_user(id)

@app.get("/edit_user")
def edit_user_(id: int, first_name: str = None, last_name: str = None):
    return edit_user(id, first_name, last_name)

@app.get("/add_getbook_to_journal")
def add_getbook_to_journal_(book_id: int, user_id: int, days_to_return: int = 14):
    return add_getbook_to_journal(book_id, user_id, days_to_return)

@app.get("/add_returnbook_to_journal")
def add_returnbook_to_journal_(book_id: int):
    return add_returnbook_to_journal(book_id)

@app.get("/total_count_books")
def total_count_books_():
    return total_count_books()

@app.get("/total_count_users")
def total_count_users_():
    return total_count_users()

@app.get("/total_count_rent")
def total_count_rent_():
    return total_count_rent()

@app.get("/total_count_notreturn")
def total_count_notreturn_():
    return total_count_notreturn()

@app.get("/total_last_date")
def total_last_date_():
    return total_last_date()

@app.get("/max_reading_author")
def max_reading_author_():
    return max_reading_author()

@app.get("/top_genres")
def top_genres_():
    return top_genres()

@app.get("/top_genres_for_users")
def top_genres_for_users_():
    return top_genres_for_users()

@app.get("/total_delays")
def total_delays_():
    return total_delays()

@app.get("/check_db")
def check_db_():
    return os.path.exists(DB + "/sqlite.db")

@app.get("/create_test_data")
def create_test_data_():
    return create_test_data()
