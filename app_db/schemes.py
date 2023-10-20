books_scheme = """CREATE TABLE IF NOT EXISTS books (
book_id INTEGER PRIMARY KEY AUTOINCREMENT, 
title VARCHAR(250), 
author VARCHAR(150), 
genre_id INTEGER, 
cur_journal_id INTEGER)"""

genres_scheme = """CREATE TABLE IF NOT EXISTS genres (
genre_id INTEGER PRIMARY KEY AUTOINCREMENT, 
genre VARCHAR(150))"""

users_scheme = """CREATE TABLE IF NOT EXISTS users (
user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
first_name VARCHAR(150), 
last_name VARCHAR(150))"""

rent_journal_scheme = """CREATE TABLE IF NOT EXISTS rent_journal (
id INTEGER PRIMARY KEY AUTOINCREMENT, 
fk_book_id INTEGER, 
fk_user_id INTEGER, 
date_start DATETIME, 
date_stop DATETIME, 
date_expected_stop DATETIME)"""

schemes = [books_scheme, genres_scheme, users_scheme, rent_journal_scheme]
