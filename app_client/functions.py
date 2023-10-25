import requests
from settings import SERVER, PORT

HOST = f"http://{SERVER}:{PORT}"


def create_tables():
    return requests.get(HOST + "/create_tables").json()

def add_book(title: str, author: str, genre: str) -> list:
    return requests.get(HOST + f"/add_book?title={title}&author={author}&genre={genre}").json()


def delete_book(id: int) -> list:
    return requests.get(HOST + f"/delete_book?id={id}").json()

def edit_book(id: int, title: str = None, author: str = None, genre: str = None) -> list:
    return requests.get(HOST + f"/edit_book?id={id}&title={title}&author={author}&genre={genre}").json()

def add_user(first_name: str, last_name: str) -> list:
    return requests.get(HOST + f"/add_user?first_name={first_name}&last_name={last_name}").json()

def delete_user(id: int) -> list:
    return requests.get(HOST + f"/delete_user?id={id}").json()

def edit_user(id: int, first_name: str = None, last_name: str = None) -> list:
    return requests.get(HOST + f"/edit_user?id={id}&first_name={first_name}&last_name={last_name}").json()

def add_getbook_to_journal(book_id: int, user_id: int, days_to_return: int = 14) -> list:
    return requests.get(HOST + f"/add_getbook_to_journal?book_id={book_id}&user_id={user_id}&days_to_return={days_to_return}").json()

def add_returnbook_to_journal(book_id: int) -> list:
    return requests.get(HOST + f"/add_returnbook_to_journal?book_id={book_id}").json()

def total_count_books() -> list:
    return requests.get(HOST + "/total_count_books").json()

def total_count_users() -> list:
    return requests.get(HOST + "/total_count_users").json()

def total_count_rent() -> list:
    return requests.get(HOST + "/total_count_rent").json()

def total_count_notreturn() -> list:
    return requests.get(HOST + "/total_count_notreturn").json()

def total_last_date() -> list:
    return requests.get(HOST + "/total_last_date").json()

def max_reading_author() -> list:
    return requests.get(HOST + "/max_reading_author").json()

def top_genres() -> list:
    return requests.get(HOST + "/top_genres").json()

def top_genres_for_users() -> list:
    return requests.get(HOST + "/top_genres_for_users").json()

def total_delays() -> list:
    return requests.get(HOST + "/total_delays").json()

def check_db():
    return requests.get(HOST + "/check_db").json()

def create_test_data():
    return requests.get(HOST + "/create_test_data").json()