import httpx
import asyncio
from collections import deque

from rss_parser import rss_parser

# Очередь из уже опубликованных постов, чтобы их не дублировать
posted_q = deque(maxlen=40)

# 50 первых символов от текста новости - это ключ для проверки повторений
n_test_chars = 50

async def print_message_func(message):
    '''Печатает посты в консоль'''
    print(message)

# Настройка event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

httpx_client = httpx.AsyncClient()

# Добавляет в текущий event_loop rss парсер
loop.create_task(rss_parser(httpx_client, posted_q, n_test_chars, print_message_func))

# Запуск event loop
loop.run_forever()
