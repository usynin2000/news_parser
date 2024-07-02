from config import (
    MASS_MEDIA_THREAD,
    TECH_THREAD,
)

rss_channels = {
    "www.rbc.ru": [
        "https://rssexport.rbc.ru/rbcnews/news/20/full.rss",
        MASS_MEDIA_THREAD,
    ],
    "www.vedomosti.ru": [
        "https://www.vedomosti.ru/rss/rubric/business.xml",
        MASS_MEDIA_THREAD,
    ],
    "www.vedomosti.ru (Tech)": [
        "https://www.vedomosti.ru/rss/rubric/technology.xml",
        TECH_THREAD,
    ],
    "www.interfax.ru": ["https://www.interfax.ru/rss.asp", MASS_MEDIA_THREAD],
    "www.bloomberg.com": [
        "https://feeds.bloomberg.com/technology/news.rss",
        TECH_THREAD,
    ],
    "www.forbes.com": ["https://rss.app/feeds/0mitjp1cMnXGQkAZ.xml", TECH_THREAD],
    "www.wired.com (Science)": [
        "https://www.wired.com/feed/category/science/latest/rss",
        TECH_THREAD,
    ],
    "www.wired.com (AI)": ["https://www.wired.com/feed/tag/ai/latest/rss", TECH_THREAD],
    # "www.artforum.com": ["https://www.artsjournal.com/feed", ART_THREAD],
    "www.ycombinator.com": ["https://news.ycombinator.com/rss", TECH_THREAD],
    "www.reddit.com": [
        "https://www.reddit.com/r/technology/top.rss?t=day",
        TECH_THREAD,
    ],
    "www.theguardian.com": [
        "https://www.theguardian.com/us/technology/rss",
        TECH_THREAD,
    ],
    "www.arstechnica.com": [
        "https://feeds.arstechnica.com/arstechnica/technology-lab",
        TECH_THREAD,
    ],
    "www.wsj.com": ["https://feeds.a.dj.com/rss/RSSWSJD.xml", TECH_THREAD],
    "www.ft.com": ["https://www.ft.com/technology?format=rss", TECH_THREAD],
    "www.it-world.ru (Market)": [
        "https://www.it-world.ru/it-news/market/rss/",
        TECH_THREAD,
    ],
    "www.it-world.ru (Tech)": [
        "https://www.it-world.ru/tech/technology/rss/",
        TECH_THREAD,
    ],
    "www.it-world.ru (Products)": [
        "https://www.it-world.ru/tech/products/rss/",
        TECH_THREAD,
    ],
    "www.it-world.ru (CIO News)": [
        "https://www.it-world.ru/cionews/business/rss/",
        TECH_THREAD,
    ],
    "www.it-world.ru (Government)": [
        "https://www.it-world.ru/cionews/government/rss/",
        TECH_THREAD,
    ],
    "www.it-world.ru (State and Law)": [
        "https://www.it-world.ru/it-news/state/rss/",
        TECH_THREAD,
    ],
    "www.techxplore.com (HI-Tech / Innovation)": [
        "https://techxplore.com/rss-feed/breaking/hi-tech-news/",
        TECH_THREAD,
    ],
    "www.techxplore.com (Software)": [
        "https://techxplore.com/rss-feed/software-news/",
        TECH_THREAD,
    ],
    "www.techxplore.com (ML/AI)": [
        "https://techxplore.com/rss-feed/breaking/machine-learning-ai-news/",
        TECH_THREAD,
    ],
    "www.techxplore.com (Internet)": [
        "https://techxplore.com/rss-feed/breaking/internet-news/",
        TECH_THREAD,
    ],
    "www.techxplore.com (CS)": [
        "https://techxplore.com/rss-feed/breaking/computer-sciences-news/",
        TECH_THREAD,
    ],
    "www.techxplore.com (Business)": [
        "https://techxplore.com/rss-feed/breaking/business-tech-news/",
        TECH_THREAD,
    ],
    "www.techxplore.com (Consumer / Gadgets)": [
        "https://techxplore.com/rss-feed/breaking/consumer-gadgets-news/",
        TECH_THREAD,
    ],
    "www.informationisbeautiful.com": [
        "https://informationisbeautiful.net/feed/",
        MASS_MEDIA_THREAD,
    ],
    "www.infographicsarchive.com": [
        "https://www.infographicsarchive.com/feed/",
        MASS_MEDIA_THREAD,
    ],
    "www.visualistan.com": [
        "https://www.visualistan.com/feeds/posts/default?alt=rss",
        MASS_MEDIA_THREAD,
    ],
    "www.rosstat.gov.ru": ["https://rosstat.gov.ru/folder/313/rss", MASS_MEDIA_THREAD],
}
