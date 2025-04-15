import os
import asyncio
import nats

class NatsSubscriber:
    def __init__(self, service_callback):
        self.nats_url = os.getenv("NATS_URL")
        self.service_callback = service_callback
        self.nc = None

    async def connect(self):
        self.nc = await nats.connect(self.nats_url)

    async def subscribe(self, topics):
        if isinstance(topics, str):
            topics = [topics]

        async def message_handler(msg):
            message = msg.data.decode()
            print(message)
            await self.service_callback(message)

        for topic in topics:
            await self.nc.subscribe(topic, cb=message_handler)

