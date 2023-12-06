# -*- coding: utf-8 -*-
from Chat import Manager as manager
import asyncio
import logging

from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage
from Product_button_parser import Product_button_parser

async def main() -> None:
    connection = await connect("http://localhost:5672")
    channel = await connection.channel()
    exchange = channel.default_exchange
    queue = await channel.declare_queue("additional_image_caption")
    parser = Product_button_parser()
    print(" [x] Awaiting RPC requests")
    # chat = manager.ChatManager()

    async with queue.iterator() as qiterator:
        message: AbstractIncomingMessage
        async for message in qiterator:
            try:
                async with message.process(requeue=False):
                    assert message.reply_to is not None

                    geted_info = message.body.decode('utf-8')

                    print(geted_info)

                    # chat.getProductInfo("Банан")      // returns string
                    # chat.getProductFact("Банан")
                    # geted_info = chat.getCustomInfo("Банан", geted_info)
                    # chat.getRandomInfo("Банан")

                    response = geted_info.encode()
                    await exchange.publish(
                        Message(
                            body=response,
                            correlation_id=message.correlation_id,
                        ),
                        routing_key=message.reply_to,
                    )

            except Exception:
                logging.exception("Processing error for message %r", message)


if __name__ == '__main__':
    asyncio.run(main())
