from typing import Mapping
import requests
import asyncio


class MessageParser():

    def __init__(self, base_url: str, file_url: str) -> None:
        self.base_url: str = base_url
        self.file_url: str = file_url

    async def parse(self, update_info):
        chat_id: str = self._get_chat_id(update_info)
        update_type: str = self._get_update_type(update_info)
        parsed_data: Mapping = {}
        match update_type:
            case 'image_message' | 'image_callback' | 'image_with_caption_message':
                image_info = self._get_photo(update_info)
                image_url: str = image_info['image_url']
                image_id: str = image_info['image_id']
                input_caption: str = image_info['input_caption']
                parsed_data = {
                    'image_id': image_id,
                    'image_url': image_url,
                    'input_caption': input_caption
                }
            case _:
                parsed_data = {
                    'text': 'Неверный формат сообщения. Прикрепите фото "быстрым способом" с запросом по желанию',
                    'reply_to_message_id': self._get_replied_message_id(update_info)
                }
        parsed_data['chat_id'] = chat_id
        parsed_data['update_type'] = update_type
        return parsed_data

    def _get_chat_id(self, update_info) -> str:
        if 'message' in update_info:
            chat = update_info['message']['chat']
        elif 'callback_query' in update_info:
            chat = update_info['callback_query']['message']['chat']
        else:
            raise TypeError("Unknowned message's type")

        chat_id = str(chat['id'])

        return chat_id

    def _get_update_type(self, update_info):
        if 'message' in update_info and \
            'photo' in update_info['message'] and \
            update_info['message']['photo'] and \
                'file_id' in update_info['message']['photo'][-1]:
            if 'caption' in update_info['message']:
                return 'image_with_caption_message'
            else:
                return 'image_message'
        elif 'callback_query' in update_info and \
            'message' in update_info['callback_query'] and \
            'photo' in update_info['callback_query']['message'] and \
            update_info['callback_query']['message']['photo'] and \
                'file_id' in update_info['callback_query']['message']['photo'][-1]:
            return 'image_callback'
        else:
            return None

    def _get_photo(self, update_info) -> Mapping[str, str]:
        photo_id: str = ""
        input_caption: str = ""
        if 'message' in update_info:
            photo_id = update_info['message']['photo'][-1]['file_id']
            if 'caption' in update_info['message']:
                input_caption = update_info['message']["caption"]
        elif 'callback_query' in update_info:
            photo_id = update_info["callback_query"]['message']['photo'][-1]['file_id']
            input_caption = update_info["callback_query"]["data"]
        else:
            raise TypeError("Unknowned message's type")
        url: str = self.base_url + 'getFile?file_id='+str(photo_id)
        image_info: Mapping = requests.get(url=url).json()['result']
        image_id: str = image_info['file_id']
        image_path: str = image_info['file_path']
        image_url: str = self.file_url + image_path
        return {'image_id': image_id, 'image_url': image_url, 'input_caption': input_caption}

    def _get_replied_message_id(self, update_info) -> str:
        replied_id: str = ""
        if 'message' in update_info:
            replied_id = str(update_info['message']['message_id'])
        elif 'callback_query' in update_info:
            replied_id = str(
                update_info["callback_query"]['message']['message_id'])
        else:
            raise TypeError("Unknowned message's type")
        return replied_id
