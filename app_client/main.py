import requests
from settings import SERVER, PORT

HOST = f"http://{SERVER}:{PORT}"



def add_book() -> list:
    pass


def delete_book(id: int) -> list:
    pass

def edit_book() -> list:
    pass

def add_user() -> list:
    pass

def delete_user() -> list:
    pass

def edit_user() -> list:
    pass

def add_getbook_to_journal() -> list:
    pass

def add_returnbook_to_journal() -> list:
    pass

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
