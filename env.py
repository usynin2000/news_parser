import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

ALERT_THREAD = os.getenv("ALERT_THREAD")

MASS_MEDIA_THREAD = os.getenv("MASS_MEDIA_THREAD")

TECH_THREAD = os.getenv("TECH_THREAD")

ART_THREAD = os.getenv("ART_THREAD")


