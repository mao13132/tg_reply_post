# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from datetime import datetime

from src.telegram.tg_get_id_module import TgGetIdModule


class GetTargetId:
    def __init__(self, telegram_core, BotDB):
        """@developer_telegrams"""

        self.telegram_core = telegram_core
        self.BotDB = BotDB

    async def get_target_id(self, channel):

        if channel[1:].isdigit():
            return channel

        get_sql_id = self.BotDB.get_id_channel(channel)

        if not get_sql_id:
            get_sql_id = await TgGetIdModule(self.telegram_core, self.BotDB).get_id_channel(channel)

        return get_sql_id
