from sqlite3 import Error, connect
from settings import DB
from schemes import schemes


def create_connection(path):
    """Создает соединение с базой данных SQLite"""
    connection = None
    try:
        connection = connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def create_tables():
    """Создает таблицы"""
    connection = create_connection(DB)
    cursor = connection.cursor()
    for _ in schemes:
        cursor.execute(_)
    connection.commit()
    connection.close()


def query(sql):
    connection = create_connection(DB)
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.close()
    return rows


def add_book(title, author, genre):
    """Добавляет книгу в базу данных"""
    connection = create_connection(DB)
    cursor = connection.cursor()
    # ищем id жанра в существующих данных
    cursor.execute(f"SELECT genre_id FROM genres WHERE genre = '{genre}'")

    if cursor.fetchall():  # если нашли, запишем его id
        genre_id = cursor.fetchall()[0][0]
    else:  # если жанр не нашелся, добавляем его и запишем получившийся id
        cursor.execute(f"INSERT INTO genres (genre) VALUES ('{genre}')")
        cursor.execute(f"SELECT genre_id FROM genres WHERE genre = '{genre}'")
        genre_id = cursor.fetchall()[0][0]

    cursor.execute(f"INSERT INTO books (title, author, genre_id) VALUES ('{title}', '{author}', {genre_id})")
    connection.commit()
    connection.close()


if __name__ == '__main__':
    add_book("Мастер и маргарита", "Булгаков М.А.", "Роман")
