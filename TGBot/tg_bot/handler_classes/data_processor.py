import json
from typing import Iterable, Mapping


class DataProcessor:

    def __init__(self, base_url: str) -> None:
        self.base_url: str = base_url
        image_buttons_json = open(file="./buttons/buttons_for_photos.json")
        self.buttons_for_images: Mapping = json.loads(
            image_buttons_json.read())

    def prepare_data(self, message_info: Mapping) -> Mapping:
        chat_id = message_info['chat_id']
        update_type = message_info['update_type']
        url: str = ""
        data: Mapping = {}
        match update_type:
            case 'image_message' | 'image_callback' | 'image_with_caption_message':
                url = self.base_url + 'sendPhoto'
                data = self._prepare_photo_data(
                    chat_id,
                    update_type,
                    message_info['image_id'],
                    message_info['caption']
                )
            case _:
                url = self.base_url + "sendMessage"
                data = self._prepare_text_data(
                    chat_id,
                    message_info['text'],
                    message_info['reply_to_message_id']
                )
        return {"url": url, "data": data}

    def _prepare_text_data(self, chat_id: str, text: str, reply_to_message_id: str) -> Mapping:
        data = {
            'chat_id': chat_id,
            'text': text,
            'reply_to_message_id': reply_to_message_id
        }
        return data

    def _prepare_photo_data(self, chat_id: str, update_type: str, image_id: str, caption: str) -> Mapping:

        data: Mapping = {}
        object_type = caption.split()[0]
        inline_keyboard: Mapping[str,
                                 Iterable[Mapping[str: str]]] = {}
        if update_type == 'image_message':
            buttons_for_images = dict(self.buttons_for_images).copy()
            inline_keyboard["inline_keyboard"] = []
            for i in range(len(buttons_for_images["inline_keyboard"])):
                inline_keyboard["inline_keyboard"].append([])
                for j in range(len(buttons_for_images["inline_keyboard"][i])):
                    inline_keyboard["inline_keyboard"][i].append({})
                    inline_keyboard["inline_keyboard"][i][j] = {
                        'text': buttons_for_images["inline_keyboard"][i][j]['text'],
                        'callback_data': object_type + " " + buttons_for_images["inline_keyboard"][i][j]['callback_data']
                    }

        data = {
            'chat_id': chat_id,
            'reply_markup': json.dumps(inline_keyboard),
            'photo': image_id,
            'caption': caption
        }

        return data
