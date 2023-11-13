import datetime
import sqlite3
from datetime import datetime

from src.logic._logger import logger_msg


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
                                f"monitoring (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"id_chat TEXT, id_msg TEXT, date DATETIME, other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table monitoring {es}')

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

    def exist_message(self, id_chat, id_msg):
        try:
            result = self.cursor.execute(f"SELECT * FROM monitoring WHERE id_chat='{id_chat}' AND id_msg='{id_msg}'")

            response = result.fetchall()

        except Exception as es:
            logger_msg(f'Ошибка при проверки существования записи из TG канала "{es}"')
            return False

        if response == []:
            return False

        return True

    def add_message(self, id_chat, id_msg):

        result = self.cursor.execute(f"SELECT * FROM monitoring WHERE id_chat='{id_chat}' AND id_msg='{id_msg}'")

        response = result.fetchall()

        if response == []:
            now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute("INSERT OR IGNORE INTO monitoring ('id_chat',"
                                "'id_msg', "
                                "'date') VALUES (?,?,?)",
                                (id_chat, id_msg,
                                 now_date,))

            self.conn.commit()
            return True

        return False

    def count_from_channel(self, id_chat):

        result = self.cursor.execute(f"SELECT count(*) FROM monitoring WHERE id_chat='{id_chat}'")

        response = result.fetchall()

        try:
            response = response[0][0]
        except:
            return ''

        return response

    def close(self):
        # Закрытие соединения
        self.conn.close()
        print('Отключился от SQL BD')
