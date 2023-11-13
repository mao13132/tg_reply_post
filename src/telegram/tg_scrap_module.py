# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio
import time
from datetime import datetime

from settings import CHANNELS_DONOR, ADMIN_CHANEL
from src.logic._logger import logger_msg
from src.telegram.get_target_id import GetTargetId
from src.telegram.join_chat import JoinChat
from src.telegram.tg_get_id_module import TgGetIdModule
from src.telegram.tg_get_message import TgGetMessage


class ScrapModule:
    def __init__(self, path_dir_project, BotDB, telegram_core):
        self.path_dir_project = path_dir_project
        self.BotDB = BotDB
        self.telegram_core = telegram_core

    async def get_id_channel(self, channel: str):
        if channel[1:].isdigit():
            return channel

        get_sql_id = self.BotDB.get_id_channel(channel)

        if not get_sql_id:
            get_sql_id = await TgGetIdModule(self.telegram_core, self.BotDB).get_id_channel(channel)

        return get_sql_id

    async def incubator_job_channel(self, id_channel, link_channel, target_id_chat):

        status_error = False

        for _try in range(2):

            try:
                res_get_message = await TgGetMessage(
                    self.path_dir_project, self.BotDB, self.telegram_core).start_one_channel(
                    id_channel, link_channel, target_id_chat)

                return res_get_message

            except Exception as es:

                status_error = str(es)

                logger_msg(f'Ошибка при работе с модулем TgGetMessage ошибка '
                           f'link_channel "{link_channel}" id_channel "id_channel" "{es}"')

                res_add = await JoinChat(self.telegram_core.app).join_to_chat(link_channel)

                logger_msg(f'Результат присоединения к чату: {res_add}')

                await asyncio.sleep(30)

        if status_error:
            return False
        else:
            return True

    async def iter_channels(self):

        good_count = 0

        target_id_chat = await GetTargetId(self.telegram_core, self.BotDB).get_target_id(ADMIN_CHANEL)

        if not target_id_chat:
            logger_msg(f'Не смог определить ID канала для постинга')

            return False

        for count, link_channel in enumerate(CHANNELS_DONOR):
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Начинаю обработку {link_channel}')

            if count > 0:
                time.sleep(60)

            id_channel = await self.get_id_channel(link_channel)

            if not id_channel:
                continue

            res = await self.incubator_job_channel(id_channel, link_channel, target_id_chat)

            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Закончил обработку {link_channel}')

            good_count += 1

        return good_count

    async def start_scrap(self):

        res_job = await self.iter_channels()

        print(f'Выполнил круг проверки всех чатов: {res_job}')

        return res_job
