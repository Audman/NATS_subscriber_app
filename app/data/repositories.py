import asyncio
from .database import SessionLocal
from .models import Message

class MessageRepository:
    def save_message(self, content, timestamp):
        def db_task():
            session = SessionLocal()
            try:
                msg = Message(content=content, timestamp=timestamp)
                session.add(msg)
                session.commit()
            finally:
                session.close()

        loop = asyncio.get_event_loop()
        return loop.run_in_executor(None, db_task)
