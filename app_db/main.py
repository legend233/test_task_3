from typing import Union

from fastapi import FastAPI

from functions import (create_tables, add_book, delete_book, edit_book, 
                    add_user, delete_user, edit_user, 
                    add_getbook_to_journal, add_returnbook_to_journal, 
                    total_count_books, total_count_users, 
                    total_count_rent, total_count_notreturn,
                    total_last_date, max_reading_author, top_genres,
                    top_genres_for_users, total_delays)

app = FastAPI()


@app.get("/create_tables")
def create_tables_():
    return create_tables()

@app.get("/add_book")
def add_book_():
    pass
    return add_book()

@app.get("/delete_book")
def delete_book_():
    pass
    return delete_book()

@app.get("/edit_book")
def edit_book_():
    pass
    return edit_book()

@app.get("/add_user")
def add_user_():
    pass
    return add_user()

@app.get("/delete_user")
def delete_user_():
    pass
    return delete_user()

@app.get("/edit_user")
def edit_user_():
    pass
    return edit_user()

@app.get("/add_getbook_to_journal")
def add_getbook_to_journal_():
    pass
    return add_getbook_to_journal()

@app.get("/add_returnbook_to_journal")
def add_returnbook_to_journal_():
    pass
    return add_returnbook_to_journal()

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