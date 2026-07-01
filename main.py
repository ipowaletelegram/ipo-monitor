import os
import json
import hashlib
import requests
from bs4 import BeautifulSoup

# ---------------- CONFIG ---------------- #

NSE_URL = "https://www.nseindia.com/get-quote/equity/RAMBHAJO/Advit-Jewels-Limited"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml",
    "Referer": "https://www.google.com/"
}

DATA_FILE = "monitor.json"

# ---------------- TELEGRAM ---------------- #

def send_telegram(message):
    if not BOT_TOKEN:
        print("BOT_TOKEN not found!")
        return

    if not CHAT_ID:
        print("CHAT_ID not found!")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=30
    )

    print("Telegram Status:", response.status_code)
    print("Telegram Response:", response.text)

# ---------------- NSE ---------------- #

def get_page():

    session = requests.Session()

    session.get(
        "https://www.nseindia.com",
        headers=HEADERS,
        timeout=30
    )

    response = session.get(
        NSE_URL,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return response.text

# ---------------- HASH ---------------- #

def extract_data(html):

    soup = BeautifulSoup(html, "html.parser")

    return soup.get_text(" ", strip=True)


def load_old_hash():

    if not os.path.exists(DATA_FILE):
        return None

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    return data.get("hash")


def save_hash(h):

    with open(DATA_FILE, "w") as f:
        json.dump({"hash": h}, f)

# ---------------- MAIN ---------------- #

def main():

    print("Checking NSE IPO page...")

    html = get_page()

    content = extract_data(html)

    new_hash = hashlib.sha256(content.encode()).hexdigest()

    old_hash = load_old_hash()

    # First Run
    if old_hash is None:

        save_hash(new_hash)

        send_telegram(
            "✅ IPO Monitor Started Successfully!\n\nGitHub Actions is working."
        )

        print("First run completed.")

        return

    # Change Detected
    if new_hash != old_hash:

        print("Change detected!")

        send_telegram(
            f"""🚨 NSE PAGE UPDATED

Website:
{NSE_URL}

Please check the page."""
        )

        save_hash(new_hash)

    else:

        print("No change.")

# ---------------- START ---------------- #

if __name__ == "__main__":
    main()
