import json
import warnings
import requests

warnings.filterwarnings('ignore')

from io import BytesIO

import seaborn as sns
from PIL import Image
sns.set_theme(style="darkgrid", font_scale=1.5, font="SimHei", rc={"axes.unicode_minus":False})

import torch
import torchmetrics
from torch import nn, optim
from torch.nn import functional as F

from torchvision import transforms, models
import lightning.pytorch as pl


class LitModel(pl.LightningModule):
    def __init__(self):
        super().__init__()
        with open('products.json', 'r', encoding="utf-8") as products:
            self.classes = json.load(products)
        self.num_classes = len(self.classes.keys())

        self.densenet = models.densenet121(pretrained=True)
        for param in self.densenet.parameters():
            param.requires_grad = False
        self.densenet.classifier = nn.Linear(1024, self.num_classes)
        self.accuracy = torchmetrics.Accuracy(task="multiclass", num_classes=self.num_classes)
        self.load_state_dict(torch.load('model_params.pt'))
        self.test_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

    def forward(self, x):
        x = self.densenet(x)
        return x

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=0.001, betas=(0.9, 0.99), eps=1e-08, weight_decay=1e-5)
        return optimizer

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        acc = self.accuracy(y_hat, y)
        self.log('train_loss', loss, on_step=True, on_epoch=False, prog_bar=True, logger=True)
        self.log('train_acc', acc, on_step=True, on_epoch=False, logger=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        preds = torch.argmax(y_hat, dim=1)
        acc = self.accuracy(preds, y)
        self.log('val_acc', acc, on_step=False, on_epoch=True, prog_bar=True, logger=True)

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        preds = torch.argmax(y_hat, dim=1)
        acc = self.accuracy(preds, y)
        self.log('test_acc', acc)

    def predict_step(self, batch, batch_idx, dataloader_idx=None):
        x, y = batch
        y_hat = self(x)
        preds = torch.argmax(y_hat, dim=1)
        return preds

    def recognize(self, url: str) -> str:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        input_image = self.test_transform(image).float()
        input_batch = input_image.unsqueeze(0)

        self.densenet.eval()

        out = self.densenet(input_batch)
        _, index = torch.max(out, 1)
        percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

        predicted_class = self.classes[str(percentage.tolist().index(max(percentage)))]

        return predicted_class


# model = LitModel()
# print(model.recognize('https://shop.evalar.ru/upload/iblock/602/602d6ce5691fe5f71377e1fdf587c201.jpg'))
