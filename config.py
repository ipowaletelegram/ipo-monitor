import os

# ==============================
# TELEGRAM SETTINGS
# ==============================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ==============================
# GENERAL SETTINGS
# ==============================

CHECK_INTERVAL = 600
TIMEOUT = 30

DATA_FILE = "monitor.json"

# ==============================
# REQUEST HEADERS
# ==============================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

# ==============================
# WORDS TO IGNORE
# ==============================

IGNORE_WORDS = [
    "cookie",
    "cookies",
    "privacy",
    "privacy policy",
    "copyright",
    "advertisement",
    "ads",
    "login",
    "sign in",
    "subscribe",
    "menu",
    "accept",
    "reject"
]

# ==============================
# UNIVERSAL WEBSITE LIST
# ==============================

URLS = [

    {
        "name": "SEBI DRHP",
        "url": "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=3&ssid=15&smid=10",
        "mode": "text",
        "selector": None,
        "ignore": []
    },
    {
        "name": "SEBI RHP",
        "url": "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=3&ssid=15&smid=11",
        "mode": "text",
        "selector": None,
        "ignore": []
    },
    {
    "name": "InvestorGain Mainboard GMP",
    "url": "https://www.investorgain.com/report/ipo-gmp-live/331/ipo/",
    "mode": "text",
    "selector": None,
    "ignore": []
}
]
