from app.data.repositories import MessageRepository
import pytest
from datetime import datetime

@pytest.mark.asyncio
async def test_save_message_runs():
    repo = MessageRepository()
    await repo.save_message("Unit test message", datetime.utcnow())
