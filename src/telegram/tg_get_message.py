# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import time
from datetime import datetime

from settings import ADMIN_CHANEL
from src.logic._logger import logger_msg
from src.telegram.get_target_id import GetTargetId

import logging

from src.telegram.join_chat import JoinChat


class TgGetMessage:
    def __init__(self, path_dir_project, BotDB, telegram_core):
        self.path_dir_project = path_dir_project
        self.BotDB = BotDB
        self.telegram_core = telegram_core

    async def forward_to_target_channel(self, message, target_id_chat):
        status_error = False

        for _try in range(3):

            try:

                await self.telegram_core.app.forward_messages(
                    chat_id=int(target_id_chat),
                    from_chat_id=message.chat.id,
                    message_ids=message.id
                )

                return True

            except Exception as es:
                status_error = str(es)

                if 'MESSAGE_ID_INVALID' in status_error:
                    return False

                logger_msg(f'Ошибка при пересылке необходимого сообщения в целевой чат "{es}"')

                res_add = await JoinChat(self.telegram_core.app).join_to_chat(target_id_chat)

                logger_msg(f'Результат присоединения к целевому чату: {res_add}')

                time.sleep(60)

                continue

        logger_msg(f'Все попытки переслать сообщение вышли "{status_error}"')

        return False

    async def delete_forward_message(self, message, id_channel):
        try:
            res = await self.telegram_core.app.delete_messages(id_channel, message.id)
        except Exception as es:
            logger_msg(f'Не удаётся удалить пересланное сообщение из целевого чата "{es}"')

            return False

        return True

    async def start_one_channel(self, id_channel, link_channel, target_id_chat):

        count_msg_from_channel = self.BotDB.count_from_channel(id_channel)

        good_message = 0

        if not count_msg_from_channel:
            new_channel = True
        else:
            new_channel = False

        async for message in self.telegram_core.app.get_chat_history(int(id_channel)):

            id_message = message.id

            try:
                format_msg = message.media.value
            except:
                format_msg = 'text'

            if format_msg != 'photo':
                continue

            if new_channel:
                res_add = self.BotDB.add_message(id_channel, id_message)

                logger_msg(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                           f'Добавил последние сообщение из нового чата: "{res_add}"')

                return True

            exist_post = self.BotDB.exist_message(id_channel, id_message)

            if exist_post:

                if good_message == 0:
                    print(f'В канале не публиковалось новых сообщений')

                return True

            res_forward = await self.forward_to_target_channel(message, target_id_chat)

            if not res_forward:
                continue

            logger_msg(f'Переслал #{id_message} сообщение из чата {link_channel} в {target_id_chat}')

            res_add = self.BotDB.add_message(id_channel, id_message)

            if res_add:
                good_message += 1

                res = await self.delete_forward_message(message, id_channel)

            print(f'Переслал сообщений: {good_message}')
