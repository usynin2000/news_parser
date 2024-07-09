from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_HASH, API_ID


# Создаем клиент и получаем string session
with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("Ваша string session:\n")
    print(client.session.save())
