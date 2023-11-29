from typing import Iterable, Mapping
import random
import requests


class MessageParser():

    def get_update_type(self, update_info):
        if 'message' in update_info and \
            'photo' in update_info['message'] and \
            update_info['message']['photo'] and \
                'file_id' in update_info['message']['photo'][-1]:
            return 'image'
        else:
            return None

    def get_photo(self, update_info, base, get_file_method_url) -> Mapping[str, str]:
        photo_id: str = update_info['message']['photo'][-1]['file_id']
        chat_id: int = int(update_info['message']['chat']['id'])
        url = base+'getFile?file_id='+str(photo_id)
        image_info: Mapping = requests.get(url=url).json()['result']
        image_id: str = image_info['file_id']
        image_path: str = image_info['file_path']
        image_url = get_file_method_url + image_path
        return {'image_id': image_id, 'image_url': image_url}
