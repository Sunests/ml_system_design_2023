import asyncio
from typing import Iterable, Mapping
from tg_bot.handler_classes.message_parser import MessageParser
from tg_bot.handler_classes.rpc_client import RPCClient
import aiohttp
from tg_bot.handler_classes.data_processor import DataProcessor
import os
from dotenv import load_dotenv


class TGBot():

    async def run_bot(self):
        self.lastUpdate: int = 0
        load_dotenv()
        token = os.getenv("API_TOKEN")
        self.base_url = 'https://api.telegram.org/bot'+token+'/'
        self.file_url = 'https://api.telegram.org/file/bot'+token+'/'
        self.rpcclient = await RPCClient().connect()

        self.parser: MessageParser = MessageParser(
            self.base_url, self.file_url)

        self.session = aiohttp.ClientSession()
        self.dp = DataProcessor(self.base_url)
        while True:
            await asyncio.sleep(2)
            asyncio.create_task(self.get_updates())

    async def get_updates(self) -> Iterable:
        try:
            print("Было")
            response: aiohttp.ClientResponse = await self.session.get(
                self.base_url+'getUpdates?offset='+str(self.lastUpdate))
            if response.status == 409:
                return []
            if response.status != 200:
                print('Messages receiving error: server responded not 200')
                return []
            updates = (await response.json())['result']
            if (isinstance(updates, list)) and updates:
                updates_new = [self.handle_telegram_update(i) for i in updates]
                asyncio.gather(*updates_new)
            else:
                return []

        except:
            return []

    async def handle_telegram_update(self, update_info):
        try:
            update_id: int = int(update_info['update_id'])
            self.lastUpdate: int = update_id + \
                1 if self.lastUpdate <= update_id else self.lastUpdate
            message_info = await self.parser.parse(update_info)
            message_info['caption'] = await self.get_caption(message_info)
            prepared_data = self.dp.prepare_data(message_info)

            await self.send_message_to_user(prepared_data)
        except Exception as e:
            print(e)

    async def get_caption(self, message_info):
        update_type = message_info['update_type']
        caption = ""
        match update_type:
            case 'image_message' | 'image_callback' | 'image_with_caption_message':
                image_url = message_info['image_url']
                if update_type != 'image_callback':
                    caption = str(await self.rpcclient.get_image_info(image_url, True))
                if update_type != 'image_message':
                    input_caption = message_info['input_caption']
                    caption = f"{caption}\n{str(await self.rpcclient.get_image_info(input_caption, False))}"

        return caption

    async def send_message_to_user(self, prepared_data: Mapping):
        url = prepared_data["url"]
        data = prepared_data["data"]
        response: aiohttp.ClientResponse = await self.session.post(url=url, data=data)
        response.raise_for_status()
