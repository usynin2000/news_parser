from telethon import TelegramClient, events
from env import API_ID, API_HASH, CHAT_ID

# Введите ваш API ID и API Hash, которые вы получили на my.telegram.org
api_id = API_ID
api_hash = API_HASH

# Телефонный номер вашего аккаунта Telegram
phone_number = '89165851045'

# ID канала откуда будем пересылать сообщение
source_channel_id = 2216168393  # Либо числовой ID, например: -1001234567890

# ID чата куда будем пересылать сообщение
target_chat_id = int(CHAT_ID)  # Либо числовой ID, например: -1009876543210

# Создаем клиент Telethon
client = TelegramClient('anon', api_id, api_hash)

async def main():
    await client.start(phone_number)

    # Получаем сущность целевого чата
    try:
        target_entity = await client.get_entity(target_chat_id)
        print(target_entity)
    except ValueError as e:
        print(f"Error: {e}")
        return

    @client.on(events.NewMessage(chats=source_channel_id))
    async def handler(event):
        try:
            # Пересылаем сообщение
            await client.forward_messages(target_entity, event.message)
            print("Message forwarded successfully.")
        except Exception as e:
            print(f"Failed to forward message: {e}")

    print("Listening for new messages...")
    await client.run_until_disconnected()

# Запускаем клиент
client.loop.run_until_complete(main())
