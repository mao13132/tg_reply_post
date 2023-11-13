# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
class TgGetIdModule:
    def __init__(self, telegram_core, BotDB):
        self.BotDB = BotDB
        self.telegram_core = telegram_core

    async def get_id_channel(self, link_channel):
        try:

            name_chat = link_channel.replace('https://t.me/', '')

        except Exception as es:
            print(f'Не могу получить вырезать имя чата "{link_channel}" "{es}"')

            return False

        try:

            res_chat = await self.telegram_core.app.get_chat(name_chat)

        except Exception as es:
            print(f'Исключения при получение ID чат {es}')
            return False

        id_chat = res_chat.id

        self.BotDB.add_id_channel(link_channel, id_chat)

        return id_chat
