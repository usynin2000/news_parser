from collections import deque
from telethon import TelegramClient, events
from utils import create_logger
from env import CHAT_ID


from env import API_ID, API_HASH


async def telegram_parser(
    session,
    api_id,
    api_hash,
    telegram_channels,
    posted_q,
    n_test_chars=50,
    check_pattern_func=None,
    logger=None,
    loop=None,
):

    telegram_channels_links = list(telegram_channels.values())

    client = TelegramClient(session, api_id, api_hash, base_logger=logger, loop=loop)

    await client.start()

    @client.on(events.NewMessage(chats=telegram_channels_links))
    async def handler(event):
        if event.raw_text == "":
            return

        news_text = " ".join(event.raw_text.split("\n")[:2])

        if not (check_pattern_func is None):
            if not check_pattern_func(news_text):
                return

        # dublicate check
        head = news_text[:n_test_chars].strip()
        if head in posted_q:
            return

        source = telegram_channels[event.message.peer_id.channel_id]
        link = f"{source}/{event.message.id}"
        channel = "@" + source.split("/")[-1]
        post = f"<b>{channel}</b>\n{link}\n{news_text}"

        target_entity = await client.get_entity(int(CHAT_ID))

        try:
            await client.forward_messages(target_entity, event.message)
            logger.info(f"✅ {post}")
        except Exception as e:
            logger.info(f"❌, {post} ERROR: {e}")

        posted_q.appendleft(head)

    return client


if __name__ == "__main__":

    logger = create_logger("TelegramParser")
    logger.info("Start...")
    # Initialize logger

    telegram_channels = {
        1099860397: "https://t.me/rbc_news",
        1101170442: "https://t.me/rian_ru",
        1133408457: "https://t.me/prime1",
        1288489154: "https://t.me/topor",
        1149896996: "https://t.me/interfaxonline",
        1203560567: "https://t.me/markettwits",
        1394050290: "https://t.me/bbbreaking",
        2216168393: "https://t.me/rio_testing",
    }

    # Очередь из уже опубликованных постов, чтобы их не дублировать
    posted_q = deque(maxlen=20)

    client = telegram_parser("gazp", API_ID, API_HASH, telegram_channels, posted_q, logger=logger)

    client.run_until_disconnected()
