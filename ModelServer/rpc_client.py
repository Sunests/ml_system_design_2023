import pika
from typing import Iterable
import random
import time


class RPCClient:
    def connect(self):

        self.products: Iterable = ['банан', 'капуста',
                                   'щавель', 'помидор', 'огурец', 'арбуз', 'алоэ']
        while True:
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host='rabbitmq', port="5672"))
                break
            except Exception as e:
                print(f"Failed to connect to RabbitMQ: {e}")
                time.sleep(3)

        self.channel = connection.channel()

        self.channel.queue_declare(queue='standart_image_caption')

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='standart_image_caption',
                                   on_message_callback=self._on_request)

    def _on_request(self, ch, method, props, body):
        # место для работы модели
        response = random.choice(self.products)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()
