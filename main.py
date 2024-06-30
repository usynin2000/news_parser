import asyncio
from collections import deque

import httpx
from rss_parser import rss_parser
from telegram_parser import telegram_parser
from utils import create_logger
from bot import send_msg
from news_sources.tg_channels import telegram_channels
from news_sources.rss_channels import rss_channels

from config import (
    API_ID,
    API_HASH,
    STRING_SESSION,
)
from telethon.sessions import StringSession


# Configuration for post filtering
n_test_chars = 50
amount_messages = 300
posted_q = deque(maxlen=amount_messages)
timeout = 4

# Initialize logger
logger = create_logger("logger")
logger.info("Start...")


async def send_message_func(text, thread, parse_mode=None):
    logger.info(text)
    retry_after = 1
    while True:
        try:
            await send_msg(text, thread, parse_mode)
            await asyncio.sleep(timeout * 2)
        except Exception as e:
            if "429" in str(e):
                retry_after = int(str(e).split("retry after")[1].strip()) + 2
                logger.error(f"Too Many Requests: retrying after {retry_after} seconds")
                await asyncio.sleep(retry_after)
            else:
                logger.error(f"Failed to send message: {e}")
                break
        finally:
            break


# Query to check if parser works
async def fetch_with_retry(httpx_client, url, retries=3, timeout=20):
    for attempt in range(retries):
        try:
            response = await httpx_client.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            if attempt < retries - 1:
                await asyncio.sleep(2**attempt)  # Exponential backoff
                continue
            else:
                raise e


async def wrapper(httpx_client, source, rss_link, thread):
    is_done = False
    while not is_done:
        try:
            await fetch_with_retry(httpx_client, rss_link)
            await rss_parser(
                httpx_client,
                source,
                rss_link,
                posted_q,
                n_test_chars,
                lambda text: True,  # Placeholder for actual filtering function
                send_message_func,
                thread,
                logger,
                timeout,
            )
        except Exception as e:
            message = f"⚠️ ERROR: {source} parser is down! \n{e}"
            logger.error(message)
            await asyncio.sleep(timeout * 20)
        finally:
            is_done = True


async def main():
    await telegram_parser(
        StringSession(STRING_SESSION),
        API_ID,
        API_HASH,
        telegram_channels,
        posted_q,
        logger=logger,
    )
    async with httpx.AsyncClient() as httpx_client:
        tasks = []
        for source, rss_info in rss_channels.items():
            tasks.append(wrapper(httpx_client, source, rss_info[0], rss_info[1]))
            await asyncio.sleep(timeout)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        message = f"⚠️ ERROR: main loop is down! \n{e}"
        logger.error(message)
        print(message)
