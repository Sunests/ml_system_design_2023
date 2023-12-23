import json
from ultralytics import YOLO
import requests
from PIL import Image
from io import BytesIO


class YoloModel:
    def __init__(self):
        with open('products.json', 'r', encoding='utf-8') as products:
            self.classes = json.load(products)
        self.num_classes = len(self.classes.keys())

        self.yolo_model = YOLO('best.onnx', task='classify')

    def recognize(self, url: str) -> str:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))

        results = self.yolo_model.predict(image, imgsz=(224, 224), verbose=False)

        probs = [float(prob) for prob in list(results[0].probs.data)]
        predicted_class = self.classes[str(probs.index(max(probs)))]

        return predicted_class


# model = YoloModel()
# print(model.recognize('https://shop.evalar.ru/upload/iblock/602/602d6ce5691fe5f71377e1fdf587c201.jpg'))
