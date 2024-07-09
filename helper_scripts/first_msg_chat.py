import asyncio
from bot import send_msg
from config import ART_CHAT_ID


async def send_message():
    await send_msg("Hello", thread=None, chat_id=ART_CHAT_ID)


asyncio.run(send_message())
