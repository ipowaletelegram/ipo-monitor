import os

# Telegram

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Check interval (GitHub Actions handles scheduling)
CHECK_INTERVAL = 600

# Request timeout
TIMEOUT = 30

# Request headers

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

# File to store hashes

DATA_FILE = "monitor.json"

# Ignore words

IGNORE_WORDS = [
    "cookie",
    "cookies",
    "privacy",
    "copyright",
    "advertisement",
    "ads",
    "subscribe",
    "login",
    "sign in"
]

# Universal Website List

URLS = [

    {
        "name": "NSE",
        "url": "https://www.nseindia.com/index-tracker/NIFTY%2050",
        "mode": "text"
    },

    {
        "name": "BSE",
        "url": "https://www.bseindia.com/sensex/code/16",
        "mode": "text"
    },

    {
        "name": "SEBI",
        "url": "https://www.sebi.gov.in",
        "mode": "text"
    }

]
