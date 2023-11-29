import requests
import asyncio
from typing import Iterable
from MessageParser import MessageParser

token = '6648128422:AAFOJYtBvuTQ5gJzUw9Te9x4ULj-_pFCZVI'
base = 'https://api.telegram.org/bot'+token+'/'
file = 'https://api.telegram.org/file/bot'+token+'/'


class TGBot():

    def __init__(self) -> None:
        self.parser: MessageParser = MessageParser()
        self.lastUpdate: int = 0

    async def run_bot(self):
        while True:
            await asyncio.sleep(2)
            self.get_updates()

    def get_updates(self):
        # messages checker
        try:
            response: requests.request = requests.get(
                base+'getUpdates?offset='+str(self.lastUpdate))
            if (response.status_code != 200):
                print('Messages receiving error: server responded not 200')
                return
        except Exception:
            print('Messages receiving error')
            return

        updates: Iterable = response.json()['result']
        if (isinstance(updates, list)) and updates:
            try:
                self.handle_telegram_update(updates=updates)
            except Exception:
                print("ЧЗХ")

    def handle_telegram_update(self, updates: Iterable):
        for i in updates:
            try:
                update_id: int = int(i['update_id'])
                self.lastUpdate: int = update_id + \
                    1 if self.lastUpdate <= update_id else self.lastUpdate
                update_type: str = self.parser.get_update_type(i)
                match update_type:
                    case 'photo':
                        self.parser.get_photo(
                            update_info=i, base=base, file=file)
                    case _:
                        print("Unidentified type")
            except Exception:
                print("Something went wrong")


if __name__ == '__main__':
    tgBot = TGBot()
    asyncio.run(main=tgBot.run_bot())
