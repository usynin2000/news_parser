import httpx
import asyncio
from collections import deque
import feedparser

from bot import send_msg

from text_generator import generate_text


async def rss_parser(httpx_client, posted_q,
                     n_test_chars, send_message_func=None):
    '''Парсер rss ленты'''

    rss_link = 'https://rssexport.rbc.ru/rbcnews/news/20/full.rss'

    while True:
        try:
            response = await httpx_client.get(rss_link)
        except:
            await asyncio.sleep(10)
            continue

        feed = feedparser.parse(response.text)

        for entry in feed.entries[::-1]:
            summary = entry['summary']
            title = entry['title']
            link = entry['links'][0]['href']

            news_text = generate_text(title, summary, link, source="РБК")

            head = news_text[:n_test_chars].strip()

            if head in posted_q:
                continue

            if send_message_func is None:
                pass
                await send_msg(news_text)
            else:
                await send_message_func(f'rbc.ru\n{news_text}')

            posted_q.appendleft(head)

        await asyncio.sleep(60)


if __name__ == "__main__":

    # Очередь из уже опубликованных постов, чтобы их не дублировать
    posted_q = deque(maxlen=20)

    # 50 первых символов от текста новости - это ключ для проверки повторений
    n_test_chars = 50

    httpx_client = httpx.AsyncClient()

    asyncio.run(rss_parser(httpx_client, posted_q, n_test_chars))