# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import CHANNELS_DONOR
from src.telegram.tg_get_id_module import TgGetIdModule


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

    async def iter_channels(self):
        for channel in CHANNELS_DONOR:
            print(channel)

            id_channel = await self.get_id_channel(channel)

            if not id_channel:
                continue

            print()

    async def start_scrap(self):
        res_job = await self.iter_channels()

        return True
