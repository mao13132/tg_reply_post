# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from datetime import datetime


class JoinChat:
    def __init__(self, app):
        """@developer_telegrams"""

        self.app = app

    async def join_to_chat(self, link_channel):
        """@developer_telegrams"""
        try:
            if '+' not in link_channel:
                link_channel = link_channel.replace('https://t.me/', '')

            response = await self.app.join_chat(link_channel)
        except Exception as es:
            print(f'{datetime.now().strftime("%H:%M:%S")} Ошибка join_chat ()  "{es}"')

            return False

        return True
