import asyncio
from telebot import async_telebot
from env import BOT_TOKEN, CHAT_ID, ALERT_THREAD


class TelegramClient:
    def __init__(self, token: str):
        self.token = token
        self.bot = async_telebot.AsyncTeleBot(BOT_TOKEN)

    async def send_alert(
        self,
        text: str,
        chat_id: str = CHAT_ID,
        thread_id: int = ALERT_THREAD,
        photo: str | None = None,
    ) -> None:
        if photo:
            await self.bot.send_photo(
                chat_id=chat_id,
                message_thread_id=thread_id,
                photo=photo,
                caption=text,
                parse_mode="HTML",
            )
        else:
            await self.bot.send_message(
                chat_id=chat_id,
                message_thread_id=thread_id,
                text=text,
                parse_mode="HTML",
                disable_web_page_preview=True
            )

    async def close(self):
        await self.bot.close_session()


async def send_msg(text: str):
    bot = TelegramClient(BOT_TOKEN)
    await bot.send_alert(text)
    await bot.close()

if __name__ == "__main__":
    asyncio.run(send_msg("MORGEN"))
