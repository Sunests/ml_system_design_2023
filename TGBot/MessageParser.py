from typing import Iterable, Mapping
import random
import requests


class MessageParser():

    def __init__(self) -> None:
        self.products: Iterable = ['банан', 'капуста', 'щавель',
                                   'помидор', 'огурец', 'арбуз', 'алоэ']

    def get_update_type(self, update_info):
        if 'message' in update_info and \
            'photo' in update_info['message'] and \
            update_info['message']['photo'] and \
                'file_id' in update_info['message']['photo'][-1]:
            return 'photo'
        else:
            return None

    def get_photo(self, update_info, base, file):
        photo_id: str = update_info['message']['photo'][-1]['file_id']
        chat_id: int = int(update_info['message']['chat']['id'])
        image_info: Mapping = requests.get(
            base+'getFile?file_id='+str(photo_id)).json()['result']
        file_unique_id: str = image_info['file_unique_id']
        file_path: str = image_info['file_path']
        img_data = requests.get(
            file+str(file_path)).content
        files: Mapping = {'photo': img_data}
        requests.post(
            base+'sendPhoto?chat_id='+str(chat_id)+'&caption=' + random.choice(self.products), files=files)
