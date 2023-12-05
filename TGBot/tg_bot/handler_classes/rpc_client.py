import asyncio
import uuid
from typing import MutableMapping, Callable
from aio_pika import Message, connect
from aio_pika.abc import (
    AbstractChannel, AbstractConnection, AbstractIncomingMessage, AbstractQueue,
)


class RPCClient:
    connection: AbstractConnection
    channel: AbstractChannel
    callback_queue: AbstractQueue

    def __init__(self) -> None:
        self.futures: MutableMapping[str, asyncio.Future] = {}

    async def connect(self) -> "RPCClient":
        while True:
            try:
                self.connection = await connect("http://rabbitmq:5672")
                self.channel = await self.connection.channel()
                self.callback_queue = await self.channel.declare_queue(exclusive=True)
                await self.callback_queue.consume(self.on_response, no_ack=True)
                return self
            except Exception as e:
                print(f"Failed to connect to RabbitMQ: {e}")
                await asyncio.sleep(3)

    async def on_response(self, message: AbstractIncomingMessage) -> None:
        if message.correlation_id is None:
            print(f"Bad message {message!r}")
            return
        future: asyncio.Future = self.futures.pop(message.correlation_id)
        future.set_result(message.body.decode('utf-8'))

    async def get_image_info(self, url: str, standart_info: bool) -> str:
        correlation_id = str(uuid.uuid4())
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self.futures[correlation_id] = future

        await self.channel.default_exchange.publish(
            Message(
                url.encode(),
                content_type="text/plain",
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
            ),
            routing_key="standart_image_caption" if standart_info else "additional_image_caption",
        )
        return await future
