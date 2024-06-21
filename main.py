import asyncio
from collections import deque

import httpx
from rss_parser import rss_parser  # Ensure this is the correct import path for your project
from utils import create_logger
from bot import send_msg  # Ensure this is the correct import path for your project

from env import MASS_MEDIA_THREAD, TECH_THREAD, ART_THREAD

# RSS channels configuration
rss_channels = {
    'www.rbc.ru': ['https://rssexport.rbc.ru/rbcnews/news/20/full.rss', MASS_MEDIA_THREAD],
    "www.vedomosti.ru": ["https://www.vedomosti.ru/rss/rubric/business.xml", MASS_MEDIA_THREAD],
    "TECH www.vedomosti.ru": ["https://www.vedomosti.ru/rss/rubric/technology.xml", TECH_THREAD],
    'www.interfax.ru': ['https://www.interfax.ru/rss.asp', MASS_MEDIA_THREAD],
    'www.bloomberg.com': ['https://feeds.bloomberg.com/technology/news.rss', TECH_THREAD],
    "www.artforum.com": ["https://www.artsjournal.com/feed", ART_THREAD],
}

# Configuration for post filtering
n_test_chars = 50
amount_messages = 150
posted_q = deque(maxlen=amount_messages)
timeout = 4

# Initialize logger
logger = create_logger('gazp')
logger.info('Start...')


async def send_message_func(text, thread, parse_mode):
    logger.info(text)
    retry_after = None
    while True:
        try:
            await send_msg(text, thread, parse_mode)
            await asyncio.sleep(timeout * 2)
            break
        except Exception as e:
            if '429' in str(e):
                retry_after = int(str(e).split('retry after')[1].strip())
                logger.error(f'Too Many Requests: retrying after {retry_after} seconds')
                await asyncio.sleep(retry_after)
            else:
                logger.error(f'Failed to send message: {e}')
                break


async def fetch_with_retry(httpx_client, url, retries=3, timeout=10):
    for attempt in range(retries):
        try:
            response = await httpx_client.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                raise e


async def wrapper(httpx_client, source, rss_link, thread):
    is_done = False
    while not is_done:
        try:
            response = await fetch_with_retry(httpx_client, rss_link)
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
                timeout
            )
            is_done = True
        except Exception as e:
            message = f'⚠️ ERROR: {source} parser is down! \n{e}'
            logger.error(message)
            await asyncio.sleep(timeout * 20)


async def main():
    async with httpx.AsyncClient() as httpx_client:
        tasks = []
        for source, rss_link in rss_channels.items():
            tasks.append(wrapper(httpx_client, source, rss_link[0], rss_link[1]))
            await asyncio.sleep(timeout)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        message = f'⚠️ ERROR: main loop is down! \n{e}'
        logger.error(message)
        print(message)
