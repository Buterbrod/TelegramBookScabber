import sqlite3  # SQLite
import datetime
import os

db_file = 'telegramScrabber.db'


class DB:
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    # полный путь до файла db
    @staticmethod
    def db_file_path():
        # pwd = os.getcwd()  # текущая директория - pwd
        pwd = os.path.dirname(os.path.abspath(__file__))  # директория скрипта
        file_path = os.path.join(pwd, db_file)
        return file_path

    # присоединиться к бд
    def db_connect(self):
        # подключиться к базе данных
        self.connection = sqlite3.connect(self.db_file_path())
        # открыть курсор для выполнения операций
        self.cursor = self.connection.cursor()

    # отсоединиться от бд
    def db_disconnect(self):
        # закрыть курсор для выполнения операций
        self.cursor.close()
        # отключиться от базы данных
        self.connection.close()

    # создать таблицы, если их нет
    def db_create_tables(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Channels" \
            " (id INT, name TEXT, technical_name TEXT, last_process_date DATE)")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Books" \
            " (channel_id INT, id INT, message_id INT, message_date DATE, file_name TEXT, file_size INT, state TEXT)")

    # получить идентификатор канала
    def get_channel_id(self, technical_name):
        i = self.cursor. \
            execute("SELECT id FROM Channels WHERE technical_name = :v1", {'v1': technical_name}). \
            fetchone()
        return i[0]

    # получить идентификатор добавляемого канала
    def new_channel_id(self):
        # получить максимальное значение id
        self.cursor.execute("SELECT max(id) FROM Channels")
        res = self.cursor.fetchone()
        # 1 или max(id)+1
        i = 1 if res[0] is None else res[0] + 1
        return i

    # добавить телеграмм-канал
    def add_channel(self, name, technical_name):
        # получить id канала
        i = self.get_channel_id(technical_name)
        if i is None:
            # добавить новый канал
            i = self.new_channel_id()
            self.cursor.execute(
                "INSERT INTO Channels"
                " (id, name, technical_name, last_process_date)"
                " VALUES (?, ?, ?, ?)",
                (i, name, technical_name, datetime.datetime.now()))
            self.connection.commit()
        return i

    # получить идентификатор канала
    def get_book_id(self, channel_id, file_name):
        self.cursor.execute(
            "SELECT id "
            " FROM Books "
            " WHERE channel_id = :v1 AND file_name = :v2",
            {'v1': channel_id, 'v2': file_name})
        i = self.cursor.fetchone()
        return i

    # получить идентификатор для новой книги
    def new_book_id(self, channel_id):
        # получить максимальное значение id
        self.cursor.execute(
            "SELECT max(id)"
            " FROM Books"
            " WHERE channel_id = :v1",
            {'v1': channel_id})
        res = self.cursor.fetchone()
        # 1 или max(id)+1
        i = 1 if res[0] is None else res[0] + 1
        return i

    # добавить книгу из телеграмм-канала
    def add_book(self, channel_id, message_id, message_date, file_name, file_size, state):
        # получить id книги
        i = self.get_book_id(channel_id, file_name)
        if i is None:
            # добавить новый канал
            i = self.new_book_id(channel_id)
            self.cursor.execute(
                "INSERT INTO Books "
                " (channel_id, id, message_id, message_date, file_name, file_size, state)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)",
                (channel_id, i, message_id, message_date, file_name, file_size, state))
            self.connection.commit()
        return i

    # получить атрибуты книги
    def get_book_attr(self, channel_id, file_name):
        # получить атрибуты книги
        self.cursor.execute(
            "SELECT id, message_id, message_date, file_name, file_size, state"
            " FROM Books"
            " WHERE channel_id = :v1 AND file_name = :v2",
            {'v1': channel_id, 'v2': file_name})
        i = self.cursor.fetchone()
        return i

    # установить состояние книги - RESERVED, DOWNLOADED
    def set_book_state(self, channel_id, file_name, state):
        res = self.get_book_attr(channel_id, file_name)
        if res[4] == state:
            return False
        # установить состояние книги
        self.cursor.execute(
            "UPDATE Books"
            " SET state = ?"
            " WHERE channel_id = ? AND file_name = ?",
            (state, channel_id, file_name))
        self.connection.commit()
        return True


def test():
    urls = [
        ('Data Science Books', 'https://t.me/DataScience_Books'),
        ('Javascript js frontend', 'https://t.me/frontendarchive'),  # !!!
        ('Книги для программиста', 'https://t.me/bookofgeek'),
        ('Data Science Books (Backup Channel)', 'https://t.me/+KTJB5MeJzJRhMDk8'),
        ('DLStories | Нейронные сети и ИИ', 'https://t.me/dl_stories'),
        ('Physics.Math.Code', 'https://t.me/physics_lib'),
        ('Архив программиста', 'https://t.me/techrocksarchive'),  # !!!
        ('Архив книг по Базам данным', 'https://t.me/dblib'),
        ('Java библиотека', 'https://t.me/javalib')  # !!!
    ]

    db = DB()
    db.db_connect()
    db.db_create_tables()
    for i in urls:
        db.add_channel(i[0], i[1])
    db.add_book(1, 1, datetime.date.today(), 'test', 3000, 'RESERVED')
    st = db.set_book_state(1, 'test', 'PROCESSED')
    id = db.get_book_id(1, 'test')
    db.db_disconnect()


if __name__ == '__main__':
    test()
