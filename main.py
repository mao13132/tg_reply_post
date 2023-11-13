# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio
import logging
import os
from src.telegram.tg_auth_module import TgAuthModule

import logging

logger_core = logging.getLogger()

logging.basicConfig(handlers=[logging.FileHandler(filename="./src/logs.txt",
                                                  encoding='utf-8', mode='a+')],
                    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
                    datefmt="%F %A %T",
                    level=logging.DEBUG)


async def main():
    path_dir_project = os.path.dirname(__file__)

    sessions_path = os.path.join(path_dir_project, 'src', 'sessions')

    bot_core = TgAuthModule(sessions_path)

    telegram_core = await bot_core.start_tg()

    if not telegram_core:
        return False


if __name__ == '__main__':
    res = asyncio.run(main())
