# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio

from src.logic._logger import logger_msg
from src.telegram.join_chat import JoinChat


class TgGetIdModule:
    def __init__(self, telegram_core, BotDB):
        self.BotDB = BotDB
        self.telegram_core = telegram_core

    async def get_id_channel(self, link_channel):
        status_error = False

        for _try in range(2):
            try:

                name_chat = link_channel.replace('https://t.me/', '')

            except Exception as es:
                logger_msg(f'Не могу получить вырезать имя чата "{link_channel}" "{es}"')

                return False

            try:
                res_chat = await self.telegram_core.app.get_chat(name_chat)

                id_chat = res_chat.id

                self.BotDB.add_id_channel(link_channel, id_chat)

                return id_chat

            except Exception as es:

                status_error = str(es)

                # print(f'Ошибка при работе с модулем TgGetMessage ошибка "{es}"')

                res_add = await JoinChat(self.telegram_core.app).join_to_chat(link_channel)

                print(f'Результат присоединения к чату: {res_add}')

                await asyncio.sleep(30)

        logger_msg(f'Ошибка при работе с модулем TgGetMessage ошибка "{status_error}"')

        return False
