import pika
from typing import Iterable
import random
import time


class RPCClient:
    def __init__(self, model):
        self.model = model

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port="5672"))

        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='standart_image_caption')

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='standart_image_caption',
                                   on_message_callback=self._on_request)

    def _on_request(self, ch, method, props, body):
        # Место для работы модели
        response = self.model.recognize(body)
        print(body)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()


