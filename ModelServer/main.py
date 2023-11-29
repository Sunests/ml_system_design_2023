#!/usr/bin/env python
import pika
from typing import Iterable

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=8080))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')
products: Iterable = ['банан', 'капуста',
                      'щавель', 'помидор', 'огурец', 'арбуз', 'алоэ']


def on_request(ch, method, props, body):
    response = body
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
