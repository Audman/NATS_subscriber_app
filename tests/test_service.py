import pytest
from app.service.message_service import MessageService

@pytest.mark.asyncio
async def test_process_message_valid():
    service = MessageService()
    await service.process_message("Hello, test!")
