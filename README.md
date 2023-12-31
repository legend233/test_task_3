# test_task_3
Тестовое задание от компании БИТ

## Задание
Приложение АРМ Помощник библиотекаря. Приложение должно позволять выяснить:
1. Какие книги есть в библиотеке;
2. Когда и кто брал книгу;
3. Где и у кого книга находится сейчас.

Подробнее: https://github.com/legend233/test_task_3/tree/main/info (ТЗ + схема БД)

## Установка приложений (Console)
    Запускаем Git Bash

    git clone https://github.com/legend233/test_task_3.git
### Data Base (sqlite + fastapi)
    cd test_task_3/app_db
    pip install -r requirements.txt
    touch .env      (Для создания файла .env в Linux или MacOS, для Windows пропустите эту команду)
    echo "DB=YOUR_DB_FOLDER" >> .env    (например DB=/home/user/db для Linux, MacOS или DB=C:\db для Windows)
    python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
### Client(requests)
    Запускаем Git Bash в новом окне

    cd test_task_3/app_client
    pip install -r requirements.txt
    touch .env      (Для создания файла .env в Linux или MacOS, для Windows пропустите эту команду)
    echo "SERVER=YOUR_SERVER_IP" >> .env (например SERVER=localhost если сервер запущен на том же компьютере, что и client или SERVER=154.54.55.65 если сервер запущен на другом компьютере. Укажите IP адрес своего сервера)
    echo "PORT=8000" >> .env
    echo "OUTPUTFOLDER=YOUR_OUTPUT_FOLDER" >> .env (например OUTPUTFOLDER=/home/user/output для Linux, MacOS или OUTPUTFOLDER=C:\output для Windows)

    выходим из Git Bash и запускаем main.py через shell
    python main.py

## Установка приложений (Docker)
    git clone https://github.com/legend233/test_task_3.git

### Data Base (sqlite + fastapi)
    cd test_task_3/app_db
    docker build -t apr-db .
    docker run -p 8000:8000 -e TZ=Europe/Moscow -v /YOUR_DB_FOLDER:/DB --rm --name apr-db apr-db

### Client(requests)
    cd test_task_3/app_client
    docker build -t apr-client .
    docker run -it -e TZ=Europe/Moscow -e SERVER=IP_ADDRESS -e PORT=YOUR_SERVER_PORT -v /YOUR_OUTPUT:/output --rm --name apr-client apr-client

### ENV
    DB=/YOUR_DB_FOLDER                  Путь к директории с БД
    SERVER=YOUR_SERVER_IP               IP адрес сервера
    PORT=8000                           Порт сервера
    OUTPUTFOLDER=YOUR_OUTPUT_FOLDER     Дирректория для сохранения отчетов

# Благодарности
* Ричард Столлман
* Линус Торвальдс
* Компания БИТ
