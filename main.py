# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio
import os

from settings import REFRESH_TIME
from src.logic._logger import logger_msg
from src.telegram.tg_auth_module import TgAuthModule

import logging

from src.sql.bot_connector import BotDB

from src.telegram.tg_scrap_module import ScrapModule

logger_core = logging.getLogger()

logging.basicConfig(handlers=[logging.FileHandler(filename="./src/logs.txt",
                                                  encoding='utf-8', mode='a+')],
                    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
                    datefmt="%F %A %T",
                    level=logging.WARNING)


async def main():
    path_dir_project = os.path.dirname(__file__)

    sessions_path = os.path.join(path_dir_project, 'src', 'sessions')

    bot_core = TgAuthModule(sessions_path)

    telegram_core = await bot_core.start_tg()

    if not telegram_core:
        return False

    while True:
        await ScrapModule(path_dir_project, BotDB, telegram_core).start_scrap()

        print(f'Засыпаю на {REFRESH_TIME}')

        await asyncio.sleep(REFRESH_TIME)


if __name__ == '__main__':
    res = asyncio.run(main())
