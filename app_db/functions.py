import datetime
from sqlite3 import Error, connect
from settings import DB
from schemes import schemes


def create_connection(path: str):
    """Создает соединение с базой данных SQLite"""
    connection = None
    try:
        connection = connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


class SQL:
    def __enter__(self):
        self.conn = create_connection(DB)
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def execute(self, sql, params=()):
        return self.cur.execute(sql, params)


def create_tables():
    """Создает таблицы"""
    with SQL() as cursor:
        for _ in schemes:
            cursor.execute(_)
    return True


def query(sql: str) -> list:
    """Выводит информацию из базы данных"""
    with SQL() as cursor:
        rows = cursor.execute(sql)
        return rows.fetchall()


def add_book(title: str, author: str, genre: str) -> bool:
    """Добавляет книгу в базу данных"""
    with SQL() as cursor:
        # ищем id жанра в существующих данных
        request = cursor.execute("SELECT genre_id FROM genres WHERE genre = ?", (genre,))

        if request.fetchall():  # если нашли, запишем его id
            genre_id = request.fetchall()[0][0]
        else:  # если жанр не нашелся, добавляем его и запишем получившийся id
            cursor.execute("INSERT INTO genres (genre) VALUES (?)", (genre,))
            request = cursor.execute("SELECT genre_id FROM genres ORDER BY genre_id DESC LIMIT 1", params=())
            genre_id = request.fetchall()[0][0]
        cursor.execute("INSERT INTO books (title, author, genre_id) VALUES (?, ?, ?)", (title, author, genre_id))
    return True


def delete_book(id: int) -> bool:
    """Функция удаляет данные о книге из базы данных"""
    with SQL() as cursor:
        cursor.execute("DELETE FROM books WHERE book_id = ?", (id,))
    return True


def edit_book(id: int, title: str = None, author: str = None, genre: str = None) -> bool:
    """Функция редактирует данные о книге в базе данных"""
    with SQL() as cursor:
        request = cursor.execute("SELECT title, author, genre_id FROM books WHERE book_id = ?", (id,))
        if _ := request.fetchall():
            cur_title, cur_author, cur_genre_id = _[0]
            if title:
                cur_title = title
            if author:
                cur_author = author
            if genre:
                # ищем id жанра в существующих данных
                request = cursor.execute("SELECT genre_id FROM genres WHERE genre = ?", (genre,))
                if _ := request.fetchall():  # если нашли, запишем его id
                    cur_genre_id = _[0][0]
                else:  # если жанр не нашелся, добавляем его и запишем получившийся id
                    cursor.execute("INSERT INTO genres (genre) VALUES (?)", (genre,))
                    request = cursor.execute("SELECT genre_id FROM genres ORDER BY genre_id DESC LIMIT 1", params=())
                    cur_genre_id = request.fetchall()[0][0]
            # обновляем данные
            cursor.execute("UPDATE books SET title = ?, author = ?, genre_id = ? WHERE book_id = ?",
                           (cur_title, cur_author, cur_genre_id, id))
            return True
        else:
            return False


def add_user(first_name: str, last_name: str) -> bool:
    """Функция добавляет нового пользователя в базу данных"""
    with SQL() as cursor:
        # проверим, существует ли пользователь в базе
        request = cursor.execute("SELECT first_name, last_name FROM users WHERE first_name=? AND last_name=?",
                                 (first_name, last_name))
        if request.fetchall():
            # пользователь уже существует в базе выходим
            return False
        else:  # если нет, добавляем
            cursor.execute("INSERT INTO users (first_name, last_name) VALUES (?, ?)",
                           (first_name, last_name))
            return True


def delete_user(id: int) -> bool:
    """Функция удаляет данные о пользователе из базы данных"""
    with SQL() as cursor:
        cursor.execute("DELETE FROM users WHERE user_id = ?", (id,))
        return True


def edit_user(id: int, first_name: str = None, last_name: str = None) -> bool:
    """Функция редактирует данные о пользователе в базе данных"""
    with SQL() as cursor:
        request = cursor.execute("SELECT first_name, last_name FROM users WHERE user_id = ?", (id,))
        if _ := request.fetchall():
            cur_first_name, cur_last_name = _[0]
            if first_name:
                cur_first_name = first_name
            if last_name:
                cur_last_name = last_name
            cursor.execute("UPDATE users SET first_name = ?, last_name = ? WHERE user_id = ?",
                           (cur_first_name, cur_last_name, id))
            return True
        else:
            return False


def add_getbook_to_journal(book_id: int, user_id: int) -> bool:
    """Функция добавляет запись в журнал о взятии книги посетителем"""
    date_start = datetime.datetime.now()
    date_expected_stop = date_start + datetime.timedelta(days=14)
    with SQL() as cursor:
        request = cursor.execute("SELECT fk_book_id FROM rent_journal WHERE (fk_book_id) = ? AND date_stop IS NULL",
                                 (book_id,))
        if request.fetchall():
            return False
        else:
            cursor.execute(
                "INSERT INTO rent_journal (fk_book_id, fk_user_id, date_start, date_expected_stop) VALUES (?, ?, ?, ?)",
                    (book_id, user_id, date_start, date_expected_stop))
            fk_journal_id = cursor.execute("SELECT id FROM rent_journal ORDER BY id DESC LIMIT 1").fetchall()[0][0]
            cursor.execute("UPDATE books SET cur_journal_id = ? WHERE book_id = ?",
                           (fk_journal_id, book_id))
            return True

def add_returnbook_to_journal(book_id: int) -> bool:
    """Добовляет отметку в журнал о возврате книги. Также обновляет последнюю запись о книги в таблице books"""
    with SQL() as cursor:
        cur_journal_id = cursor.execute("SELECT id FROM rent_journal WHERE fk_book_id = ? ORDER BY id DESC LIMIT 1",
                                        (book_id,)).fetchall()[0][0]
        cursor.execute("UPDATE rent_journal SET date_stop = ? WHERE fk_book_id = ? AND date_stop IS NULL",
                       (datetime.datetime.now(), book_id))
        cursor.execute("UPDATE books SET cur_journal_id = ? WHERE book_id = ?", (cur_journal_id, book_id))
        return True


def total_count_books() -> int:
    """Выводит количество книг в библиотеке"""
    with SQL() as cursor:
        return cursor.execute("SELECT COUNT(*) FROM books").fetchall()[0][0]


def total_count_users() -> int:
    """Выводит количество посетителей в библиотеке"""
    with SQL() as cursor:
        return cursor.execute("SELECT COUNT(*) FROM users").fetchall()[0][0]


def total_count_rent(user_id: int) -> int:
    """Выводит количество взятий книг посетителем"""
    with SQL() as cursor:
        return cursor.execute("SELECT COUNT(*) FROM rent_journal WHERE fk_user_id = ?",
                              (user_id,)).fetchall()[0][0]

def total_count_notreturn(user_id: int) -> int:
    """Выводит количество невозвращенных книг посетителем"""
    with SQL() as cursor:
        return cursor.execute("SELECT COUNT(*) FROM rent_journal WHERE fk_user_id = ? AND date_stop IS NULL",
                              (user_id,)).fetchall()[0][0]

if __name__ == '__main__':
    print(total_count_rent(11))
