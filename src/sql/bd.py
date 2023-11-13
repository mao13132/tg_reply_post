import datetime
import sqlite3
from datetime import datetime


class BotDB:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, db_file):
        try:

            self.conn = sqlite3.connect(db_file, timeout=30)
            print('Подключился к SQL DB:', db_file)
            self.cursor = self.conn.cursor()
            self.check_table()
        except Exception as es:
            print(f'Ошибка при работе с SQL {es}')

    def check_table(self):

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"id_channels (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"id_channel TEXT, link_channel TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table posts {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"posts (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"id_chat TEXT, date DATETIME, message_id TEXT, text TEXT, "
                                f"source TEXT, title TEXT, admin TEXT, target_channels TEXT, "
                                f"active BOOLEAN DEFAULT 1, "
                                f"publish BOOLEAN DEFAULT 0, other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table posts {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"media (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"message_id TEXT, path TEXT, source TEXT, admin TEXT, target_channels TEXT, "
                                f"other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table media {es}')

    def get_id_channel(self, link_channel):

        result = self.cursor.execute(f"SELECT id_channel FROM id_channels WHERE link_channel='{link_channel}'")

        response = result.fetchall()

        try:
            response = response[0][0]
        except:
            return []

        return response

    def add_id_channel(self, link_channel, id_chat):

        self.cursor.execute("INSERT OR IGNORE INTO id_channels ('link_channel', 'id_channel') VALUES (?, ?)",
                            (link_channel, id_chat))

        self.conn.commit()

        return self.cursor.lastrowid

    def exist_post(self, id_chat, title, date_post):
        try:
            result = self.cursor.execute(f"SELECT * FROM posts WHERE id_chat='{id_chat}' AND date='{date_post}' "
                                         f"AND title='{title}'")

            response = result.fetchall()

        except Exception as es:
            print(f'Ошибка при проверки существования записи из TG канала "{es}"')
            return False

        if response == []:
            return False

        return True

    def add_message(self, id_chat, message_id, title, text, source, date_post, admin_channel, target_channels):

        result = self.cursor.execute(f"SELECT * FROM posts WHERE admin='{admin_channel}' AND id_chat='{id_chat}' "
                                     f"AND title='{title}' AND source='{source}' AND "
                                     f"target_channels='{target_channels}'")

        response = result.fetchall()

        if response == []:
            self.cursor.execute("INSERT OR IGNORE INTO posts ('id_chat', 'message_id', 'title', 'text', 'source', "
                                "'date', 'admin', 'target_channels') VALUES (?,?,?,?,?,?,?,?)",
                                (id_chat, message_id, title, text, source,
                                 date_post, admin_channel, target_channels))

            self.conn.commit()
            return True

        return False

    def save_media(self, message_id, path, source, admin_channel, target_channels):

        result = self.cursor.execute(f"SELECT * FROM media WHERE path='{path}' AND admin='{admin_channel}' AND "
                                     f"target_channels='{target_channels}'")

        response = result.fetchall()

        if response == []:
            self.cursor.execute(
                "INSERT OR IGNORE INTO media ('message_id', 'path', 'source', 'admin', 'target_channels') "
                "VALUES (?,?,?,?,?)",
                (message_id, path, source, admin_channel, target_channels))

            self.conn.commit()
            return True

        return False

    def close(self):
        # Закрытие соединения
        self.conn.close()
        print('Отключился от SQL BD')
