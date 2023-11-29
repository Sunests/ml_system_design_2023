import requests
import asyncio
from typing import Iterable, Mapping
from MessageParser import MessageParser
from RPCClient import RPCClient
import threading

token = '6648128422:AAFOJYtBvuTQ5gJzUw9Te9x4ULj-_pFCZVI'
base = 'https://api.telegram.org/bot'+token+'/'
get_file_method_url = 'https://api.telegram.org/file/bot'+token+'/'


class TGBot():

    async def run_bot(self):
        self.lastUpdate: int = 0
        self.parser: MessageParser = MessageParser()
        self.rpcclient = await RPCClient().connect()
        while True:
            await asyncio.sleep(2)
            asyncio.create_task(self.get_updates())

    async def get_updates(self):
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
                updates_new = [self.handle_telegram_update(i) for i in updates]
                await asyncio.gather(*updates_new)
            except Exception:
                print("ЧЗХ")

    async def handle_telegram_update(self, i):
        try:
            update_id: int = int(i['update_id'])
            self.lastUpdate: int = update_id + \
                1 if self.lastUpdate <= update_id else self.lastUpdate
            chat_id: str = str(i['message']['chat']['id'])
            update_type: str = self.parser.get_update_type(i)
            match update_type:
                case 'image':
                    image_info = self.parser.get_photo(
                        update_info=i, base=base, get_file_method_url=get_file_method_url)
                    image_url: str = image_info['image_url']
                    image_id: str = image_info['image_id']
                    caption = str(await self.rpcclient.call(image_url))

                    await self.send_message_to_user(
                        chat_id, update_type, image_id=image_id, caption=caption)
                case _:
                    print("Unidentified type")
        except Exception as e:
            print(e)

    async def send_message_to_user(self, chat_id: str, update_type: str, **kwargs):
        try:
            match update_type:
                case 'image':
                    image_id: str = kwargs['image_id']
                    caption: str = kwargs['caption']
                    url = base+'sendPhoto?' + \
                        'chat_id=' + str(chat_id) +\
                        '&photo=' + image_id + \
                        '&caption=' + caption
                    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
                    response = loop.run_in_executor(None, requests.post, url)
                    await response
                    result_of_responce: requests.Response = response.result()
                    if result_of_responce.status_code != 200:
                        print("Фото не было отправлено")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    tgBot = TGBot()
    asyncio.run(main=tgBot.run_bot())
