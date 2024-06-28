import asyncio
from collections import deque

import httpx
from rss_parser import rss_parser
from telegram_parser import telegram_parser
from utils import create_logger
from bot import send_msg

from config import (
    MASS_MEDIA_THREAD,
    TECH_THREAD,
    ART_THREAD,
    API_ID,
    API_HASH,
    STRING_SESSION,
)
from telethon.sessions import StringSession

telegram_channels = {
    1099860397: "https://t.me/rbc_news",
    1101170442: "https://t.me/rian_ru",
    1133408457: "https://t.me/prime1",
    1149896996: "https://t.me/interfaxonline",
    1394050290: "https://t.me/bbbreaking",
    2216168393: "https://t.me/rio_testing",
    1115468824: "https://t.me/lentadnya",
    1036362176: "https://t.me/rt_russian",
    1003921752: "https://t.me/bbcrussian",
    # 2143062667: "https://t.me/2143062667",
    1106368426: "https://t.me/dumatv",
    1213234440: "https://t.me/rtvimain",
    1012339614: "https://t.me/rgrunews",
    1033134963: "https://t.me/inosmichannel",
    1031569976: "https://t.me/vcnews",
    1663745640: "https://t.me/dumabrief",
    1259487816: "https://t.me/SputnikARM",
    # 1833210104: "https://t.me/1833210104",
    1305489268: "https://t.me/blogsobyanin",
    # 1747110091: "https://t.me/1747110091",
    1447317686: "https://t.me/minobrnaukiofficial",
    1443309542: "https://t.me/trends",
    1763850118: "https://t.me/malepeg",
    1031559169: "https://t.me/DtOperativno",
    1238097313: "https://t.me/naukauniver",
    1333788481: "https://t.me/banki_oil",
    1345423158: "https://t.me/anon_prok",
    1260622817: "https://t.me/readovkanews",
    1742369677: "https://t.me/tele_eve",
    1432477212: "https://t.me/novosti_voinaa",
    1754252633: "https://t.me/joinchat/sOj9iDAtUkMyYWQy",
    1100158992: "https://t.me/shot_shot",
    1526452346: "https://t.me/government_rus",
    1065276858: "https://t.me/MID_Russia",
    2007734082: "https://t.me/mediamvd",
    1793307477: "https://t.me/minfin",
    1151131428: "https://t.me/mchs_official",
    1512944688: "https://t.me/minzdrav_ru",
    1082968817: "https://t.me/mod_russia",
    1222869173: "https://t.me/naebnet",
    1307778786: "https://t.me/exploitex",
    1319248631: "https://t.me/whackdoor",
    1381927809: "https://t.me/chatgpt3",
    1836239552: "https://t.me/hiaimedia",
    1752992242: "https://t.me/technomotel",
    1578782557: "https://t.me/NewHiTech9",
    1043793945: "https://t.me/d_code",
    1292630300: "https://t.me/mintsifry",
}

# RSS channels configuration
rss_channels = {
    "www.rbc.ru": [
        "https://rssexport.rbc.ru/rbcnews/news/20/full.rss",
        MASS_MEDIA_THREAD,
    ],
    "www.vedomosti.ru": [
        "https://www.vedomosti.ru/rss/rubric/business.xml",
        MASS_MEDIA_THREAD,
    ],
    "TECH www.vedomosti.ru": [
        "https://www.vedomosti.ru/rss/rubric/technology.xml",
        TECH_THREAD,
    ],
    "www.interfax.ru": ["https://www.interfax.ru/rss.asp", MASS_MEDIA_THREAD],
    "www.bloomberg.com": [
        "https://feeds.bloomberg.com/technology/news.rss",
        TECH_THREAD,
    ],
    "www.forbes.com": ["https://rss.app/feeds/0mitjp1cMnXGQkAZ.xml", TECH_THREAD],
    "Science www.wired.com": [
        "https://www.wired.com/feed/category/science/latest/rss",
        TECH_THREAD,
    ],
    "AI www.wired.com": ["https://www.wired.com/feed/tag/ai/latest/rss", TECH_THREAD],
    "www.artforum.com": ["https://www.artsjournal.com/feed", ART_THREAD],
}

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
        for source, rss_link in rss_channels.items():
            tasks.append(wrapper(httpx_client, source, rss_link[0], rss_link[1]))
            await asyncio.sleep(timeout)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        message = f"⚠️ ERROR: main loop is down! \n{e}"
        logger.error(message)
        print(message)
