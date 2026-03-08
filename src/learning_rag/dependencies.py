from typing import AsyncGenerator

import aio_pika
from aio_pika.abc import AbstractRobustChannel


async def get_rabbitmq_client() -> AsyncGenerator[AbstractRobustChannel, None]:
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost")

    async with connection:
        channel = await connection.channel()
        yield channel
