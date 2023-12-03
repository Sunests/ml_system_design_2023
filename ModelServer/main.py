#!/usr/bin/env python
import pika
from typing import Iterable
import random

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=8080))

channel = connection.channel()

channel.queue_declare(queue='standart_image_caption')
products: Iterable = ['банан', 'капуста',
                      'щавель', 'помидор', 'огурец', 'арбуз', 'алоэ']


def on_request(ch, method, props, body):

    # место для работы модели
    response = random.choice(products)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='standart_image_caption',
                      on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
