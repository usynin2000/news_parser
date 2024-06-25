import os

from dotenv import load_dotenv

load_dotenv()

# NOTIFIER BOT TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN")

# CHAT ENVS
CHAT_ID = os.getenv("CHAT_ID")
ALERT_THREAD = os.getenv("ALERT_THREAD")
MASS_MEDIA_THREAD = os.getenv("MASS_MEDIA_THREAD")
TECH_THREAD = os.getenv("TECH_THREAD")
ART_THREAD = os.getenv("ART_THREAD")

# 'HASH' account (to parse tg channels)
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

STRING_SESSION = os.getenv("STRING_SESSION")