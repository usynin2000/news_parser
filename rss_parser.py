import asyncio
from collections import deque
import httpx
import feedparser

from text_generator import generate_text
from utils import random_user_agent_headers
from config import ALERT_THREAD


async def rss_parser(
    httpx_client,
    source,
    rss_link,
    posted_q,
    n_test_chars=50,
    check_pattern_func=None,
    send_message_func=None,
    thread=ALERT_THREAD,
    logger=None,
    timeout=10,
):

    while True:
        try:
            response = await httpx_client.get(
                rss_link, headers=random_user_agent_headers()
            )
            response.raise_for_status()
        except Exception as e:
            if not (logger is None):
                logger.error(f"{source} rss error pass\n{e}")

            await asyncio.sleep(timeout * 10)
            continue

        feed = feedparser.parse(response.text)

        for entry in feed.entries[:3]:

            try:
                summary = entry["summary"]
            except KeyError:
                summary = ""

            title = entry["title"]
            link = entry["links"][0]["href"]

            news_text = f"{title}\n{summary}"

            if not (check_pattern_func is None):
                if not check_pattern_func(news_text):
                    continue

            # check for dublicates
            head = news_text[:n_test_chars].strip()
            if head in posted_q:
                continue

            post = generate_text(title, summary, link, source=source)

            if send_message_func is None:
                print(post, "\n")
            else:
                await send_message_func(post, thread, parse_mode="HTML")

            # put in queue in the beginning
            posted_q.appendleft(head)
            await asyncio.sleep(timeout)

        await asyncio.sleep(10 * timeout)


if __name__ == "__main__":
    source = "www.rbc.ru"

    rss_link = ("https://rssexport.rbc.ru/rbcnews/news/20/full.rss",)

    posted_q = deque(maxlen=20)

    httpx_client = httpx.AsyncClient()

    asyncio.run(rss_parser(httpx_client, source, rss_link, posted_q))
