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


def add_book(title: str, author: str, genre: str) -> bool:
    """Добавляет книгу в базу данных"""
    with SQL() as cursor:
        # ищем id жанра в существующих данных
        request = cursor.execute("SELECT genre_id FROM genres WHERE genre = ?", (genre,))

        if _ := request.fetchall():  # если нашли, запишем его id
            genre_id = _[0][0]
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


def add_getbook_to_journal(book_id: int, user_id: int, days_to_return: int = 14) -> bool:
    """Функция добавляет запись в журнал о взятии книги посетителем"""
    date_start = datetime.datetime.now()
    date_expected_stop = date_start + datetime.timedelta(days=days_to_return)
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


def total_count_books() -> list:
    """Выводит все книги в библиотеке"""
    with SQL() as cursor:
        return cursor.execute(
            """SELECT b.book_id, b.title, b.author, g.genre, b.cur_journal_id
            FROM books b
            LEFT JOIN genres g ON b.genre_id = g.genre_id""").fetchall()


def total_count_users() -> list:
    """Выводит всех посетителей в библиотеке"""
    with SQL() as cursor:
        return cursor.execute("SELECT * FROM users").fetchall()


def total_count_rent() -> list:
    """Выводит количество взятых книг посетителем за все время"""
    with SQL() as cursor:
        return cursor.execute(
            """SELECT u.*, COUNT(r.id) AS rent_count
            FROM users u
            LEFT JOIN rent_journal r ON u.user_id = r.fk_user_id
            GROUP BY u.user_id""").fetchall()


def total_count_notreturn() -> list:
    """Выводит количество невозвращенных книг посетителями"""
    with SQL() as cursor:
        return cursor.execute(
            """SELECT r.fk_user_id, u.first_name, u.last_name, count(r.id) AS rent_count
            FROM rent_journal r
            LEFT JOIN users u ON r.fk_user_id = u.user_id
            WHERE r.date_stop IS NULL
            GROUP BY r.fk_user_id""").fetchall()


def total_last_date() -> list:
    """Выводит последние посещения библиотеки"""
    with SQL() as cursor:
        return cursor.execute(
            """select *, (SELECT CASE WHEN date_stop IS NULL THEN date_start 
            ELSE date_stop END AS last_date FROM rent_journal WHERE rent_journal.fk_user_id = users.user_id)
            FROM users""").fetchall()

def max_reading_author() -> list:
    """Выводит рейтинг самых читаемых авторов у посетителей"""
    with SQL() as cursor:
        return cursor.execute(
            """SELECT author, COUNT(books.author) AS author_count FROM rent_journal
            LEFT JOIN books ON rent_journal.fk_book_id=books.book_id
            GROUP BY author ORDER BY author_count DESC""").fetchall()


def top_genres() -> list:
    """Выводит самые читаемые жанры в порядке убывания"""
    with SQL() as cursor:
        return cursor.execute(
            """SELECT genre, COUNT(books.genre_id) AS genre_count FROM rent_journal
            LEFT JOIN books ON rent_journal.fk_book_id=books.book_id
            LEFT JOIN genres ON books.genre_id=genres.genre_id
            GROUP BY genre ORDER BY genre_count DESC"""
        ).fetchall()


def top_genres_for_users() -> list:
    """Выводит самые читаемые жанры посетителей"""
    with SQL() as cursor:
        return cursor.execute(
            """WITH counts AS (
            SELECT u.first_name, u.last_name, r.fk_user_id, g.genre, COUNT(*) as genre_count
            FROM rent_journal r
            LEFT JOIN books b ON r.fk_book_id = b.book_id
            LEFT JOIN genres g ON b.genre_id = g.genre_id
            LEFT JOIN users u ON r.fk_user_id = u.user_id
            GROUP BY r.fk_user_id, g.genre
            )
            SELECT c1.fk_user_id, c1.first_name, c1.last_name, c1.genre
            FROM counts c1
            LEFT JOIN counts c2 ON c1.fk_user_id = c2.fk_user_id AND c1.genre_count < c2.genre_count
            WHERE c2.fk_user_id IS NULL
            group by c1.fk_user_id
            ORDER BY c1.fk_user_id""").fetchall()


def total_delays() -> list:
    """Выводит количество невозвращенных вовремя книг посетителями"""
    with SQL() as cursor:
        return cursor.execute(
            """SELECT id, users.first_name, users.last_name, books.title, date_stop, date_expected_stop
            FROM rent_journal
            LEFT JOIN books ON rent_journal.fk_book_id = books.book_id
            LEFT JOIN users ON rent_journal.fk_user_id = users.user_id
            WHERE (date_stop > date_expected_stop) or (date_stop IS NULL and current_timestamp > date_expected_stop)
            ORDER BY fk_user_id""").fetchall()


def create_test_data():
    """Создание тестовых данных"""
    create_tables()
    # книги
    add_book("The Great Gatsby", "F. Scott Fitzgerald", "Fiction")
    add_book("To Kill a Mockingbird", "Harper Lee", "Fiction")
    add_book("1984", "George Orwell", "Science Fiction")
    add_book("Pride and Prejudice", "Jane Austen", "Romance")
    add_book("The Catcher in the Rye", "J.D. Salinger", "Fiction")
    add_book("The Hobbit", "J.R.R. Tolkien", "Fantasy")
    add_book("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "Fantasy")
    add_book("The Lord of the Rings", "J.R.R. Tolkien", "Fantasy")
    add_book("To the Lighthouse", "Virginia Woolf", "Fiction")
    add_book("Moby-Dick", "Herman Melville", "Adventure")
    add_book("The Odyssey", "Homer", "Epic Poetry")
    add_book("The Adventures of Huckleberry Finn", "Mark Twain", "Adventure")
    add_book("The Great Expectations", "Charles Dickens", "Classic")
    add_book("The Alchemist", "Paulo Coelho", "Fiction")
    add_book("Crime and Punishment", "Fyodor Dostoevsky", "Psychological Fiction")
    add_book("To Kill a Mockingbird", "Harper Lee", "Fiction")
    add_book("Go Set a Watchman", "Harper Lee", "Fiction")
    add_book("To Kill a Mockingbird", "Harper Lee", "Classic")
    add_book("To Kill a Mockingbird", "Harper Lee", "Literature")
    add_book("To Kill a Mockingbird", "Harper Lee", "Drama")


    # пользователи
    add_user("John", "Doe")
    add_user("Jane", "Smith")
    add_user("Michael", "Johnson")
    add_user("Emily", "Davis")
    add_user("David", "Wilson")
    add_user("Sarah", "Anderson")
    add_user("Robert", "Thomas")
    add_user("Jennifer", "Taylor")
    add_user("William", "Martinez")
    add_user("Jessica", "Brown")

    # журнал книг аренда
    add_getbook_to_journal(1, 1, 14)
    add_getbook_to_journal(2, 1, 14)
    add_getbook_to_journal(3, 1, 14)
    add_getbook_to_journal(4, 1, 14)
    add_getbook_to_journal(5, 2, 14)
    add_getbook_to_journal(6, 2, 14)
    add_getbook_to_journal(7, 2, 14)
    add_getbook_to_journal(8, 2, 14)
    add_getbook_to_journal(9, 2, 14)
    add_getbook_to_journal(10, 3, 14)
    add_getbook_to_journal(11, 3, 14)
    add_getbook_to_journal(12, 3, 14)
    add_getbook_to_journal(13, 3, 14)
    add_getbook_to_journal(14, 3, 14)
    add_getbook_to_journal(15, 4, 14)
    add_getbook_to_journal(16, 4, 14)
    add_getbook_to_journal(17, 4, 14)
    add_getbook_to_journal(18, 4, 14)
    
    # возврат книг в журнал
    add_returnbook_to_journal(book_id=1)
    add_returnbook_to_journal(book_id=2)
    add_returnbook_to_journal(book_id=3)
    add_returnbook_to_journal(book_id=4)
    add_returnbook_to_journal(book_id=5)
    add_returnbook_to_journal(book_id=6)


    # добавляем просрок книги в журнал вручную
    with SQL() as cursor:
        date_stop = datetime.datetime.now() + datetime.timedelta(days=14)
        date_expected_stop = date_stop - datetime.timedelta(days=4)
        for id in range(12, 17):
            cursor.execute("""UPDATE rent_journal SET date_stop = ?, date_expected_stop = ? WHERE fk_book_id = ?""", (date_stop, date_expected_stop, id))