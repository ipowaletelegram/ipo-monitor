import hashlib
import json
import os
import re
import time

import requests
from bs4 import BeautifulSoup

from config import (
    HEADERS,
    DATA_FILE,
    IGNORE_WORDS,
    TIMEOUT
)

# -----------------------------
# HTTP SESSION
# -----------------------------

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Referer": "https://www.google.com/",
})
session.headers.update(HEADERS)


# -----------------------------
# DOWNLOAD WEBSITE
# -----------------------------

def download(url):

    last_error = None

    for attempt in range(3):

        try:

            response = session.get(
                url,
                timeout=TIMEOUT,
                allow_redirects=True,
            )

            response.raise_for_status()

            print("Status:", response.status_code)
            print("Final URL:", response.url)
            print("Content Length:", len(response.text))

            return response.text

        except Exception as e:

            last_error = e

            print(f"Retry {attempt+1}/3 : {e}")

            time.sleep(2)

    raise last_error

# -----------------------------
# CLEAN HTML
# -----------------------------

def clean_text(html):

    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted tags
    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "iframe"
    ]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    text = text.lower()

    # Ignore configured words
    for word in IGNORE_WORDS:

        text = text.replace(word.lower(), "")

    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)

    # Remove emails
    text = re.sub(r"\S+@\S+", "", text)

    # Remove extra blank lines
    text = re.sub(r"\n+", "\n", text)

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


# -----------------------------
# HASH
# -----------------------------

def get_hash(text):

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


# -----------------------------
# LOAD HASHES
# -----------------------------

def load_hashes():

    if not os.path.exists(DATA_FILE):

        return {}

    try:

        with open(DATA_FILE, "r", encoding="utf-8") as f:

            return json.load(f)

    except Exception:

        return {}


# -----------------------------
# SAVE HASHES
# -----------------------------

def save_hashes(data):

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# -----------------------------
# CHECK CHANGE
# -----------------------------

def check_change(name, new_hash):

    hashes = load_hashes()

    old_hash = hashes.get(name)

    # First Run
    if old_hash is None:

        hashes[name] = new_hash

        save_hashes(hashes)

        print(f"{name} : First Run")

        return False

    # Changed
    if old_hash != new_hash:

        hashes[name] = new_hash

        save_hashes(hashes)

        print(f"{name} : Changed")

        return True

    print(f"{name} : No Change")

    return False


# -----------------------------
# DELETE HASH
# -----------------------------

def delete_hash(name):

    hashes = load_hashes()

    if name in hashes:

        del hashes[name]

        save_hashes(hashes)


# -----------------------------
# RESET ALL
# -----------------------------

def reset_hashes():

    save_hashes({})

