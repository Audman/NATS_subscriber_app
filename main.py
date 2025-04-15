import asyncio
from app.api.nats_client import NatsSubscriber
from app.service.message_service import MessageService
from dotenv import load_dotenv

topics = ["messages"]

async def main():
    # Initialize service layer
    service = MessageService()

    # Initialize NATS subscriber
    subscriber = NatsSubscriber(service.process_message)
    await subscriber.connect()
    await subscriber.subscribe(topics)

    # Keep the connection alive
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
