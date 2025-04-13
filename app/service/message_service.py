from datetime import datetime
from app.data.repositories import MessageRepository

class MessageService:
    def __init__(self):
        self.repo = MessageRepository()

    async def process_message(self, message_str):
        content = message_str.strip()
        if not content:
            raise ValueError("Empty message content")

        timestamp = datetime.now()
        await self.repo.save_message(content, timestamp)
