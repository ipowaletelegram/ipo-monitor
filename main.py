import os
import json
import hashlib
import requests
from bs4 import BeautifulSoup

NSE_URL = "https://www.nseindia.com/get-quote/equity/RAMBHAJO/Advit-Jewels-Limited"

BOT_TOKEN = os.getenv("8453886638:AAGRB0psb6DW_zZQopj2MEZuWO7u3x8S-LY")
CHAT_ID = os.getenv("@Ipowalee_bot")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml",
    "Referer": "https://www.google.com/"
}

DATA_FILE = "monitor.json"


def send_telegram(msg):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram credentials missing.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


def get_page():
    session = requests.Session()

    # Visit home page first (helps with NSE)
    session.get(
        "https://www.nseindia.com",
        headers=HEADERS,
        timeout=30
    )

    r = session.get(
        NSE_URL,
        headers=HEADERS,
        timeout=30
    )

    r.raise_for_status()

    return r.text


def extract_data(html):
    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text(" ", strip=True)

    return text


def load_old_hash():
    if not os.path.exists(DATA_FILE):
        return None

    with open(DATA_FILE, "r") as f:
        return json.load(f).get("hash")


def save_hash(h):
    with open(DATA_FILE, "w") as f:
        json.dump({"hash": h}, f)


def main():

    print("Checking NSE IPO page...")

    html = get_page()

    content = extract_data(html)

    new_hash = hashlib.sha256(content.encode()).hexdigest()

    old_hash = load_old_hash()

    if old_hash is None:
        save_hash(new_hash)
        print("First run completed.")
        return

    if new_hash != old_hash:

        print("Change detected!")

        send_telegram(
            f"""🚨 NSE IPO PAGE UPDATED

Website:
{NSE_URL}

Please check for new IPO updates."""
        )

        save_hash(new_hash)

    else:
        print("No change.")


if __name__ == "__main__":
    main()
